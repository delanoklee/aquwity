#!/usr/bin/env python3
"""Acuity - Simple text input bar"""

import tkinter as tk
import sys


class AcuityApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Acuity")

        # Make it a slim, minimal window
        self.root.geometry("400x50")
        self.root.resizable(True, False)  # Can resize width, not height

        # Dark theme colors
        bg_color = "#1a1a1a"
        fg_color = "#ffffff"
        entry_bg = "#2d2d2d"

        self.root.configure(bg=bg_color)

        # Create the text input
        self.entry = tk.Entry(
            self.root,
            font=("Helvetica", 16),
            bg=entry_bg,
            fg=fg_color,
            insertbackground=fg_color,  # Cursor color
            relief="flat",
            highlightthickness=1,
            highlightcolor="#4a4a4a",
            highlightbackground="#3a3a3a",
        )
        self.entry.pack(fill="x", expand=True, padx=10, pady=10)

        # Focus the entry on start
        self.entry.focus_set()

        # Bind Escape to close
        self.root.bind("<Escape>", lambda e: self.root.quit())

    def run(self):
        self.root.mainloop()


def main():
    app = AcuityApp()
    app.run()


if __name__ == "__main__":
    main()
