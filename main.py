#!/usr/bin/env python3
"""
Acuity - Focus Tracker MVP
Monitors user activity to help maintain focus on priorities
"""

import sys
from config import Config
from src.database import Database
from src.ai_analyzer import AIAnalyzer
from src.background_worker import BackgroundWorker
from ui.gui import AcuityGUI
from ui.setup_wizard import run_setup_if_needed

def main():
    """Main entry point for Acuity"""

    print("=" * 50)
    print("Acuity Focus Tracker - MVP")
    print("=" * 50)

    # Run setup wizard if needed
    if not run_setup_if_needed():
        print("\nSetup cancelled. Exiting.")
        sys.exit(0)

    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease run the setup wizard again or manually configure .env")
        sys.exit(1)

    print(f"\n✓ Configuration loaded")
    print(f"  - Screenshot interval: {Config.SCREENSHOT_INTERVAL} minutes")
    print(f"  - Database: {Config.DB_PATH}")

    # Initialize components
    try:
        print("\n✓ Initializing database...")
        db = Database(Config.DB_PATH)

        print("✓ Initializing AI analyzer...")
        ai_analyzer = AIAnalyzer(Config.ANTHROPIC_API_KEY)

        print("✓ Initializing background worker...")
        worker = BackgroundWorker(db, ai_analyzer)

        print("✓ Starting background monitoring...")
        worker.start()

        print("\n✓ Launching GUI...")
        gui = AcuityGUI(db, worker)

        print("\n" + "=" * 50)
        print("Acuity is now running!")
        print("=" * 50)
        print("\nTo use:")
        print("1. Enter what you're working on in the task field")
        print("2. Click 'Start Task'")
        print("3. Acuity will monitor your activity automatically")
        print(f"4. Screenshots will be analyzed every {Config.SCREENSHOT_INTERVAL} minutes")
        print("\nYou can also click 'Check Now' to trigger an immediate check.")
        print("\n" + "=" * 50 + "\n")

        # Run the GUI (blocking)
        gui.run()

        # Cleanup on exit
        print("\nStopping background worker...")
        worker.stop()
        print("Acuity shut down cleanly.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
