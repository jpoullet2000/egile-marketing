"""
A/B Test Manager for managing marketing A/B tests.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from ..client import AzureOpenAIClient
from ..config import AzureOpenAIConfig
from ..exceptions import ABTestError


class ABTestManager:
    """A/B testing management tool for marketing campaigns."""

    def __init__(self, openai_client: Optional[AzureOpenAIClient] = None):
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )
        self._active_tests: Dict[str, Dict[str, Any]] = {}

    async def create_ab_test(
        self,
        test_name: str,
        variant_a: Dict[str, Any],
        variant_b: Dict[str, Any],
        success_metric: str,
        duration_days: int = 14,
    ) -> Dict[str, Any]:
        """Create a new A/B test."""
        try:
            test_id = f"test_{int(datetime.now().timestamp())}"
            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)

            test_config = {
                "test_id": test_id,
                "test_name": test_name,
                "variant_a": variant_a,
                "variant_b": variant_b,
                "success_metric": success_metric,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "status": "active",
                "results": None,
            }

            self._active_tests[test_id] = test_config

            return test_config

        except Exception as e:
            raise ABTestError(f"A/B test creation failed: {e}")

    async def analyze_test_results(
        self, test_id: str, results_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze A/B test results and provide insights."""
        try:
            if test_id not in self._active_tests:
                raise ABTestError(f"Test {test_id} not found")

            test = self._active_tests[test_id]

            prompt = f"""
            Analyze these A/B test results and provide insights:
            
            Test: {test["test_name"]}
            Success Metric: {test["success_metric"]}
            Results Data: {json.dumps(results_data, indent=2)}
            
            Provide:
            1. Statistical significance assessment
            2. Winner determination
            3. Confidence level
            4. Recommendations for next steps
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are an A/B testing and statistics expert.",
                },
                {"role": "user", "content": prompt},
            ]

            response = await self.openai_client.chat_completion(messages=messages)

            # Update test with results
            test["results"] = {
                "data": results_data,
                "analysis": response.choices[0].message.content,
                "analyzed_at": datetime.now().isoformat(),
            }
            test["status"] = "completed"

            return test["results"]

        except Exception as e:
            raise ABTestError(f"A/B test analysis failed: {e}")

    def get_test_status(self, test_id: str) -> Dict[str, Any]:
        """Get the status of an A/B test."""
        if test_id not in self._active_tests:
            raise ABTestError(f"Test {test_id} not found")

        return self._active_tests[test_id]

    def list_active_tests(self) -> List[Dict[str, Any]]:
        """List all active A/B tests."""
        return [
            test for test in self._active_tests.values() if test["status"] == "active"
        ]
