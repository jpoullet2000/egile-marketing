"""
Exception classes for the Egile Marketing package.

Provides a hierarchy of custom exceptions for better error handling
and debugging in marketing automation workflows.
"""

from typing import Optional, Dict, Any


class EgileMarketingError(Exception):
    """Base exception for all Egile Marketing errors."""

    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.operation = operation
        self.context = context or {}

    def __str__(self) -> str:
        if self.operation:
            return f"{self.operation}: {self.message}"
        return self.message


class AzureOpenAIError(EgileMarketingError):
    """Raised when Azure OpenAI operations fail."""

    def __init__(
        self,
        message: str,
        model: Optional[str] = None,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, operation, context)
        self.model = model
        self.status_code = status_code
        self.request_id = request_id


class MCPServerError(EgileMarketingError):
    """Raised when MCP server operations fail."""

    def __init__(
        self,
        message: str,
        server_name: Optional[str] = None,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, operation, context)
        self.server_name = server_name


class MarketingAgentError(EgileMarketingError):
    """Raised when marketing agent operations fail."""

    def __init__(
        self,
        message: str,
        agent_name: Optional[str] = None,
        operation: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, operation, context)
        self.agent_name = agent_name


class ContentGenerationError(EgileMarketingError):
    """Raised when content generation fails."""

    pass


class SocialMediaError(EgileMarketingError):
    """Raised when social media operations fail."""

    pass


class EmailCampaignError(EgileMarketingError):
    """Raised when email campaign operations fail."""

    pass


class SEOError(EgileMarketingError):
    """Raised when SEO operations fail."""

    pass


class AnalyticsError(EgileMarketingError):
    """Raised when analytics operations fail."""

    pass


class LeadScoringError(EgileMarketingError):
    """Raised when lead scoring operations fail."""

    pass


class SegmentationError(EgileMarketingError):
    """Raised when customer segmentation operations fail."""

    pass


class ABTestError(EgileMarketingError):
    """Raised when A/B testing operations fail."""

    pass


class AuthenticationError(EgileMarketingError):
    """Raised when authentication fails."""

    def __init__(self, message: str, auth_method: Optional[str] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.auth_method = auth_method


class ConfigurationError(EgileMarketingError):
    """Raised when configuration is invalid."""

    pass


class RetryableError(EgileMarketingError):
    """Raised for errors that can be retried."""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after
