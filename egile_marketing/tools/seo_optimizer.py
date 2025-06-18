"""
SEO Optimizer for improving search engine optimization of marketing content.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from ..client import AzureOpenAIClient
from ..config import AzureOpenAIConfig
from ..exceptions import SEOError


class SEOOptimizer:
    """SEO optimization tool for marketing content."""

    def __init__(self, openai_client: Optional[AzureOpenAIClient] = None):
        self.openai_client = openai_client or AzureOpenAIClient(
            AzureOpenAIConfig.from_environment()
        )

    async def optimize_content(
        self, content: str, target_keywords: List[str], content_type: str = "blog_post"
    ) -> Dict[str, Any]:
        """Optimize content for SEO."""
        try:
            prompt = f"""
            Optimize this {content_type} content for SEO with target keywords: {", ".join(target_keywords)}
            
            Original content: {content}
            
            Provide SEO-optimized version that naturally incorporates keywords.
            """

            messages = [
                {
                    "role": "system",
                    "content": "You are an SEO content optimization expert.",
                },
                {"role": "user", "content": prompt},
            ]

            response = await self.openai_client.chat_completion(messages=messages)
            optimized_content = response.choices[0].message.content

            # Calculate SEO metrics
            seo_score = self._calculate_seo_score(optimized_content, target_keywords)

            return {
                "original_content": content,
                "optimized_content": optimized_content,
                "target_keywords": target_keywords,
                "seo_score": seo_score,
                "optimized_at": datetime.now().isoformat(),
            }

        except Exception as e:
            raise SEOError(f"SEO optimization failed: {e}")

    def _calculate_seo_score(self, content: str, keywords: List[str]) -> Dict[str, Any]:
        """Calculate basic SEO score."""
        word_count = len(content.split())

        keyword_density = {}
        for keyword in keywords:
            count = content.lower().count(keyword.lower())
            density = count / word_count if word_count > 0 else 0
            keyword_density[keyword] = {"count": count, "density": round(density, 4)}

        overall_score = min(100, sum(k["count"] for k in keyword_density.values()) * 10)

        return {
            "overall_score": overall_score,
            "word_count": word_count,
            "keyword_density": keyword_density,
        }
