import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import os

class SetupWizard:
    """First-run setup wizard for Acuity"""

    def __init__(self):
        self.api_key = None
        self.completed = False

        # Create window
        self.root = tk.Tk()
        self.root.title("Acuity Setup")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        """Setup the wizard UI"""

        # Main container
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Welcome title
        title_label = ttk.Label(
            main_frame,
            text="Welcome to Acuity!",
            font=('Arial', 20, 'bold')
        )
        title_label.grid(row=0, column=0, pady=(0, 10))

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Your AI-powered focus tracker",
            font=('Arial', 12)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 30))

        # Instructions
        instructions = """To use Acuity, you need an Anthropic API key.
This allows Acuity to use Claude AI to analyze
your screenshots and determine if you're on-task.

Don't worry - it only takes 2 minutes to set up!"""

        instructions_label = ttk.Label(
            main_frame,
            text=instructions,
            justify=tk.CENTER,
            font=('Arial', 10)
        )
        instructions_label.grid(row=2, column=0, pady=(0, 20))

        # Get API Key button
        get_key_button = ttk.Button(
            main_frame,
            text="Get API Key (Opens Browser)",
            command=self.open_anthropic_console
        )
        get_key_button.grid(row=3, column=0, pady=(0, 20), sticky=(tk.W, tk.E))

        # API Key input section
        api_key_label = ttk.Label(
            main_frame,
            text="Paste your API key here:",
            font=('Arial', 10, 'bold')
        )
        api_key_label.grid(row=4, column=0, pady=(0, 5))

        self.api_key_entry = ttk.Entry(main_frame, font=('Arial', 10), show='*')
        self.api_key_entry.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # Show/Hide toggle
        self.show_key_var = tk.BooleanVar(value=False)
        show_key_check = ttk.Checkbutton(
            main_frame,
            text="Show API key",
            variable=self.show_key_var,
            command=self.toggle_key_visibility
        )
        show_key_check.grid(row=6, column=0, sticky=tk.W, pady=(0, 20))

        # Continue button
        self.continue_button = ttk.Button(
            main_frame,
            text="Continue",
            command=self.validate_and_save
        )
        self.continue_button.grid(row=7, column=0, sticky=(tk.W, tk.E))

        # Later button
        later_button = ttk.Button(
            main_frame,
            text="I'll do this later",
            command=self.skip_setup
        )
        later_button.grid(row=8, column=0, pady=(10, 0))

    def open_anthropic_console(self):
        """Open Anthropic console in browser"""
        webbrowser.open('https://console.anthropic.com/')

    def toggle_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')

    def validate_and_save(self):
        """Validate and save the API key"""
        api_key = self.api_key_entry.get().strip()

        if not api_key:
            messagebox.showwarning("Missing API Key", "Please enter your API key.")
            return

        # Basic validation - Anthropic keys start with 'sk-ant-'
        if not api_key.startswith('sk-ant-'):
            result = messagebox.askyesno(
                "Invalid Format",
                "This doesn't look like a valid Anthropic API key.\n"
                "Anthropic keys start with 'sk-ant-'.\n\n"
                "Continue anyway?"
            )
            if not result:
                return

        # Save to .env file
        try:
            self.save_api_key(api_key)
            self.api_key = api_key
            self.completed = True

            messagebox.showinfo(
                "Setup Complete!",
                "Your API key has been saved.\n\n"
                "Acuity will now start!"
            )

            self.root.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error Saving",
                f"Failed to save API key: {e}\n\n"
                "Please try again or contact support."
            )

    def save_api_key(self, api_key: str):
        """Save API key to .env file"""
        env_path = '.env'

        # Read existing .env or create new one
        env_content = {}
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_content[key.strip()] = value.strip()

        # Update API key
        env_content['ANTHROPIC_API_KEY'] = api_key

        # Set defaults if not present
        if 'SCREENSHOT_INTERVAL' not in env_content:
            env_content['SCREENSHOT_INTERVAL'] = '5'
        if 'DB_PATH' not in env_content:
            env_content['DB_PATH'] = './data/acuity.db'

        # Write back to file
        with open(env_path, 'w') as f:
            f.write("# Acuity Configuration\n")
            f.write("# Generated by setup wizard\n\n")
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")

    def skip_setup(self):
        """User chose to skip setup"""
        result = messagebox.askyesno(
            "Skip Setup?",
            "You need an API key to use Acuity.\n\n"
            "Are you sure you want to skip setup?\n"
            "You can always run setup again later."
        )

        if result:
            self.completed = False
            self.root.destroy()

    def run(self) -> bool:
        """Run the wizard and return whether setup was completed"""
        self.root.mainloop()
        return self.completed


def needs_setup() -> bool:
    """Check if setup wizard needs to run"""
    # Check if .env exists and has API key
    if not os.path.exists('.env'):
        return True

    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key or api_key == 'your_api_key_here':
        return True

    return False


def run_setup_if_needed() -> bool:
    """Run setup wizard if needed. Returns True if app should continue."""
    if needs_setup():
        wizard = SetupWizard()
        completed = wizard.run()

        if not completed:
            # User skipped setup
            return False

        # Reload environment after setup
        from dotenv import load_dotenv
        load_dotenv(override=True)

    return True
