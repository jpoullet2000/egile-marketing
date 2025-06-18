"""
Customer Segmenter for segmenting customers for targeted marketing.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..client import AzureOpenAIClient
from ..config import AzureOpenAIConfig
from ..exceptions import SegmentationError


class CustomerSegmenter:
    """Customer segmentation tool for targeted marketing."""

    def __init__(self, openai_client: Optional[AzureOpenAIClient] = None):
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )

    async def create_segments(
        self, customer_data: List[Dict[str, Any]], segmentation_criteria: List[str]
    ) -> Dict[str, Any]:
        """Create customer segments based on criteria."""
        try:
            # Analyze customer data for segmentation
            prompt = f"""
            Analyze this customer data and create meaningful segments based on: {", ".join(segmentation_criteria)}
            
            Customer data sample: {str(customer_data[:5])}  # First 5 customers
            Total customers: {len(customer_data)}
            
            Suggest 3-5 distinct customer segments with characteristics and marketing recommendations.
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are a customer segmentation expert.",
                },
                {"role": "user", "content": prompt},
            ]

            response = await self.openai_client.chat_completion(messages=messages)

            # Mock segment assignment (would use ML in production)
            segments = self._assign_segments(customer_data)

            return {
                "segments": segments,
                "analysis": response.choices[0].message.content,
                "criteria_used": segmentation_criteria,
                "total_customers": len(customer_data),
                "created_at": datetime.now().isoformat(),
            }

        except Exception as e:
            raise SegmentationError(f"Customer segmentation failed: {e}")

    def _assign_segments(
        self, customer_data: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Assign customers to segments (simplified logic)."""
        segments = {
            "high_value": [],
            "growth_potential": [],
            "at_risk": [],
            "new_customers": [],
        }

        for customer in customer_data:
            customer_id = customer.get("id", "unknown")
            value = customer.get("lifetime_value", 0)

            if value > 1000:
                segments["high_value"].append(customer_id)
            elif value > 500:
                segments["growth_potential"].append(customer_id)
            elif value < 100:
                segments["new_customers"].append(customer_id)
            else:
                segments["at_risk"].append(customer_id)

        return segments
