import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Optional

from src.database import Database
from src.background_worker import BackgroundWorker

class AcuityGUI:
    """Simple GUI for Acuity focus tracker"""

    def __init__(self, db: Database, worker: BackgroundWorker):
        self.db = db
        self.worker = worker
        self.current_task = None

        # Create main window
        self.root = tk.Tk()
        self.root.title("Acuity - Focus Tracker")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.setup_ui()
        self.update_display()

        # Set update callback for worker
        self.worker.update_callback = self.update_display

    def setup_ui(self):
        """Setup the user interface"""

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Acuity Focus Tracker",
                               font=('Arial', 18, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Current Task Section
        task_frame = ttk.LabelFrame(main_frame, text="Current Task", padding="10")
        task_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        task_frame.columnconfigure(0, weight=1)

        # Task input
        self.task_entry = ttk.Entry(task_frame, font=('Arial', 12))
        self.task_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.start_task())

        # Task buttons
        button_frame = ttk.Frame(task_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.start_button = ttk.Button(button_frame, text="Start Task",
                                       command=self.start_task)
        self.start_button.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))

        self.complete_button = ttk.Button(button_frame, text="Complete Task",
                                         command=self.complete_task,
                                         state=tk.DISABLED)
        self.complete_button.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))

        # Current task display
        self.current_task_label = ttk.Label(task_frame, text="No active task",
                                           font=('Arial', 10, 'italic'),
                                           foreground='gray')
        self.current_task_label.grid(row=2, column=0, pady=(10, 0))

        # Today's Summary Section
        summary_frame = ttk.LabelFrame(main_frame, text="Today's Summary", padding="10")
        summary_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        summary_frame.columnconfigure(0, weight=1)

        # Summary labels
        self.summary_text = tk.Text(summary_frame, height=6, font=('Arial', 10),
                                   state=tk.DISABLED, wrap=tk.WORD)
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Recent Activity Section
        activity_frame = ttk.LabelFrame(main_frame, text="Recent Activity", padding="10")
        activity_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        activity_frame.columnconfigure(0, weight=1)
        activity_frame.rowconfigure(0, weight=1)

        # Activity list with scrollbar
        activity_scroll = ttk.Scrollbar(activity_frame)
        activity_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.activity_listbox = tk.Listbox(activity_frame, height=8, font=('Arial', 9),
                                          yscrollcommand=activity_scroll.set)
        self.activity_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        activity_scroll.config(command=self.activity_listbox.yview)

        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, sticky=(tk.W, tk.E))
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)

        self.refresh_button = ttk.Button(control_frame, text="Refresh",
                                        command=self.update_display)
        self.refresh_button.grid(row=0, column=0, padx=(0, 5), sticky=(tk.W, tk.E))

        self.check_now_button = ttk.Button(control_frame, text="Check Now",
                                          command=self.force_check)
        self.check_now_button.grid(row=0, column=1, padx=(5, 0), sticky=(tk.W, tk.E))

        # Status bar
        self.status_label = ttk.Label(main_frame, text="Ready",
                                     font=('Arial', 9), foreground='green')
        self.status_label.grid(row=5, column=0, pady=(10, 0))

        # Configure row weights for resizing
        main_frame.rowconfigure(3, weight=1)

    def start_task(self):
        """Start a new task"""
        task_description = self.task_entry.get().strip()

        if not task_description:
            messagebox.showwarning("No Task", "Please enter a task description.")
            return

        try:
            task_id = self.db.create_task(task_description)
            self.task_entry.delete(0, tk.END)
            self.update_display()
            self.status_label.config(text=f"Started task: {task_description}", foreground='green')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start task: {e}")

    def complete_task(self):
        """Mark current task as complete"""
        if self.current_task:
            try:
                self.db.complete_task(self.current_task['id'])
                self.update_display()
                self.status_label.config(text="Task completed!", foreground='green')
            except Exception as e:
                messagebox.showerror("Error", f"Failed to complete task: {e}")

    def force_check(self):
        """Manually trigger an activity check"""
        if not self.current_task:
            messagebox.showinfo("No Task", "Please start a task before checking activity.")
            return

        self.status_label.config(text="Checking now...", foreground='orange')
        self.root.update()

        try:
            self.worker.force_check()
            self.update_display()
            self.status_label.config(text="Check completed!", foreground='green')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to perform check: {e}")
            self.status_label.config(text="Check failed", foreground='red')

    def update_display(self):
        """Update all display elements"""
        try:
            # Update current task
            self.current_task = self.db.get_current_task()

            if self.current_task:
                task_desc = self.current_task['description']
                started = self.current_task['started_at']
                self.current_task_label.config(
                    text=f"Working on: {task_desc}\nStarted: {started}",
                    foreground='black'
                )
                self.complete_button.config(state=tk.NORMAL)
            else:
                self.current_task_label.config(text="No active task", foreground='gray')
                self.complete_button.config(state=tk.DISABLED)

            # Update summary
            summary = self.db.get_today_summary()
            summary_text = f"""
Total Checks: {summary['total_checks']}
On Task: {summary['on_task_count']} ({summary['on_task_percentage']:.1f}%)
Off Task: {summary['off_task_count']}
Inactive: {summary['inactive_count']}
"""
            self.summary_text.config(state=tk.NORMAL)
            self.summary_text.delete(1.0, tk.END)
            self.summary_text.insert(1.0, summary_text)
            self.summary_text.config(state=tk.DISABLED)

            # Update recent activity
            activities = self.db.get_recent_activities(10)
            self.activity_listbox.delete(0, tk.END)

            for activity in activities:
                timestamp = activity['timestamp']
                status = "✓ ON TASK" if activity['is_on_task'] else "✗ OFF TASK"
                if activity['is_inactive']:
                    status = "⊝ INACTIVE"

                analysis = activity['ai_analysis'][:50] if activity['ai_analysis'] else ""

                line = f"{timestamp[:16]} | {status} | {analysis}"
                self.activity_listbox.insert(tk.END, line)

        except Exception as e:
            print(f"Error updating display: {e}")

    def run(self):
        """Start the GUI main loop"""
        self.root.mainloop()
