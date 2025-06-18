# Egile Marketing

🚀 **AI-powered marketing automation via MCP server tools**

Egile Marketing is a comprehensive Python package that provides intelligent marketing automation capabilities through Model Context Protocol (MCP) server tools. Built on Azure OpenAI and designed for enterprise marketing teams, it offers content generation, campaign management, analytics, and optimization tools.

## ✨ Features

### 🎯 Content Generation
- Multi-format content creation (emails, social posts, blogs, ads)
- Brand voice consistency and guidelines enforcement
- SEO optimization and keyword integration
- A/B variant generation for testing
- Content effectiveness scoring

### 📊 Campaign Management
- Multi-channel campaign creation and coordination
- Automated content generation for different audiences
- Performance tracking and optimization recommendations
- A/B testing framework
- Real-time campaign monitoring

### 🔍 Analytics & Insights
- Comprehensive performance reporting
- AI-powered insights and recommendations
- ROI analysis and cost optimization
- Audience behavior analysis
- Predictive analytics for campaign outcomes

### 🎪 Social Media Automation
- Platform-specific content optimization
- Hashtag strategy and optimization
- Optimal posting schedule recommendations
- Engagement tracking and analysis
- Multi-platform campaign coordination

### 📧 Email Marketing
- Personalized email content generation
- Subject line optimization
- Segmented campaign management
- Deliverability optimization
- Automated drip campaigns

### 🏆 Lead Management
- Intelligent lead scoring
- Customer segmentation
- Behavioral tracking
- Qualification automation
- Pipeline optimization

## 🚀 Quick Start

### Installation

```bash
pip install egile-marketing
```

### Basic Usage

```python
import asyncio
from egile_marketing import MarketingAgent
from egile_marketing.config import MarketingAgentConfig, AzureOpenAIConfig

async def main():
    # Configure Azure OpenAI
    openai_config = AzureOpenAIConfig.from_environment()
    
    # Initialize marketing agent
    agent_config = MarketingAgentConfig(
        openai_config=openai_config,
        brand_voice="professional",
        target_audiences=["SMB owners", "Marketing managers"]
    )
    
    agent = MarketingAgent(agent_config)
    
    # Generate marketing content
    content = await agent.generate_content(
        content_type="email",
        brief="Welcome email for new customers",
        target_audience="SMB owners",
        tone="friendly"
    )
    
    print(content['content'])
    await agent.close()

asyncio.run(main())
```

### MCP Server Setup

```python
from egile_marketing.server import create_marketing_server

async def run_server():
    server = await create_marketing_server(
        name="MyMarketingServer",
        host="localhost",
        port=8000
    )
    await server.run()
```

## 🛠️ Configuration

### Environment Variables

Set up your Azure OpenAI credentials:

```bash
export AZURE_OPENAI_ENDPOINT="your-endpoint"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
export AZURE_KEY_VAULT_URL="your-keyvault-url"  # Optional
export AZURE_OPENAI_API_KEY_SECRET_NAME="openai-key"  # Optional
export AZURE_USE_MANAGED_IDENTITY="true"  # For Azure-hosted environments
```

### Configuration Classes

```python
from egile_marketing.config import (
    MarketingAgentConfig,
    MarketingServerConfig,
    ContentGenerationConfig
)

# Customize content generation
content_config = ContentGenerationConfig(
    model="gpt-4",
    temperature=0.7,
    seo_optimization=True,
    brand_guidelines_enabled=True
)

# Configure marketing agent
agent_config = MarketingAgentConfig(
    name="MyMarketingAgent",
    brand_voice="professional",
    content_types=["email", "social_media", "blog_post"],
    target_audiences=["Enterprise", "SMB", "Startups"]
)
```

## 🔧 Available Tools

### Content Generator
```python
from egile_marketing.tools import ContentGenerator
from egile_marketing.tools.content_generator import ContentRequest

generator = ContentGenerator()
request = ContentRequest(
    content_type="social_media",
    brief="Promote our new feature",
    target_audience="Tech professionals",
    keywords=["innovation", "productivity"]
)

result = await generator.generate_content(request)
```

### Social Media Manager
```python
from egile_marketing.tools import SocialMediaManager

sm_manager = SocialMediaManager()

# Create a post
post = await sm_manager.create_post(
    platform="linkedin",
    content_brief="Share industry insights",
    target_audience="Marketing professionals"
)

# Create a campaign
campaign = await sm_manager.create_campaign(
    name="Product Launch",
    platforms=["twitter", "linkedin"],
    content_brief="Announce new product",
    target_audience="B2B customers"
)
```

### Email Campaign Manager
```python
from egile_marketing.tools import EmailCampaignManager

email_manager = EmailCampaignManager()

campaign = await email_manager.create_campaign(
    name="Welcome Series",
    content_brief="Onboard new customers",
    target_segments=["new_customers"],
    campaign_type="welcome"
)
```

### Analytics Reporter
```python
from egile_marketing.tools import AnalyticsReporter

reporter = AnalyticsReporter()

report = await reporter.generate_performance_report(
    campaign_data=campaign_metrics,
    time_period="last_30_days"
)
```

## 🏗️ Architecture

Egile Marketing is built on a modular architecture:

```
egile_marketing/
├── client.py              # Azure OpenAI client with marketing optimizations
├── agent.py               # Intelligent marketing agent
├── mcp_server.py          # MCP server constructor for marketing tools
├── config.py              # Configuration management
├── exceptions.py          # Custom exceptions
├── server.py              # Main server entry point
└── tools/                 # Individual marketing tools
    ├── content_generator.py
    ├── social_media_manager.py
    ├── email_campaign_manager.py
    ├── seo_optimizer.py
    ├── analytics_reporter.py
    ├── lead_scorer.py
    ├── customer_segmenter.py
    └── ab_test_manager.py
```

## 🔗 MCP Server Integration

Use as an MCP server to integrate with other AI systems:

```bash
# Start the marketing MCP server
egile-marketing-server --host localhost --port 8000
```

The server exposes marketing tools as MCP functions that can be called by AI assistants and other systems.

## 📚 Examples

Check out the `examples/` directory for comprehensive usage examples:

- `basic_usage.py` - Getting started with core features
- `campaign_automation.py` - Full campaign automation workflow
- `content_optimization.py` - Content generation and optimization
- `analytics_reporting.py` - Performance analysis and reporting

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: jeanbaptistepoullet@gmail.com
- 💬 Issues: [GitHub Issues](https://github.com/your-org/egile-marketing/issues)
- 📖 Documentation: [Full Documentation](https://egile-marketing.readthedocs.io)

## 🎯 Roadmap

- [ ] Integration with major marketing platforms (HubSpot, Salesforce, etc.)
- [ ] Advanced ML models for predictive analytics
- [ ] Real-time personalization engine
- [ ] Multi-language content generation
- [ ] Advanced A/B testing statistical analysis
- [ ] Automated campaign optimization
- [ ] Voice and video content generation
- [ ] Advanced customer journey mapping

---

**Built with ❤️ for modern marketing teams**