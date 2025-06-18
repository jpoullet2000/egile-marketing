"""
Content Generator tool for creating marketing content using AI.

This tool provides advanced content generation capabilities specifically
designed for marketing use cases.
"""

import json
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

import structlog

from ..client import AzureOpenAIClient
from ..config import ContentGenerationConfig, AzureOpenAIConfig
from ..exceptions import ContentGenerationError


logger = structlog.get_logger(__name__)


@dataclass
class ContentRequest:
    """Structure for content generation requests."""

    content_type: str
    brief: str
    target_audience: str
    tone: str = "professional"
    length: str = "medium"
    keywords: Optional[List[str]] = None
    brand_guidelines: Optional[Dict[str, Any]] = None
    template_id: Optional[str] = None


@dataclass
class GeneratedContent:
    """Structure for generated content response."""

    content: str
    content_type: str
    target_audience: str
    tone: str
    length: str
    keywords: List[str]
    effectiveness_score: Optional[Dict[str, Any]] = None
    seo_metrics: Optional[Dict[str, Any]] = None
    generated_at: str = ""
    metadata: Optional[Dict[str, Any]] = None


class ContentGenerator:
    """
    AI-powered marketing content generator.

    Features:
    - Multi-format content generation (emails, social posts, blogs, ads)
    - Brand voice consistency
    - SEO optimization
    - Content scoring and optimization
    - Template-based generation
    - A/B variant creation
    """

    def __init__(
        self,
        openai_client: Optional[AzureOpenAIClient] = None,
        config: Optional[ContentGenerationConfig] = None,
    ):
        """
        Initialize the content generator.

        Args:
            openai_client: Azure OpenAI client
            config: Content generation configuration
        """
        self.config = config or ContentGenerationConfig()
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )

        self._content_templates: Dict[str, Dict[str, Any]] = {}
        self._brand_guidelines: Dict[str, Any] = {}

        logger.info("Content Generator initialized")

    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """
        Generate marketing content based on the request.

        Args:
            request: Content generation request

        Returns:
            Generated content with metadata
        """
        try:
            logger.info(
                "Generating content",
                content_type=request.content_type,
                target_audience=request.target_audience,
                tone=request.tone,
            )

            # Build the generation prompt
            system_prompt = self._build_system_prompt(request)
            user_prompt = self._build_user_prompt(request)

            # Generate content using AI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            response = await self.openai_client.chat_completion(
                messages=messages,
                # Use client's default model instead of config model
                # model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
            )

            generated_text = response.choices[0].message.content

            # Post-process content if needed
            processed_content = self._post_process_content(generated_text, request)

            # Calculate SEO metrics if enabled
            seo_metrics = None
            if self.config.seo_optimization and request.keywords:
                seo_metrics = self._calculate_seo_metrics(
                    processed_content, request.keywords
                )

            # Score content effectiveness
            effectiveness_score = await self._score_content_effectiveness(
                processed_content, request
            )

            result = GeneratedContent(
                content=processed_content,
                content_type=request.content_type,
                target_audience=request.target_audience,
                tone=request.tone,
                length=request.length,
                keywords=request.keywords or [],
                effectiveness_score=effectiveness_score,
                seo_metrics=seo_metrics,
                generated_at=datetime.now().isoformat(),
                metadata={
                    "model_used": self.config.model,
                    "temperature": self.config.temperature,
                    "brand_guidelines_applied": bool(request.brand_guidelines),
                },
            )

            logger.info("Content generated successfully")
            return result

        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            raise ContentGenerationError(f"Failed to generate content: {e}")

    async def generate_ab_variants(
        self, request: ContentRequest, variant_count: int = 2
    ) -> List[GeneratedContent]:
        """
        Generate multiple A/B test variants of content.

        Args:
            request: Base content request
            variant_count: Number of variants to generate

        Returns:
            List of content variants
        """
        try:
            variants = []

            for i in range(variant_count):
                # Modify request slightly for each variant
                variant_request = self._create_variant_request(request, i)
                variant_content = await self.generate_content(variant_request)
                variant_content.metadata = variant_content.metadata or {}
                variant_content.metadata["variant_id"] = f"variant_{i + 1}"
                variants.append(variant_content)

            logger.info(f"Generated {len(variants)} A/B variants")
            return variants

        except Exception as e:
            logger.error(f"A/B variant generation failed: {e}")
            raise ContentGenerationError(f"Failed to generate A/B variants: {e}")

    async def optimize_content(
        self,
        content: str,
        content_type: str,
        target_audience: str,
        optimization_goals: List[str],
    ) -> str:
        """
        Optimize existing content for specific goals.

        Args:
            content: Original content
            content_type: Type of content
            target_audience: Target audience
            optimization_goals: List of optimization objectives

        Returns:
            Optimized content
        """
        try:
            optimization_prompt = f"""
            Optimize the following {content_type} content for {target_audience} with these goals:
            {", ".join(optimization_goals)}

            Original content:
            {content}

            Provide the optimized version that better achieves the specified goals while maintaining the core message.
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are a marketing optimization expert.",
                },
                {"role": "user", "content": optimization_prompt},
            ]

            response = await self.openai_client.chat_completion(
                messages=messages, model=self.config.model, temperature=0.5
            )

            optimized_content = response.choices[0].message.content

            logger.info("Content optimized successfully")
            return optimized_content

        except Exception as e:
            logger.error(f"Content optimization failed: {e}")
            raise ContentGenerationError(f"Failed to optimize content: {e}")

    def _build_system_prompt(self, request: ContentRequest) -> str:
        """Build system prompt for content generation."""
        brand_text = ""
        if request.brand_guidelines:
            brand_text = f"\\n\\nBrand Guidelines:\\n{json.dumps(request.brand_guidelines, indent=2)}"

        template_text = ""
        if request.template_id and request.template_id in self._content_templates:
            template = self._content_templates[request.template_id]
            template_text = (
                f"\\n\\nContent Template:\\n{json.dumps(template, indent=2)}"
            )

        return f"""You are an expert marketing copywriter specializing in {request.content_type} content.

Your task is to create compelling, conversion-focused {request.content_type} content that:
- Resonates with the target audience: {request.target_audience}
- Maintains a {request.tone} tone of voice
- Follows marketing best practices for {request.content_type}
- Includes clear calls-to-action when appropriate
- Is optimized for engagement and conversion
- Meets {request.length} length requirements

{brand_text}{template_text}

Focus on creating content that drives action and achieves marketing objectives."""

    def _build_user_prompt(self, request: ContentRequest) -> str:
        """Build user prompt for content generation."""
        keywords_text = ""
        if request.keywords:
            keywords_text = f"\\n\\nSEO Keywords to naturally incorporate: {', '.join(request.keywords)}"

        length_guidance = {
            "short": "Keep it concise and punchy (50-150 words)",
            "medium": "Provide good detail and engagement (150-400 words)",
            "long": "Create comprehensive, detailed content (400+ words)",
        }

        return f"""Content Brief: {request.brief}

Target Audience: {request.target_audience}
Tone: {request.tone}
Length: {request.length} - {length_guidance.get(request.length, "")}
{keywords_text}

Please create engaging, high-quality {request.content_type} content that meets these requirements and drives the desired action."""

    def _post_process_content(self, content: str, request: ContentRequest) -> str:
        """Post-process generated content."""
        # Remove any markdown formatting if not needed
        if request.content_type in ["email", "social_media"]:
            content = re.sub(r"\*\*(.*?)\*\*", r"\\1", content)  # Remove bold
            content = re.sub(r"\*(.*?)\*", r"\\1", content)  # Remove italic

        # Ensure proper length constraints
        if request.length == "short" and len(content.split()) > 150:
            sentences = content.split(". ")
            content = ". ".join(sentences[:3]) + "."

        return content.strip()

    def _calculate_seo_metrics(
        self, content: str, keywords: List[str]
    ) -> Dict[str, Any]:
        """Calculate basic SEO metrics for content."""
        word_count = len(content.split())

        keyword_metrics = {}
        for keyword in keywords:
            keyword_count = content.lower().count(keyword.lower())
            keyword_density = keyword_count / word_count if word_count > 0 else 0
            keyword_metrics[keyword] = {
                "count": keyword_count,
                "density": round(keyword_density, 4),
            }

        return {
            "word_count": word_count,
            "keyword_metrics": keyword_metrics,
            "readability_estimate": "medium",  # Placeholder
            "seo_score": min(
                100, sum(m["count"] for m in keyword_metrics.values()) * 10
            ),
        }

    async def _score_content_effectiveness(
        self, content: str, request: ContentRequest
    ) -> Dict[str, Any]:
        """Score content effectiveness using AI."""
        try:
            scoring_prompt = f"""
            Score this {request.content_type} content for {request.target_audience} on a scale of 1-10 for:
            1. Overall effectiveness
            2. Audience alignment  
            3. Clarity and readability
            4. Call-to-action strength
            5. Emotional impact

            Content: {content}

            Provide scores and brief explanations in JSON format.
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are a marketing effectiveness analyst. Provide objective scoring.",
                },
                {"role": "user", "content": scoring_prompt},
            ]

            response = await self.openai_client.chat_completion(
                messages=messages, temperature=0.2
            )

            return {
                "raw_analysis": response.choices[0].message.content,
                "scored_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.warning(f"Content scoring failed: {e}")
            return {"error": str(e)}

    def _create_variant_request(
        self, base_request: ContentRequest, variant_index: int
    ) -> ContentRequest:
        """Create a variant of the base request for A/B testing."""
        # Modify tone or approach slightly for variants
        tone_variants = {
            0: base_request.tone,
            1: "conversational"
            if base_request.tone == "professional"
            else "professional",
            2: "enthusiastic" if base_request.tone != "enthusiastic" else "friendly",
        }

        return ContentRequest(
            content_type=base_request.content_type,
            brief=base_request.brief,
            target_audience=base_request.target_audience,
            tone=tone_variants.get(variant_index, base_request.tone),
            length=base_request.length,
            keywords=base_request.keywords,
            brand_guidelines=base_request.brand_guidelines,
            template_id=base_request.template_id,
        )

    def load_templates(self, templates: Dict[str, Dict[str, Any]]):
        """Load content templates."""
        self._content_templates.update(templates)
        logger.info(f"Loaded {len(templates)} content templates")

    def set_brand_guidelines(self, guidelines: Dict[str, Any]):
        """Set brand guidelines for content generation."""
        self._brand_guidelines = guidelines
        logger.info("Brand guidelines updated")
