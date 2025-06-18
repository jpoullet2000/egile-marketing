"""
Email Campaign Manager for creating and managing email marketing campaigns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from ..client import AzureOpenAIClient
from ..config import EmailMarketingConfig, AzureOpenAIConfig
from ..exceptions import EmailCampaignError


@dataclass
class EmailCampaign:
    """Structure for email campaigns."""

    campaign_id: str
    name: str
    subject_line: str
    content: str
    recipient_segments: List[str]
    send_date: Optional[str] = None
    status: str = "draft"


class EmailCampaignManager:
    """Email marketing campaign management tool."""

    def __init__(
        self,
        openai_client: Optional[AzureOpenAIClient] = None,
        config: Optional[EmailMarketingConfig] = None,
    ):
        self.config = config or EmailMarketingConfig()
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )
        self._campaigns: Dict[str, EmailCampaign] = {}

    async def create_campaign(
        self,
        name: str,
        content_brief: str,
        target_segments: List[str],
        campaign_type: str = "newsletter",
    ) -> EmailCampaign:
        """Create an email campaign."""
        try:
            campaign_id = f"email_{int(datetime.now().timestamp())}"

            # Generate subject line and content
            subject_line = await self._generate_subject_line(
                content_brief, campaign_type
            )
            content = await self._generate_email_content(content_brief, campaign_type)

            campaign = EmailCampaign(
                campaign_id=campaign_id,
                name=name,
                subject_line=subject_line,
                content=content,
                recipient_segments=target_segments,
            )

            self._campaigns[campaign_id] = campaign
            return campaign

        except Exception as e:
            raise EmailCampaignError(f"Failed to create email campaign: {e}")

    async def _generate_subject_line(self, brief: str, campaign_type: str) -> str:
        """Generate email subject line."""
        prompt = f"Create an engaging email subject line for a {campaign_type} about: {brief}"

        messages = [
            {"role": "system", "content": "You are an email marketing expert."},
            {"role": "user", "content": prompt},
        ]

        response = await self.openai_client.chat_completion(messages=messages)
        return response.choices[0].message.content.strip()

    async def _generate_email_content(self, brief: str, campaign_type: str) -> str:
        """Generate email content."""
        prompt = f"Create engaging email content for a {campaign_type} campaign about: {brief}"

        messages = [
            {"role": "system", "content": "You are an email marketing content expert."},
            {"role": "user", "content": prompt},
        ]

        response = await self.openai_client.chat_completion(messages=messages)
        return response.choices[0].message.content

    def get_campaign_metrics(self, campaign_id: str) -> Dict[str, Any]:
        """Get email campaign metrics."""
        if campaign_id not in self._campaigns:
            raise EmailCampaignError(f"Campaign {campaign_id} not found")

        return {
            "campaign_id": campaign_id,
            "open_rate": 0.25,
            "click_rate": 0.05,
            "conversion_rate": 0.02,
            "unsubscribe_rate": 0.001,
        }
