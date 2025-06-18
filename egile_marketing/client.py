"""
Azure OpenAI Client for marketing automation with managed identity support.

This client implements marketing-specific features on top of Azure OpenAI:
- Managed Identity authentication (preferred)
- Service Principal fallback for CI/CD
- Comprehensive error handling with retry logic
- Marketing-specific prompts and templates
- Content optimization and scoring
- Campaign performance tracking
"""

import os
import logging
from typing import Optional, Dict, Any, List, AsyncGenerator
from datetime import datetime, timedelta
import asyncio

from azure.identity import (
    DefaultAzureCredential,
    ManagedIdentityCredential,
    ClientSecretCredential,
)
from azure.keyvault.secrets import SecretClient
from openai import AsyncAzureOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import structlog
import httpx

from .exceptions import AzureOpenAIError, AuthenticationError, RetryableError
from .config import AzureOpenAIConfig


logger = structlog.get_logger(__name__)


class AzureOpenAIClient:
    """
    Azure OpenAI client optimized for marketing automation.

    Features:
    - Managed Identity authentication (Azure-hosted environments)
    - Service Principal authentication (CI/CD pipelines)
    - Key Vault integration for secure credential storage
    - Automatic retry with exponential backoff
    - Request/response logging and monitoring
    - Marketing-specific prompt templates
    - Content scoring and optimization
    """

    def __init__(
        self,
        config: Optional[AzureOpenAIConfig] = None,
        endpoint: Optional[str] = None,
        api_version: str = "2024-12-01-preview",
        max_retries: int = 3,
        timeout: int = 30,
        use_managed_identity: bool = True,
    ):
        """
        Initialize Azure OpenAI client for marketing automation.

        Args:
            config: Optional configuration object
            endpoint: Azure OpenAI endpoint URL
            api_version: API version to use
            max_retries: Maximum number of retries for failed requests
            timeout: Request timeout in seconds
            use_managed_identity: Whether to use managed identity for auth
        """
        self.config = config or AzureOpenAIConfig.from_environment()
        self.endpoint = endpoint or self.config.endpoint
        self.api_version = api_version
        self.max_retries = max_retries
        self.timeout = timeout
        self.use_managed_identity = use_managed_identity

        self._client: Optional[AsyncAzureOpenAI] = None
        self._credential = None
        self._last_token_refresh = None
        self._token_cache = None

        logger.info(
            "Initializing Azure OpenAI client for marketing automation",
            endpoint=self.endpoint,
            api_version=self.api_version,
            use_managed_identity=self.use_managed_identity,
        )

    async def _get_credential(self):
        """Get Azure credential with fallback strategy."""
        if self._credential is None:
            try:
                if self.use_managed_identity:
                    # Preferred: Use Managed Identity in Azure-hosted environments
                    self._credential = ManagedIdentityCredential()
                    logger.info("Using Managed Identity for authentication")
                else:
                    # Fallback: Use Default Azure Credential chain
                    self._credential = DefaultAzureCredential()
                    logger.info("Using Default Azure Credential for authentication")

            except Exception as e:
                logger.error("Failed to initialize Azure credential", error=str(e))
                raise AuthenticationError(
                    f"Failed to initialize Azure credential: {e}",
                    auth_method="managed_identity"
                    if self.use_managed_identity
                    else "default",
                )

        return self._credential

    async def _get_api_key_from_keyvault(self) -> Optional[str]:
        """Retrieve API key from Azure Key Vault if configured."""
        if not self.config.key_vault_url or not self.config.api_key_secret_name:
            return None

        try:
            credential = await self._get_credential()
            secret_client = SecretClient(
                vault_url=self.config.key_vault_url, credential=credential
            )

            secret = secret_client.get_secret(self.config.api_key_secret_name)
            logger.info("Retrieved API key from Key Vault")
            return secret.value

        except Exception as e:
            logger.error("Failed to retrieve API key from Key Vault", error=str(e))
            raise AuthenticationError(f"Failed to retrieve API key from Key Vault: {e}")

    async def _initialize_client(self):
        """Initialize the OpenAI client with proper authentication."""
        if self._client is not None:
            return self._client

        try:
            api_key = (
                os.getenv("AZURE_OPENAI_API_KEY") or self.config.api_key_secret_name
            )
            # Try to get API key from Key Vault first
            if not api_key:
                api_key = await self._get_api_key_from_keyvault()
            if api_key:
                # Use API key authentication
                self._client = AsyncAzureOpenAI(
                    api_key=api_key,
                    azure_endpoint=self.endpoint,
                    api_version=self.api_version,
                    timeout=httpx.Timeout(self.timeout),
                    max_retries=self.max_retries,
                )
                logger.info("Initialized client with API key authentication")
            else:
                # Use Azure AD token authentication
                credential = await self._get_credential()
                token = credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )

                self._client = AsyncAzureOpenAI(
                    azure_ad_token=token.token,
                    azure_endpoint=self.endpoint,
                    api_version=self.api_version,
                    timeout=httpx.Timeout(self.timeout),
                    max_retries=self.max_retries,
                )

                self._token_cache = token
                self._last_token_refresh = datetime.now()
                logger.info("Initialized client with Azure AD token authentication")

            return self._client

        except Exception as e:
            logger.error("Failed to initialize Azure OpenAI client", error=str(e))
            raise AzureOpenAIError(f"Failed to initialize client: {e}")

    async def _refresh_token_if_needed(self):
        """Refresh Azure AD token if it's close to expiration."""
        if not self._token_cache or not self._last_token_refresh:
            return

        # Refresh token if it expires within 5 minutes
        if (datetime.now() - self._last_token_refresh) > timedelta(minutes=55):
            try:
                credential = await self._get_credential()
                token = credential.get_token(
                    "https://cognitiveservices.azure.com/.default"
                )

                # Update client with new token
                if hasattr(self._client, "_azure_ad_token"):
                    self._client._azure_ad_token = token.token

                self._token_cache = token
                self._last_token_refresh = datetime.now()
                logger.info("Refreshed Azure AD token")

            except Exception as e:
                logger.warning("Failed to refresh Azure AD token", error=str(e))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(RetryableError),
    )
    async def chat_completion(
        self,
        messages: List[ChatCompletionMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> ChatCompletion:
        """
        Create a chat completion with retry logic and error handling.

        Args:
            messages: List of chat messages
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Returns:
            Chat completion response

        Raises:
            AzureOpenAIError: For API errors
            RetryableError: For retryable errors
        """
        # Use default model from config if none specified
        if model is None:
            model = self.config.default_model

        client = await self._initialize_client()
        await self._refresh_token_if_needed()

        request_start = datetime.now()
        request_id = f"req_{int(request_start.timestamp())}"

        logger.info(
            "Starting chat completion request",
            request_id=request_id,
            model=model,
            message_count=len(messages),
            temperature=temperature,
        )

        try:
            response = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs,
            )

            duration = (datetime.now() - request_start).total_seconds()

            logger.info(
                "Chat completion request completed",
                request_id=request_id,
                duration_seconds=duration,
                usage=response.usage.model_dump() if response.usage else None,
            )

            return response

        except Exception as e:
            duration = (datetime.now() - request_start).total_seconds()

            logger.error(
                "Chat completion request failed",
                request_id=request_id,
                duration_seconds=duration,
                error=str(e),
            )

            # Determine if error is retryable
            if hasattr(e, "status_code"):
                status_code = e.status_code
                if status_code in [429, 500, 502, 503, 504]:
                    raise RetryableError(
                        f"Retryable error {status_code}: {e}",
                        retry_after=getattr(e, "retry_after", None),
                    )
                else:
                    raise AzureOpenAIError(
                        f"API error {status_code}: {e}",
                        status_code=status_code,
                        request_id=request_id,
                    )
            else:
                raise AzureOpenAIError(f"Unexpected error: {e}", request_id=request_id)

    async def generate_marketing_content(
        self,
        content_type: str,
        brief: str,
        target_audience: str,
        tone: str = "professional",
        length: str = "medium",
        model: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Generate marketing content using optimized prompts.

        Args:
            content_type: Type of content (email, social, blog, ad, etc.)
            brief: Content brief and requirements
            target_audience: Description of target audience
            tone: Desired tone of voice
            length: Content length (short, medium, long)
            model: Model to use for generation

        Returns:
            Generated marketing content
        """
        # Use default model from config if none specified
        if model is None:
            model = self.config.default_model

        system_prompt = f"""You are an expert marketing copywriter. Generate high-quality {content_type} content that:
- Follows marketing best practices
- Engages the target audience effectively
- Maintains a {tone} tone of voice
- Is optimized for conversion
- Includes clear calls-to-action when appropriate"""

        user_prompt = f"""Create {content_type} content with the following specifications:

Content Brief: {brief}

Target Audience: {target_audience}

Tone: {tone}
Length: {length}

Please provide compelling, conversion-focused content that resonates with the target audience."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = await self.chat_completion(
            messages=messages, model=model, temperature=0.7, **kwargs
        )

        return response.choices[0].message.content

    async def score_content_effectiveness(
        self,
        content: str,
        content_type: str,
        target_audience: str,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Score marketing content effectiveness.

        Args:
            content: Content to score
            content_type: Type of content
            target_audience: Target audience description
            model: Model to use for scoring

        Returns:
            Content effectiveness scores and recommendations
        """
        # Use default model from config if none specified
        if model is None:
            model = self.config.default_model

        system_prompt = """You are a marketing analytics expert. Analyze marketing content and provide scores (1-10) for:
- Overall effectiveness
- Audience alignment
- Clarity and readability
- Call-to-action strength
- Emotional impact
- SEO potential (if applicable)

Also provide specific recommendations for improvement."""

        user_prompt = f"""Analyze this {content_type} content for {target_audience}:

{content}

Provide detailed scoring and actionable recommendations for improvement."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = await self.chat_completion(
            messages=messages, model=model, temperature=0.3
        )

        # Note: In production, you'd parse this response into structured data
        return {
            "raw_analysis": response.choices[0].message.content,
            "analyzed_at": datetime.now().isoformat(),
        }

    async def stream_chat_completion(
        self,
        messages: List[ChatCompletionMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Create a streaming chat completion.

        Args:
            messages: List of chat messages
            model: Model name to use
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional parameters

        Yields:
            Streaming response chunks
        """
        # Use default model from config if none specified
        if model is None:
            model = self.config.default_model

        client = await self._initialize_client()
        await self._refresh_token_if_needed()

        request_start = datetime.now()
        request_id = f"stream_req_{int(request_start.timestamp())}"

        logger.info(
            "Starting streaming chat completion request",
            request_id=request_id,
            model=model,
            message_count=len(messages),
        )

        try:
            stream = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs,
            )

            async for chunk in stream:
                yield chunk.model_dump()

        except Exception as e:
            logger.error(
                "Streaming chat completion failed", request_id=request_id, error=str(e)
            )
            raise AzureOpenAIError(f"Streaming error: {e}", request_id=request_id)

    async def close(self):
        """Clean up resources."""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Azure OpenAI client closed")

    async def __aenter__(self):
        """Async context manager entry."""
        await self._initialize_client()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
