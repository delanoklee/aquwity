#!/usr/bin/env python3
"""
Test script to verify Acuity setup is correct
"""

import sys
import os

def test_imports():
    """Test that all required packages are installed"""
    print("Testing package imports...")

    try:
        import anthropic
        print("  ✓ anthropic")
    except ImportError:
        print("  ✗ anthropic - run: pip install anthropic")
        return False

    try:
        from PIL import Image
        print("  ✓ PIL (Pillow)")
    except ImportError:
        print("  ✗ PIL - run: pip install pillow")
        return False

    try:
        import mss
        print("  ✓ mss")
    except ImportError:
        print("  ✗ mss - run: pip install mss")
        return False

    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv")
    except ImportError:
        print("  ✗ python-dotenv - run: pip install python-dotenv")
        return False

    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        print("  ✓ apscheduler")
    except ImportError:
        print("  ✗ apscheduler - run: pip install apscheduler")
        return False

    try:
        import imagehash
        print("  ✓ imagehash")
    except ImportError:
        print("  ✗ imagehash - run: pip install imagehash")
        return False

    try:
        import tkinter
        print("  ✓ tkinter")
    except ImportError:
        print("  ✗ tkinter - install python3-tk for your system")
        return False

    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")

    if not os.path.exists('.env'):
        print("  ✗ .env file not found")
        print("    Run: cp .env.example .env")
        return False
    print("  ✓ .env file exists")

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        print("  ✗ ANTHROPIC_API_KEY not set in .env")
        print("    Get your key from: https://console.anthropic.com/")
        return False
    print("  ✓ ANTHROPIC_API_KEY is set")

    return True

def test_screenshot():
    """Test screenshot capture"""
    print("\nTesting screenshot capture...")

    try:
        from src.screenshot_capture import ScreenshotCapture

        capturer = ScreenshotCapture()
        screenshot = capturer.capture_screenshot()

        print(f"  ✓ Screenshot captured: {screenshot.size[0]}x{screenshot.size[1]}")

        # Test base64 encoding
        base64_img = capturer.image_to_base64(screenshot)
        print(f"  ✓ Base64 encoding works ({len(base64_img)} bytes)")

        return True
    except Exception as e:
        print(f"  ✗ Screenshot test failed: {e}")
        return False

def test_database():
    """Test database creation"""
    print("\nTesting database...")

    try:
        from src.database import Database
        import tempfile
        import os

        # Use temporary database for testing
        temp_db = os.path.join(tempfile.gettempdir(), 'acuity_test.db')

        db = Database(temp_db)
        print("  ✓ Database created")

        # Test task creation
        task_id = db.create_task("Test task")
        print(f"  ✓ Task creation works (ID: {task_id})")

        # Test task retrieval
        task = db.get_current_task()
        assert task is not None
        assert task['description'] == "Test task"
        print("  ✓ Task retrieval works")

        # Clean up
        os.remove(temp_db)
        print("  ✓ Database operations successful")

        return True
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False

def test_api():
    """Test Anthropic API connection"""
    print("\nTesting Anthropic API connection...")

    try:
        from config import Config
        from dotenv import load_dotenv
        load_dotenv()

        Config.validate()

        import anthropic
        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)

        # Simple test message
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )

        print("  ✓ API connection successful")
        print(f"  ✓ Response: {message.content[0].text}")

        return True
    except Exception as e:
        print(f"  ✗ API test failed: {e}")
        if "authentication" in str(e).lower():
            print("    Check your API key in .env")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Acuity Setup Test")
    print("=" * 60)

    results = []

    results.append(("Package imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Screenshot capture", test_screenshot()))
    results.append(("Database operations", test_database()))
    results.append(("API connection", test_api()))

    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All tests passed! You're ready to run Acuity.")
        print("\nRun: python main.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nSee QUICKSTART.md or README.md for setup instructions.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
