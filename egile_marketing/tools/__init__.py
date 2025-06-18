"""
Marketing tools and utilities for the Egile Marketing package.

This module provides specialized marketing tools that can be used
independently or integrated into MCP servers.
"""

from .content_generator import ContentGenerator
from .social_media_manager import SocialMediaManager
from .email_campaign_manager import EmailCampaignManager
from .seo_optimizer import SEOOptimizer
from .analytics_reporter import AnalyticsReporter
from .lead_scorer import LeadScorer
from .customer_segmenter import CustomerSegmenter
from .ab_test_manager import ABTestManager

__all__ = [
    "ContentGenerator",
    "SocialMediaManager",
    "EmailCampaignManager",
    "SEOOptimizer",
    "AnalyticsReporter",
    "LeadScorer",
    "CustomerSegmenter",
    "ABTestManager",
]
