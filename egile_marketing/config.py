"""
Configuration classes for the Egile Marketing package.

These classes provide type-safe configuration management
following Azure best practices for marketing automation.
"""

import os
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv


@dataclass
class AzureOpenAIConfig:
    """Configuration for Azure OpenAI client."""

    endpoint: str
    api_version: str = "2024-02-15-preview"
    key_vault_url: Optional[str] = None
    api_key_secret_name: Optional[str] = None
    default_model: str = "gpt-4"
    max_retries: int = 3
    timeout: int = 30
    use_managed_identity: bool = True

    @classmethod
    def from_environment(cls, env_file: Optional[str] = None) -> "AzureOpenAIConfig":
        """Load configuration from environment variables."""
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load from .env file in current directory
            load_dotenv()

        return cls(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            key_vault_url=os.getenv("AZURE_KEY_VAULT_URL"),
            api_key_secret_name=os.getenv("AZURE_OPENAI_API_KEY_SECRET_NAME"),
            default_model=os.getenv("AZURE_OPENAI_DEFAULT_MODEL", "gpt-4"),
            max_retries=int(os.getenv("AZURE_OPENAI_MAX_RETRIES", "3")),
            timeout=int(os.getenv("AZURE_OPENAI_TIMEOUT", "30")),
            use_managed_identity=os.getenv("AZURE_USE_MANAGED_IDENTITY", "true").lower()
            == "true",
        )


class MarketingServerConfig(BaseModel):
    """Configuration for Marketing MCP servers."""

    name: str = Field(..., description="Unique name for the marketing MCP server")
    description: str = Field(
        ..., description="Description of server marketing capabilities"
    )
    host: str = Field(default="localhost", description="Server host")
    port: int = Field(default=8000, description="Server port")
    capabilities: Union[List[str], Dict[str, Any]] = Field(
        default_factory=list, description="Server capabilities"
    )
    tools: Union[List[str], Dict[str, Any]] = Field(
        default_factory=list, description="Available marketing tools"
    )
    resources: Union[List[str], Dict[str, Any]] = Field(
        default_factory=list, description="Available marketing resources"
    )
    max_connections: int = Field(
        default=100, description="Maximum concurrent connections"
    )
    timeout: int = Field(default=30, description="Request timeout in seconds")

    # Marketing-specific configuration
    content_templates_path: Optional[str] = Field(
        default=None, description="Path to content templates"
    )
    brand_guidelines_path: Optional[str] = Field(
        default=None, description="Path to brand guidelines"
    )
    campaign_data_path: Optional[str] = Field(
        default=None, description="Path to campaign data"
    )
    analytics_config: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Analytics configuration"
    )

    @validator("port")
    def validate_port(cls, v):
        if not (1 <= v <= 65535):
            raise ValueError("Port must be between 1 and 65535")
        return v

    @validator("name")
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()


class MarketingAgentConfig(BaseModel):
    """Configuration for the Marketing Agent."""

    name: str = Field(default="MarketingAgent", description="Agent name")
    description: str = Field(
        default="Intelligent marketing automation agent",
        description="Agent description",
    )
    openai_config: AzureOpenAIConfig = Field(
        ..., description="Azure OpenAI configuration"
    )
    server_selection_model: str = Field(
        default="gpt-4", description="Model for server selection"
    )
    max_server_selection_retries: int = Field(
        default=3, description="Max retries for server selection"
    )
    selection_temperature: float = Field(
        default=0.1, description="Temperature for server selection"
    )
    cache_selection_results: bool = Field(
        default=True, description="Whether to cache selection results"
    )
    cache_ttl_seconds: int = Field(default=300, description="Cache TTL in seconds")

    # Marketing-specific agent configuration
    content_generation_model: str = Field(
        default="gpt-4", description="Model for content generation"
    )
    content_temperature: float = Field(
        default=0.7, description="Temperature for content generation"
    )
    analytics_model: str = Field(
        default="gpt-4", description="Model for analytics and insights"
    )
    campaign_optimization_model: str = Field(
        default="gpt-4", description="Model for campaign optimization"
    )

    # Brand and voice configuration
    brand_voice: str = Field(default="professional", description="Default brand voice")
    target_audiences: List[str] = Field(
        default_factory=list, description="Default target audiences"
    )
    content_types: List[str] = Field(
        default_factory=lambda: [
            "email",
            "social_media",
            "blog_post",
            "ad_copy",
            "landing_page",
        ],
        description="Supported content types",
    )

    @validator("selection_temperature")
    def validate_temperature(cls, v):
        if not (0.0 <= v <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    @validator("content_temperature")
    def validate_content_temperature(cls, v):
        if not (0.0 <= v <= 2.0):
            raise ValueError("Content temperature must be between 0.0 and 2.0")
        return v

    @validator("max_server_selection_retries")
    def validate_retries(cls, v):
        if v < 1:
            raise ValueError("Max retries must be at least 1")
        return v


class ContentGenerationConfig(BaseModel):
    """Configuration for content generation tools."""

    model: str = Field(default="gpt-4", description="Model for content generation")
    temperature: float = Field(
        default=0.7, description="Temperature for content generation"
    )
    max_tokens: int = Field(default=2000, description="Maximum tokens per generation")
    templates_enabled: bool = Field(
        default=True, description="Whether to use content templates"
    )
    brand_guidelines_enabled: bool = Field(
        default=True, description="Whether to enforce brand guidelines"
    )

    # Content optimization settings
    seo_optimization: bool = Field(default=True, description="Enable SEO optimization")
    readability_target: str = Field(
        default="college", description="Target readability level"
    )
    keyword_density_target: float = Field(
        default=0.02, description="Target keyword density"
    )


class SocialMediaConfig(BaseModel):
    """Configuration for social media management."""

    platforms: List[str] = Field(
        default_factory=lambda: ["twitter", "linkedin", "facebook", "instagram"],
        description="Supported social media platforms",
    )

    posting_schedule: Dict[str, Any] = Field(
        default_factory=dict, description="Posting schedule configuration"
    )
    hashtag_strategy: Dict[str, Any] = Field(
        default_factory=dict, description="Hashtag strategy configuration"
    )
    engagement_targets: Dict[str, float] = Field(
        default_factory=dict, description="Engagement rate targets"
    )


class EmailMarketingConfig(BaseModel):
    """Configuration for email marketing."""

    send_limits: Dict[str, int] = Field(
        default_factory=lambda: {"hourly": 1000, "daily": 10000},
        description="Email sending limits",
    )

    template_categories: List[str] = Field(
        default_factory=lambda: [
            "welcome",
            "newsletter",
            "promotional",
            "transactional",
        ],
        description="Email template categories",
    )

    personalization_enabled: bool = Field(
        default=True, description="Enable email personalization"
    )
    ab_testing_enabled: bool = Field(
        default=True, description="Enable A/B testing for emails"
    )


class AnalyticsConfig(BaseModel):
    """Configuration for marketing analytics."""

    metrics_to_track: List[str] = Field(
        default_factory=lambda: [
            "conversion_rate",
            "click_through_rate",
            "engagement_rate",
            "cost_per_acquisition",
            "return_on_ad_spend",
        ],
        description="Metrics to track",
    )

    reporting_frequency: str = Field(default="daily", description="Reporting frequency")
    dashboard_enabled: bool = Field(
        default=True, description="Enable analytics dashboard"
    )
    real_time_monitoring: bool = Field(
        default=True, description="Enable real-time monitoring"
    )
