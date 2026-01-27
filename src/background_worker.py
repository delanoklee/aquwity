from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import threading
from typing import Optional, Callable

from src.screenshot_capture import ScreenshotCapture
from src.ai_analyzer import AIAnalyzer
from src.database import Database
from config import Config

class BackgroundWorker:
    """Manages periodic screenshot capture and analysis"""

    def __init__(self, db: Database, ai_analyzer: AIAnalyzer, update_callback: Optional[Callable] = None):
        self.db = db
        self.ai_analyzer = ai_analyzer
        self.screenshot_capture = ScreenshotCapture()
        self.scheduler = BackgroundScheduler()
        self.is_running = False
        self.update_callback = update_callback
        self.lock = threading.Lock()

    def start(self):
        """Start the background worker"""
        if not self.is_running:
            # Schedule the check to run every N minutes
            self.scheduler.add_job(
                self.perform_check,
                'interval',
                minutes=Config.SCREENSHOT_INTERVAL,
                id='screenshot_check'
            )
            self.scheduler.start()
            self.is_running = True
            print(f"Background worker started. Will check every {Config.SCREENSHOT_INTERVAL} minutes.")

            # Perform initial check immediately
            self.perform_check()

    def stop(self):
        """Stop the background worker"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            print("Background worker stopped.")

    def perform_check(self):
        """Perform a single screenshot and analysis check"""
        with self.lock:
            try:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Performing activity check...")

                # Get current task
                current_task = self.db.get_current_task()

                if not current_task:
                    print("No active task. Skipping check.")
                    return

                task_description = current_task['description']
                task_id = current_task['id']

                print(f"Current task: {task_description}")

                # Capture screenshot and check for inactivity
                screenshot_base64, is_inactive, similarity = self.screenshot_capture.get_screenshot_for_api()

                print(f"Screenshot captured. Inactive: {is_inactive}, Similarity: {similarity:.2%}")

                # Analyze with AI
                is_on_task, analysis, confidence = self.ai_analyzer.analyze_with_inactivity_check(
                    screenshot_base64,
                    task_description,
                    is_inactive,
                    similarity
                )

                print(f"Analysis: {'ON TASK' if is_on_task else 'OFF TASK'} (confidence: {confidence:.2%})")
                print(f"Details: {analysis}")

                # Log to database
                self.db.log_activity(
                    task_id=task_id,
                    is_on_task=is_on_task,
                    is_inactive=is_inactive,
                    ai_analysis=analysis,
                    confidence=confidence
                )

                print("Activity logged successfully.")

                # Notify UI if callback is set
                if self.update_callback:
                    self.update_callback()

            except Exception as e:
                print(f"Error during check: {e}")
                import traceback
                traceback.print_exc()

    def force_check(self):
        """Manually trigger a check (useful for testing)"""
        if self.is_running:
            self.perform_check()
        else:
            print("Worker is not running. Start it first.")
