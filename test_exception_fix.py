"""
Simple test to verify the exception fix.
"""

import asyncio
from egile_marketing.exceptions import AzureOpenAIError


def test_exception_fix():
    """Test that AzureOpenAIError accepts the new parameters."""
    print("🧪 Testing Exception Fix")
    print("=" * 40)

    try:
        # Test the old way (should work)
        error1 = AzureOpenAIError("Test error message")
        print("✅ Basic AzureOpenAIError creation works")

        # Test with new parameters (this was failing before)
        error2 = AzureOpenAIError(
            "API error 500: Internal server error",
            status_code=500,
            request_id="req_123456789",
        )
        print("✅ AzureOpenAIError with status_code and request_id works")

        # Test with all parameters
        error3 = AzureOpenAIError(
            "Model error",
            model="gpt-4",
            status_code=400,
            request_id="req_987654321",
            operation="chat_completion",
        )
        print("✅ AzureOpenAIError with all parameters works")

        # Verify attributes are set correctly
        assert error2.status_code == 500
        assert error2.request_id == "req_123456789"
        assert error3.model == "gpt-4"
        assert error3.operation == "chat_completion"

        print("✅ All attributes are set correctly")
        print("\n🎉 Exception fix verified successfully!")
        return True

    except Exception as e:
        print(f"❌ Exception test failed: {e}")
        return False


def test_import_structure():
    """Test that imports work correctly."""
    print("\n📦 Testing Import Structure")
    print("=" * 40)

    try:
        # Test main imports
        from egile_marketing.exceptions import (
            EgileMarketingError,
            AzureOpenAIError,
            MCPServerError,
            MarketingAgentError,
        )

        print("✅ Main exception imports work")

        from egile_marketing.config import (
            AzureOpenAIConfig,
            MarketingServerConfig,
            MarketingAgentConfig,
        )

        print("✅ Configuration imports work")

        # Test creating a config without Azure credentials
        config = MarketingServerConfig(
            name="TestServer", description="Test server for validation"
        )
        print(f"✅ Config creation works: {config.name}")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


async def main():
    """Run the tests."""
    print("🔧 Egile Marketing - Exception Fix Verification")
    print("=" * 60)

    test1_result = test_exception_fix()
    test2_result = test_import_structure()

    print("\n" + "=" * 60)
    if test1_result and test2_result:
        print("✅ All tests passed! The exception fix is working correctly.")
        print("\nThe issue with AzureOpenAIError parameters has been resolved.")
        print("You can now use the marketing tools without this error.")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
