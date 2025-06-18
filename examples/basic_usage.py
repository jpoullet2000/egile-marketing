"""
Basic usage example for Egile Marketing package.

This example demonstrates how to use the marketing tools
for content generation and campaign management.
"""

import asyncio
from egile_marketing import MarketingAgent, ContentGenerator
from egile_marketing.config import MarketingAgentConfig, AzureOpenAIConfig
from egile_marketing.tools.content_generator import ContentRequest


async def content_generation_example():
    """Example of using the content generator."""
    print("🎯 Content Generation Example")
    print("=" * 50)

    try:
        # Initialize content generator
        content_generator = ContentGenerator()

        # Create content request
        request = ContentRequest(
            content_type="social_media",
            brief="Promote our new AI-powered marketing automation platform",
            target_audience="Marketing professionals and small business owners",
            tone="professional",
            length="short",
            keywords=["marketing automation", "AI", "efficiency"],
        )

        # Generate content
        print("Generating social media content...")
        result = await content_generator.generate_content(request)

        print(f"Content Type: {result.content_type}")
        print(f"Target Audience: {result.target_audience}")
        print(f"Tone: {result.tone}")
        print(f"Generated Content:")
        print("-" * 30)
        print(result.content)
        print("-" * 30)
        print(f"Keywords used: {', '.join(result.keywords)}")

        if result.seo_metrics:
            print(f"SEO Score: {result.seo_metrics.get('seo_score', 'N/A')}")

    except Exception as e:
        print(f"Error in content generation: {e}")


async def marketing_agent_example():
    """Example of using the marketing agent."""
    print("\\n🤖 Marketing Agent Example")
    print("=" * 50)

    try:
        # Configure Azure OpenAI (you'll need to set up environment variables)
        openai_config = AzureOpenAIConfig.from_environment()

        # Configure marketing agent
        agent_config = MarketingAgentConfig(
            openai_config=openai_config,
            name="ExampleMarketingAgent",
            brand_voice="professional",
            target_audiences=["SMB owners", "Marketing managers"],
        )

        # Initialize marketing agent
        agent = MarketingAgent(agent_config)

        # Generate marketing content
        print("Creating marketing campaign...")
        campaign = await agent.create_campaign(
            campaign_name="AI Marketing Platform Launch",
            campaign_type="product_launch",
            target_segments=["SMB owners", "Marketing managers"],
            content_brief="Launch campaign for new AI marketing automation platform",
            budget=10000.0,
            duration_days=30,
            channels=["email", "social_media"],
        )

        print(f"Campaign ID: {campaign['campaign_id']}")
        print(f"Campaign Name: {campaign['campaign_name']}")
        print(f"Channels: {', '.join(campaign['channels'])}")
        print(f"Target Segments: {', '.join(campaign['target_segments'])}")
        print(f"Duration: {campaign['duration_days']} days")

        # Generate content for different audiences
        print("\\nGenerating personalized content...")
        for segment in campaign["target_segments"]:
            content = await agent.generate_content(
                content_type="email",
                brief="Welcome email for new AI marketing platform",
                target_audience=segment,
                tone="friendly",
            )

            print(f"\\nContent for {segment}:")
            print("-" * 30)
            print(
                content["content"][:200] + "..."
                if len(content["content"]) > 200
                else content["content"]
            )

        await agent.close()

    except Exception as e:
        print(f"Error in marketing agent example: {e}")


async def campaign_optimization_example():
    """Example of campaign optimization."""
    print("\\n📊 Campaign Optimization Example")
    print("=" * 50)

    try:
        # Mock performance data
        performance_data = {
            "email_campaign": {
                "open_rate": 0.18,
                "click_rate": 0.03,
                "conversion_rate": 0.015,
                "unsubscribe_rate": 0.002,
            },
            "social_media": {
                "engagement_rate": 0.045,
                "reach": 15000,
                "clicks": 450,
                "conversions": 25,
            },
        }

        # Configure and initialize agent
        openai_config = AzureOpenAIConfig.from_environment()
        agent_config = MarketingAgentConfig(openai_config=openai_config)
        agent = MarketingAgent(agent_config)

        # Create a campaign first
        campaign = await agent.create_campaign(
            campaign_name="Optimization Test Campaign",
            campaign_type="engagement",
            target_segments=["Tech enthusiasts"],
            content_brief="Test campaign for optimization",
            duration_days=7,
        )

        # Optimize the campaign
        print(
            "Analyzing campaign performance and generating optimization recommendations..."
        )
        optimization = await agent.optimize_campaign(
            campaign_id=campaign["campaign_id"], performance_data=performance_data
        )

        print(f"Campaign optimized: {optimization['campaign_id']}")
        print("Optimization Recommendations:")
        print("-" * 40)
        print(
            optimization["recommendations"][:500] + "..."
            if len(optimization["recommendations"]) > 500
            else optimization["recommendations"]
        )

        await agent.close()

    except Exception as e:
        print(f"Error in campaign optimization: {e}")


async def main():
    """Run all examples."""
    print("🚀 Egile Marketing - Basic Usage Examples")
    print("=" * 60)

    await content_generation_example()
    await marketing_agent_example()
    await campaign_optimization_example()

    print("\\n✅ Examples completed!")
    print("\\nNext steps:")
    print("1. Set up your Azure OpenAI credentials in environment variables")
    print("2. Customize the configuration for your specific needs")
    print("3. Integrate with your existing marketing systems")
    print("4. Explore the MCP server capabilities for tool integration")


if __name__ == "__main__":
    asyncio.run(main())
