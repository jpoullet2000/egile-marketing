"""
Demo script for Egile Marketing package.

This script demonstrates the basic functionality without requiring
Azure OpenAI credentials for initial testing.
"""

import asyncio
from datetime import datetime


def demo_content_generator():
    """Demo the content generator (mock implementation)."""
    print("🎯 Content Generator Demo")
    print("=" * 40)

    # Mock content generation
    content_types = ["email", "social_media", "blog_post", "ad_copy"]

    for content_type in content_types:
        print(f"\\n📝 Generating {content_type} content...")
        print(f"   Target Audience: Marketing professionals")
        print(f"   Tone: Professional")
        print(f"   Generated: Mock {content_type} content for demo")
        print(f"   SEO Score: 85/100")
        print(f"   Effectiveness Score: 9.2/10")


def demo_campaign_manager():
    """Demo the campaign management features."""
    print("\\n📊 Campaign Manager Demo")
    print("=" * 40)

    campaign_data = {
        "campaign_id": f"camp_{int(datetime.now().timestamp())}",
        "name": "AI Marketing Platform Launch",
        "type": "product_launch",
        "channels": ["email", "social_media", "ppc"],
        "target_segments": ["SMB owners", "Marketing managers"],
        "budget": 10000.0,
        "duration_days": 30,
        "status": "active",
    }

    print(f"📈 Campaign Created:")
    for key, value in campaign_data.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")

    # Mock performance metrics
    print(f"\\n📊 Campaign Performance (Mock Data):")
    print(f"   Impressions: 125,000")
    print(f"   Clicks: 3,750")
    print(f"   Conversions: 225")
    print(f"   CTR: 3.0%")
    print(f"   Conversion Rate: 6.0%")
    print(f"   ROI: 320%")


def demo_social_media_tools():
    """Demo social media management features."""
    print("\\n📱 Social Media Manager Demo")
    print("=" * 40)

    platforms = ["Twitter", "LinkedIn", "Facebook", "Instagram"]

    for platform in platforms:
        print(f"\\n🌐 {platform} Optimization:")
        print(f"   Content: Mock {platform.lower()} post content")
        print(f"   Hashtags: #marketing #AI #automation")
        print(f"   Best Time: 2:00 PM - 4:00 PM")
        print(f"   Engagement Prediction: High")


def demo_analytics_insights():
    """Demo analytics and insights features."""
    print("\\n📈 Analytics & Insights Demo")
    print("=" * 40)

    metrics = {
        "Conversion Rate": "4.5% (↑15% vs last month)",
        "Click-Through Rate": "2.8% (↑8% vs last month)",
        "Engagement Rate": "6.7% (↑22% vs last month)",
        "Cost Per Acquisition": "$125.50 (↓12% vs last month)",
        "Return on Ad Spend": "3.2x (↑18% vs last month)",
    }

    print("📊 Key Performance Indicators:")
    for metric, value in metrics.items():
        print(f"   {metric}: {value}")

    print("\\n🔍 AI Insights:")
    print("   • Email campaigns show 22% higher engagement on Tuesdays")
    print("   • LinkedIn content performs 35% better with industry hashtags")
    print("   • Video content generates 3x more leads than static images")
    print("   • Personalized subject lines increase open rates by 18%")


def demo_lead_scoring():
    """Demo lead scoring functionality."""
    print("\\n🎯 Lead Scoring Demo")
    print("=" * 40)

    leads = [
        {
            "company": "TechCorp Inc",
            "size": 250,
            "engagement": 85,
            "score": 92,
            "status": "Hot",
        },
        {
            "company": "StartupXYZ",
            "size": 15,
            "engagement": 65,
            "score": 73,
            "status": "Warm",
        },
        {
            "company": "Enterprise Co",
            "size": 1000,
            "engagement": 45,
            "score": 68,
            "status": "Cold",
        },
    ]

    print("📋 Lead Scoring Results:")
    for lead in leads:
        print(f"   {lead['company']}:")
        print(f"     Company Size: {lead['size']} employees")
        print(f"     Engagement Score: {lead['engagement']}/100")
        print(f"     Overall Score: {lead['score']}/100")
        print(f"     Status: {lead['status']}")
        print()


def demo_ab_testing():
    """Demo A/B testing capabilities."""
    print("🧪 A/B Testing Demo")
    print("=" * 40)

    test_data = {
        "test_name": "Email Subject Line Test",
        "variant_a": "Boost Your Marketing ROI by 50%",
        "variant_b": "Transform Your Marketing Strategy Today",
        "sample_size": 2000,
        "duration": "7 days",
        "winner": "Variant B",
        "confidence": "95%",
        "improvement": "+23% open rate",
    }

    print(f"🔬 A/B Test Results:")
    for key, value in test_data.items():
        print(f"   {key.replace('_', ' ').title()}: {value}")


def demo_mcp_server_info():
    """Demo MCP server information."""
    print("\\n🔌 MCP Server Demo")
    print("=" * 40)

    tools = [
        "generate_content - Generate marketing content using AI",
        "manage_campaign - Create and manage marketing campaigns",
        "get_analytics - Get marketing analytics and insights",
        "score_lead - Score and qualify leads",
        "optimize_content - Optimize content for better performance",
        "schedule_social_posts - Schedule social media posts",
        "segment_customers - Segment customers for targeting",
        "run_ab_test - Create and analyze A/B tests",
    ]

    print("🛠️  Available MCP Tools:")
    for tool in tools:
        tool_name, description = tool.split(" - ")
        print(f"   • {tool_name}: {description}")

    print("\\n🌐 Server Configuration:")
    print("   Host: localhost")
    print("   Port: 8000")
    print("   Status: Ready")
    print("   Tools Registered: 8")


async def main():
    """Run the demo."""
    print("🚀 Egile Marketing - Package Demo")
    print("=" * 60)
    print("This demo showcases the capabilities of the Egile Marketing package")
    print("without requiring Azure OpenAI credentials.")
    print("=" * 60)

    demo_content_generator()
    demo_campaign_manager()
    demo_social_media_tools()
    demo_analytics_insights()
    demo_lead_scoring()
    demo_ab_testing()
    demo_mcp_server_info()

    print("\\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\\nTo use the full functionality:")
    print("1. Set up Azure OpenAI credentials")
    print("2. Install the package: pip install egile-marketing")
    print("3. Run: python examples/basic_usage.py")
    print("4. Start MCP server: egile-marketing-server")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
