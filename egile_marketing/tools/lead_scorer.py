"""
Lead Scorer for scoring and qualifying marketing leads.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..client import AzureOpenAIClient
from ..config import AzureOpenAIConfig
from ..exceptions import LeadScoringError


class LeadScorer:
    """Lead scoring and qualification tool."""

    def __init__(self, openai_client: Optional[AzureOpenAIClient] = None):
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )

    async def score_lead(
        self,
        lead_data: Dict[str, Any],
        scoring_criteria: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Score a lead based on various factors."""
        try:
            # Default scoring criteria
            criteria = scoring_criteria or {
                "company_size": 0.3,
                "engagement_level": 0.4,
                "budget_fit": 0.2,
                "timeline": 0.1,
            }

            # Calculate base score
            base_score = self._calculate_base_score(lead_data, criteria)

            # Get AI-enhanced scoring
            ai_analysis = await self._get_ai_lead_analysis(lead_data)

            return {
                "lead_id": lead_data.get("id", "unknown"),
                "base_score": base_score,
                "ai_analysis": ai_analysis,
                "qualification": "qualified" if base_score >= 70 else "unqualified",
                "scored_at": datetime.now().isoformat(),
            }

        except Exception as e:
            raise LeadScoringError(f"Lead scoring failed: {e}")

    def _calculate_base_score(
        self, lead_data: Dict[str, Any], criteria: Dict[str, Any]
    ) -> int:
        """Calculate base lead score."""
        # Simplified scoring logic - would be more sophisticated in production
        score = 50  # Base score

        if lead_data.get("company_size", 0) > 100:
            score += 20

        if lead_data.get("engagement_score", 0) > 50:
            score += 25

        return min(100, score)

    async def _get_ai_lead_analysis(self, lead_data: Dict[str, Any]) -> str:
        """Get AI analysis of lead quality."""
        prompt = (
            f"Analyze this lead data and provide qualification insights: {lead_data}"
        )

        messages = [
            {"role": "system", "content": "You are a lead qualification expert."},
            {"role": "user", "content": prompt},
        ]

        response = await self.openai_client.chat_completion(messages=messages)
        return response.choices[0].message.content
