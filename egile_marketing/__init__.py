"""
Egile Marketing: AI-powered marketing automation via MCP server tools

A comprehensive Python package that provides:
- Marketing campaign automation
- Content generation and optimization
- Analytics and reporting tools
- Social media management
- Email marketing automation
- SEO optimization tools
- Lead generation and scoring
- Customer segmentation
- A/B testing framework
"""

__version__ = "0.1.0"
__author__ = "Jean-Baptiste Poullet"

# Core exports
from .client import AzureOpenAIClient
from .mcp_server import MarketingMCPServer, MarketingServerConfig
from .agent import MarketingAgent, MarketingAgentConfig
from .exceptions import (
    EgileMarketingError,
    AzureOpenAIError,
    MCPServerError,
    MarketingAgentError,
)

# Marketing tools exports
from .tools import (
    ContentGenerator,
    SocialMediaManager,
    EmailCampaignManager,
    SEOOptimizer,
    AnalyticsReporter,
    LeadScorer,
    CustomerSegmenter,
    ABTestManager,
)

__all__ = [
    "AzureOpenAIClient",
    "MarketingMCPServer",
    "MarketingServerConfig",
    "MarketingAgent",
    "MarketingAgentConfig",
    "EgileMarketingError",
    "AzureOpenAIError",
    "MCPServerError",
    "MarketingAgentError",
    "ContentGenerator",
    "SocialMediaManager",
    "EmailCampaignManager",
    "SEOOptimizer",
    "AnalyticsReporter",
    "LeadScorer",
    "CustomerSegmenter",
    "ABTestManager",
]
