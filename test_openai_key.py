#!/usr/bin/env python3
"""
Test script to verify OpenAI API key configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openai_key():
    """Test if OpenAI API key is configured and working"""
    
    # Check if key exists
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY is NOT set in environment variables")
        print("\nTo fix this:")
        print("1. Create a .env file in the project root")
        print("2. Add: OPENAI_API_KEY=your_actual_key_here")
        print("3. Restart the backend server")
        return False
    
    # Mask the key for security (show first 7 and last 4 characters)
    masked_key = f"{api_key[:7]}...{api_key[-4:]}" if len(api_key) > 11 else "***"
    print(f"✅ OPENAI_API_KEY is set: {masked_key}")
    
    # Try to initialize OpenAI client
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI client initialized successfully")
        
        # Try a simple API call
        print("\n🔄 Testing API connection with a simple request...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✅ API call successful! Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI API: {e}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- Network connectivity issues")
        print("- OpenAI service is down")
        print("- Insufficient API credits")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("OpenAI API Key Configuration Test")
    print("=" * 60)
    print()
    
    success = test_openai_key()
    
    print()
    print("=" * 60)
    if success:
        print("✅ All tests passed! OpenAI integration is ready.")
    else:
        print("❌ Configuration issues detected. Please fix and try again.")
    print("=" * 60)
