# Acuity - Focus Tracker MVP

Acuity is a productivity tool that helps you stay focused on your daily priorities by taking periodic screenshots and using AI to determine if you're on-task.

## Features

- **Automatic Screenshot Monitoring**: Captures screenshots every 5 minutes (configurable)
- **AI-Powered Analysis**: Uses Claude AI with vision capabilities to analyze what you're doing
- **Inactivity Detection**: Compares consecutive screenshots to detect when you're away
- **Task Management**: Simple interface to set what you're working on and mark tasks complete
- **Daily Reports**: Shows percentage of time spent on-task vs off-task
- **Privacy-Focused**: Screenshots are analyzed and deleted (not stored permanently)

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (get one at https://console.anthropic.com/)
- Linux, macOS, or Windows

## Installation

### 1. Clone or navigate to the project directory

```bash
cd /home/del/codingprojects/acuity/mvp
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Note: On Linux, you may need to install tkinter separately:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

You can also adjust the screenshot interval (in minutes):
```
SCREENSHOT_INTERVAL=5
```

## Usage

### Starting Acuity

```bash
python main.py
```

Or make it executable:
```bash
chmod +x main.py
./main.py
```

### Using the Application

1. **Start a Task**:
   - Type what you're working on in the task field (e.g., "Writing project report")
   - Click "Start Task" or press Enter

2. **Automatic Monitoring**:
   - Acuity will automatically take screenshots every 5 minutes
   - Claude AI analyzes each screenshot to determine if you're on-task
   - Results are logged and displayed in the dashboard

3. **Complete a Task**:
   - When you finish, click "Complete Task"
   - Start a new task when you're ready

4. **Manual Check**:
   - Click "Check Now" to trigger an immediate analysis
   - Useful for testing or immediate feedback

5. **View Results**:
   - Today's summary shows your on-task percentage
   - Recent activity shows the last 10 checks
   - ✓ ON TASK = Working on stated task
   - ✗ OFF TASK = Doing something else
   - ⊝ INACTIVE = Screen unchanged (away from computer)

## How It Works

1. **Screenshot Capture**: Every N minutes, Acuity captures your screen
2. **Inactivity Detection**: Compares current screenshot with previous one
   - If >95% similar, marks as inactive (you're away)
3. **AI Analysis**: If screen has changed, sends to Claude AI
   - AI analyzes what you're doing
   - Compares with your stated task
   - Determines if you're on-task or off-task
4. **Logging**: Results are stored in SQLite database
5. **Reporting**: Daily summaries calculate your focus percentage

## Project Structure

```
mvp/
├── main.py                 # Application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── src/
│   ├── database.py       # SQLite database operations
│   ├── screenshot_capture.py  # Screenshot capture and comparison
│   ├── ai_analyzer.py    # Claude API integration
│   └── background_worker.py   # Periodic monitoring scheduler
├── ui/
│   └── gui.py            # Tkinter GUI
└── data/
    └── acuity.db         # SQLite database (created on first run)
```

## Database Schema

### Tasks Table
- Stores what you're working on
- Tracks start/completion times
- One active task at a time

### Activity Logs Table
- Stores each check result
- Links to current task
- Includes AI analysis and confidence score

### Daily Summaries Table
- Aggregates daily statistics
- Calculates on-task percentage

## Configuration Options

Edit `.env` to customize:

- `ANTHROPIC_API_KEY`: Your Claude API key (required)
- `SCREENSHOT_INTERVAL`: Minutes between checks (default: 5)
- `DB_PATH`: Database file location (default: ./data/acuity.db)

## Privacy & Security

- Screenshots are sent to Anthropic's API for analysis
- Screenshots are NOT stored permanently (unless you modify the code)
- Only analysis results are saved to the database
- Database is stored locally on your machine
- No data is sent anywhere except to Claude API for analysis

## API Costs

Acuity uses Claude 3.5 Sonnet with vision capabilities. Approximate costs:

- ~$0.015 per screenshot analysis
- At 5-minute intervals: ~$0.18 per hour (12 checks)
- Full 8-hour workday: ~$1.44
- Full month (22 workdays): ~$32

You can increase the `SCREENSHOT_INTERVAL` to reduce costs.

## Troubleshooting

### "No module named 'tkinter'"
Install tkinter for your system (see Installation step 3)

### "Configuration Error: ANTHROPIC_API_KEY not found"
1. Make sure you created `.env` file (copy from `.env.example`)
2. Add your API key to the `.env` file
3. Get API key from https://console.anthropic.com/

### Screenshots not working
- Make sure you have display server running (X11 or Wayland on Linux)
- On Wayland, you may need additional permissions

### "Permission denied" errors
- Make sure the `data/` directory is writable
- On Linux, check file permissions

## Roadmap / Future Improvements

- [ ] Web-based dashboard
- [ ] Multi-monitor support
- [ ] Configurable inactivity threshold
- [ ] Weekly/monthly reports
- [ ] Export data to CSV
- [ ] Category-based tracking (not just specific tasks)
- [ ] Break time tracking
- [ ] Pomodoro timer integration
- [ ] Mobile app for viewing stats

## Contributing

This is an MVP. Feel free to fork and improve!

## License

MIT License - feel free to use and modify as needed.
