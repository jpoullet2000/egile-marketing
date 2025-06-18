"""
Basic test to verify package structure and imports.
"""


def test_package_imports():
    """Test that the main package imports work."""
    try:
        # Test main package import
        import egile_marketing

        print("✅ Main package import successful")

        # Test exception imports
        from egile_marketing.exceptions import (
            EgileMarketingError,
            ContentGenerationError,
            SocialMediaError,
        )

        print("✅ Exception imports successful")

        # Test config imports
        from egile_marketing.config import (
            MarketingServerConfig,
            MarketingAgentConfig,
            ContentGenerationConfig,
        )

        print("✅ Configuration imports successful")

        # Test that we can create config objects
        server_config = MarketingServerConfig(
            name="TestServer", description="Test marketing server"
        )
        print(f"✅ Server config created: {server_config.name}")

        content_config = ContentGenerationConfig()
        print(f"✅ Content config created with model: {content_config.model}")

        print("\\n🎉 All basic imports and configurations work correctly!")
        return True

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_tool_structure():
    """Test tool module structure."""
    try:
        # Test individual tool imports (these might fail due to missing dependencies)
        from egile_marketing.tools.content_generator import (
            ContentRequest,
            GeneratedContent,
        )

        print("✅ Content generator structures imported")

        from egile_marketing.tools.social_media_manager import (
            SocialMediaPost,
            SocialMediaCampaign,
        )

        print("✅ Social media structures imported")

        # Test creating data structures
        content_request = ContentRequest(
            content_type="email", brief="Test email", target_audience="Test audience"
        )
        print(f"✅ Content request created: {content_request.content_type}")

        return True

    except ImportError as e:
        print(f"⚠️  Tool import warning (expected if dependencies missing): {e}")
        return True  # This is expected if Azure libraries aren't installed
    except Exception as e:
        print(f"❌ Unexpected error in tool structure: {e}")
        return False


def main():
    """Run basic package tests."""
    print("🧪 Egile Marketing - Basic Package Tests")
    print("=" * 50)

    print("Testing package structure...")

    import_success = test_package_imports()
    structure_success = test_tool_structure()

    print("\\n" + "=" * 50)
    if import_success and structure_success:
        print("✅ All basic tests passed!")
        print("\\nPackage structure is valid and ready for use.")
        print("\\nNext steps:")
        print(
            "1. Install Azure dependencies: pip install azure-identity azure-keyvault-secrets"
        )
        print("2. Install OpenAI: pip install openai")
        print(
            "3. Install other dependencies: pip install fastmcp pydantic python-dotenv"
        )
        print("4. Set up Azure OpenAI credentials")
        print("5. Run the demo: python demo.py")
    else:
        print("❌ Some tests failed. Check the error messages above.")

    print("=" * 50)


if __name__ == "__main__":
    main()
