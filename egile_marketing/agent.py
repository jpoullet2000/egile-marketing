"""
Marketing Agent for intelligent marketing automation and campaign management.

This agent provides intelligent routing and execution of marketing tasks
across different MCP servers and tools, optimized for marketing workflows.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

import structlog

from .client import AzureOpenAIClient
from .config import MarketingAgentConfig, AzureOpenAIConfig
from .exceptions import MarketingAgentError, AzureOpenAIError


logger = structlog.get_logger(__name__)


class MarketingAgent:
    """
    Intelligent marketing automation agent.

    Features:
    - Intelligent task routing to appropriate marketing tools
    - Context-aware content generation
    - Campaign optimization and management
    - Multi-channel marketing coordination
    - Performance analysis and insights
    - Automated A/B testing
    - Lead scoring and segmentation
    """

    def __init__(
        self,
        config: Optional[MarketingAgentConfig] = None,
        openai_config: Optional[AzureOpenAIConfig] = None,
    ):
        """
        Initialize the marketing agent.

        Args:
            config: Marketing agent configuration
            openai_config: Azure OpenAI configuration
        """
        self.config = config or MarketingAgentConfig(
            openai_config=openai_config or AzureOpenAIConfig.from_environment()
        )

        self.openai_client = AzureOpenAIClient(self.config.openai_config)
        self._task_cache: Dict[str, Any] = {}
        self._performance_history: List[Dict[str, Any]] = []
        self._active_campaigns: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initializing Marketing Agent",
            agent_name=self.config.name,
            content_types=self.config.content_types,
            target_audiences=self.config.target_audiences,
        )

    async def generate_content(
        self,
        content_type: str,
        brief: str,
        target_audience: str,
        tone: Optional[str] = None,
        length: str = "medium",
        keywords: Optional[List[str]] = None,
        brand_guidelines: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Generate marketing content using AI.

        Args:
            content_type: Type of content to generate
            brief: Content brief and requirements
            target_audience: Target audience description
            tone: Desired tone (defaults to config brand_voice)
            length: Content length
            keywords: SEO keywords to include
            brand_guidelines: Brand guidelines to follow

        Returns:
            Generated content with metadata
        """
        try:
            tone = tone or self.config.brand_voice

            # Build context-aware prompt
            system_prompt = self._build_content_generation_prompt(
                content_type, target_audience, tone, brand_guidelines
            )

            user_prompt = self._build_user_content_prompt(brief, length, keywords)

            logger.info(
                "Generating marketing content",
                content_type=content_type,
                target_audience=target_audience,
                tone=tone,
            )

            # Generate content using OpenAI
            content = await self.openai_client.generate_marketing_content(
                content_type=content_type,
                brief=brief,
                target_audience=target_audience,
                tone=tone,
                length=length,
                # Use client's default model
            )

            # Score content effectiveness
            content_score = await self.openai_client.score_content_effectiveness(
                content=content,
                content_type=content_type,
                target_audience=target_audience,
                # Use client's default model
            )

            result = {
                "content": content,
                "content_type": content_type,
                "target_audience": target_audience,
                "tone": tone,
                "length": length,
                "keywords": keywords or [],
                "effectiveness_score": content_score,
                "generated_at": datetime.now().isoformat(),
                "agent_version": "1.0",
            }

            # Cache result for optimization
            cache_key = f"{content_type}_{target_audience}_{tone}"
            self._task_cache[cache_key] = result

            return result

        except Exception as e:
            logger.error(
                "Content generation failed", error=str(e), content_type=content_type
            )
            raise MarketingAgentError(
                f"Content generation failed: {e}",
                agent_name=self.config.name,
                operation="generate_content",
            )

    async def create_campaign(
        self,
        campaign_name: str,
        campaign_type: str,
        target_segments: List[str],
        content_brief: str,
        budget: Optional[float] = None,
        duration_days: int = 30,
        channels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create and set up a marketing campaign.

        Args:
            campaign_name: Name of the campaign
            campaign_type: Type of campaign
            target_segments: Target customer segments
            content_brief: Content requirements
            budget: Campaign budget
            duration_days: Campaign duration
            channels: Marketing channels to use

        Returns:
            Campaign configuration and assets
        """
        try:
            campaign_id = f"camp_{int(datetime.now().timestamp())}"
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)

            channels = channels or ["email", "social_media"]

            logger.info(
                "Creating marketing campaign",
                campaign_name=campaign_name,
                campaign_type=campaign_type,
                channels=channels,
            )

            # Generate content for each channel and segment
            campaign_assets = {}
            for channel in channels:
                channel_assets = {}
                for segment in target_segments:
                    content = await self.generate_content(
                        content_type=channel,
                        brief=content_brief,
                        target_audience=segment,
                        tone=self.config.brand_voice,
                    )
                    channel_assets[segment] = content
                campaign_assets[channel] = channel_assets

            # Create campaign configuration
            campaign_config = {
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "campaign_type": campaign_type,
                "target_segments": target_segments,
                "channels": channels,
                "budget": budget,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "duration_days": duration_days,
                "status": "draft",
                "assets": campaign_assets,
                "created_at": datetime.now().isoformat(),
                "created_by": self.config.name,
            }

            # Store campaign
            self._active_campaigns[campaign_id] = campaign_config

            return campaign_config

        except Exception as e:
            logger.error(
                "Campaign creation failed", error=str(e), campaign_name=campaign_name
            )
            raise MarketingAgentError(
                f"Campaign creation failed: {e}",
                agent_name=self.config.name,
                operation="create_campaign",
            )

    async def optimize_campaign(
        self, campaign_id: str, performance_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize an existing campaign based on performance data.

        Args:
            campaign_id: ID of campaign to optimize
            performance_data: Current performance metrics

        Returns:
            Optimization recommendations and updated assets
        """
        try:
            if campaign_id not in self._active_campaigns:
                raise MarketingAgentError(f"Campaign {campaign_id} not found")

            campaign = self._active_campaigns[campaign_id]

            logger.info(
                "Optimizing marketing campaign",
                campaign_id=campaign_id,
                campaign_name=campaign["campaign_name"],
            )

            # Analyze performance using AI
            analysis_prompt = f"""
            Analyze the following marketing campaign performance data and provide optimization recommendations:

            Campaign: {campaign["campaign_name"]}
            Type: {campaign["campaign_type"]}
            Channels: {", ".join(campaign["channels"])}
            Target Segments: {", ".join(campaign["target_segments"])}

            Performance Data:
            {json.dumps(performance_data, indent=2)}

            Provide specific, actionable recommendations for:
            1. Content optimization
            2. Audience targeting
            3. Channel performance
            4. Budget allocation
            5. A/B testing opportunities
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are a marketing optimization expert. Provide data-driven recommendations.",
                },
                {"role": "user", "content": analysis_prompt},
            ]

            response = await self.openai_client.chat_completion(
                messages=messages,
                # Use client's default model
                temperature=0.3,
            )

            optimization_recommendations = response.choices[0].message.content

            # Update campaign with optimization data
            campaign["optimization_history"] = campaign.get("optimization_history", [])
            campaign["optimization_history"].append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "performance_data": performance_data,
                    "recommendations": optimization_recommendations,
                }
            )

            return {
                "campaign_id": campaign_id,
                "recommendations": optimization_recommendations,
                "performance_data": performance_data,
                "optimized_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(
                "Campaign optimization failed", error=str(e), campaign_id=campaign_id
            )
            raise MarketingAgentError(
                f"Campaign optimization failed: {e}",
                agent_name=self.config.name,
                operation="optimize_campaign",
            )

    async def analyze_audience_sentiment(
        self, content: str, audience_feedback: List[str], platform: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze audience sentiment for content.

        Args:
            content: Marketing content to analyze
            audience_feedback: List of audience comments/feedback
            platform: Platform where content was published

        Returns:
            Sentiment analysis and insights
        """
        try:
            analysis_prompt = f"""
            Analyze the sentiment and engagement for the following marketing content:

            Content: {content}
            Platform: {platform}

            Audience Feedback:
            {chr(10).join(f"- {feedback}" for feedback in audience_feedback)}

            Provide analysis on:
            1. Overall sentiment (positive/negative/neutral percentages)
            2. Key themes in feedback
            3. Engagement quality indicators
            4. Suggestions for improvement
            5. Content performance score (1-10)
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are a social media and content marketing analyst expert.",
                },
                {"role": "user", "content": analysis_prompt},
            ]

            response = await self.openai_client.chat_completion(
                messages=messages, temperature=0.2
            )

            return {
                "content": content,
                "platform": platform,
                "feedback_count": len(audience_feedback),
                "analysis": response.choices[0].message.content,
                "analyzed_at": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise MarketingAgentError(
                f"Sentiment analysis failed: {e}",
                agent_name=self.config.name,
                operation="analyze_sentiment",
            )

    def _build_content_generation_prompt(
        self,
        content_type: str,
        target_audience: str,
        tone: str,
        brand_guidelines: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build system prompt for content generation."""
        guidelines_text = ""
        if brand_guidelines:
            guidelines_text = (
                f"\\nBrand Guidelines: {json.dumps(brand_guidelines, indent=2)}"
            )

        return f"""You are an expert marketing copywriter specializing in {content_type} content.

Target Audience: {target_audience}
Tone: {tone}
{guidelines_text}

Create compelling, conversion-focused content that:
- Resonates with the target audience
- Maintains the specified tone
- Follows marketing best practices
- Includes clear calls-to-action when appropriate
- Is optimized for engagement and conversion"""

    def _build_user_content_prompt(
        self, brief: str, length: str, keywords: Optional[List[str]] = None
    ) -> str:
        """Build user prompt for content generation."""
        keywords_text = ""
        if keywords:
            keywords_text = f"\\nSEO Keywords to include: {', '.join(keywords)}"

        return f"""Content Brief: {brief}

Length: {length}
{keywords_text}

Please create engaging, high-quality content that meets these requirements."""

    async def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get metrics for a specific campaign."""
        if campaign_id not in self._active_campaigns:
            raise MarketingAgentError(f"Campaign {campaign_id} not found")

        campaign = self._active_campaigns[campaign_id]

        # This would integrate with your analytics system
        return {
            "campaign_id": campaign_id,
            "campaign_name": campaign["campaign_name"],
            "status": campaign["status"],
            "metrics": {
                "impressions": 10000,
                "clicks": 250,
                "conversions": 15,
                "cost_per_click": 2.50,
                "conversion_rate": 0.06,
            },
            "retrieved_at": datetime.now().isoformat(),
        }

    async def close(self):
        """Clean up resources."""
        await self.openai_client.close()
        logger.info("Marketing Agent closed")
