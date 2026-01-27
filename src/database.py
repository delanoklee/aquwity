import sqlite3
from datetime import datetime
from typing import Optional, List, Dict
import os

class Database:
    """Handles all database operations for Acuity"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()

    def init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tasks table - stores what the user should be working on
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                started_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Activity logs table - stores screenshot analysis results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                timestamp TIMESTAMP NOT NULL,
                is_on_task INTEGER NOT NULL,
                is_inactive INTEGER DEFAULT 0,
                ai_analysis TEXT,
                confidence REAL,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        ''')

        # Daily summaries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL UNIQUE,
                total_checks INTEGER DEFAULT 0,
                on_task_count INTEGER DEFAULT 0,
                off_task_count INTEGER DEFAULT 0,
                inactive_count INTEGER DEFAULT 0,
                on_task_percentage REAL DEFAULT 0
            )
        ''')

        conn.commit()
        conn.close()

    def get_current_task(self) -> Optional[Dict]:
        """Get the currently active task"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM tasks
            WHERE is_active = 1 AND completed_at IS NULL
            ORDER BY started_at DESC
            LIMIT 1
        ''')

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    def create_task(self, description: str) -> int:
        """Create a new task and mark it as active"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Deactivate any existing active tasks
        cursor.execute('''
            UPDATE tasks SET is_active = 0
            WHERE is_active = 1 AND completed_at IS NULL
        ''')

        # Create new task
        cursor.execute('''
            INSERT INTO tasks (description, started_at)
            VALUES (?, ?)
        ''', (description, datetime.now()))

        task_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return task_id

    def complete_task(self, task_id: int):
        """Mark a task as completed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tasks
            SET completed_at = ?, is_active = 0
            WHERE id = ?
        ''', (datetime.now(), task_id))

        conn.commit()
        conn.close()

    def log_activity(self, task_id: Optional[int], is_on_task: bool,
                     is_inactive: bool = False, ai_analysis: str = "",
                     confidence: float = 0.0):
        """Log an activity check result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO activity_logs
            (task_id, timestamp, is_on_task, is_inactive, ai_analysis, confidence)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_id, datetime.now(), int(is_on_task), int(is_inactive),
              ai_analysis, confidence))

        conn.commit()
        conn.close()

        # Update daily summary
        self.update_daily_summary()

    def update_daily_summary(self):
        """Update or create today's summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        today = datetime.now().date()

        # Get today's stats
        cursor.execute('''
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN is_on_task = 1 THEN 1 ELSE 0 END) as on_task,
                SUM(CASE WHEN is_on_task = 0 AND is_inactive = 0 THEN 1 ELSE 0 END) as off_task,
                SUM(CASE WHEN is_inactive = 1 THEN 1 ELSE 0 END) as inactive
            FROM activity_logs
            WHERE DATE(timestamp) = ?
        ''', (today,))

        stats = cursor.fetchone()
        total, on_task, off_task, inactive = stats

        on_task_pct = (on_task / total * 100) if total > 0 else 0

        # Insert or update summary
        cursor.execute('''
            INSERT INTO daily_summaries
            (date, total_checks, on_task_count, off_task_count, inactive_count, on_task_percentage)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                total_checks = excluded.total_checks,
                on_task_count = excluded.on_task_count,
                off_task_count = excluded.off_task_count,
                inactive_count = excluded.inactive_count,
                on_task_percentage = excluded.on_task_percentage
        ''', (today, total, on_task, off_task, inactive, on_task_pct))

        conn.commit()
        conn.close()

    def get_today_summary(self) -> Dict:
        """Get today's activity summary"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        today = datetime.now().date()

        cursor.execute('''
            SELECT * FROM daily_summaries WHERE date = ?
        ''', (today,))

        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)

        return {
            'date': today,
            'total_checks': 0,
            'on_task_count': 0,
            'off_task_count': 0,
            'inactive_count': 0,
            'on_task_percentage': 0.0
        }

    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent activity logs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                a.*,
                t.description as task_description
            FROM activity_logs a
            LEFT JOIN tasks t ON a.task_id = t.id
            ORDER BY a.timestamp DESC
            LIMIT ?
        ''', (limit,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]
