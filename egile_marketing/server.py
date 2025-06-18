"""
Main server entry point for Egile Marketing MCP server.

This module provides the main entry point for running the marketing MCP server
with all marketing tools enabled.
"""

import asyncio
import argparse
from pathlib import Path

import structlog

from .mcp_server import MarketingMCPServer
from .config import MarketingServerConfig
from .exceptions import EgileMarketingError


logger = structlog.get_logger(__name__)


async def create_marketing_server(
    name: str = "EgileMarketingServer", host: str = "localhost", port: int = 8000
) -> MarketingMCPServer:
    """
    Create a fully configured marketing MCP server.

    Args:
        name: Server name
        host: Server host
        port: Server port

    Returns:
        Configured marketing MCP server
    """
    config = MarketingServerConfig(
        name=name,
        description="Comprehensive marketing automation MCP server",
        host=host,
        port=port,
        capabilities=[
            "content_generation",
            "campaign_management",
            "social_media_automation",
            "email_marketing",
            "seo_optimization",
            "analytics_reporting",
            "lead_scoring",
            "customer_segmentation",
            "ab_testing",
        ],
    )

    server = MarketingMCPServer(config)

    # Add all marketing tools
    server.add_content_generation_tool()
    server.add_campaign_management_tool()
    server.add_analytics_tool()
    server.add_lead_scoring_tool()

    await server.build()

    logger.info(f"Marketing MCP server '{name}' created and configured")
    return server


async def main():
    """Main entry point for the marketing server."""
    parser = argparse.ArgumentParser(description="Egile Marketing MCP Server")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--name", default="EgileMarketingServer", help="Server name")

    args = parser.parse_args()

    try:
        server = await create_marketing_server(
            name=args.name, host=args.host, port=args.port
        )

        logger.info(f"Starting marketing server on {args.host}:{args.port}")
        await server.run()

    except Exception as e:
        logger.error(f"Failed to start marketing server: {e}")
        raise EgileMarketingError(f"Server startup failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
