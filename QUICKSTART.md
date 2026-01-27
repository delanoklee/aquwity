# Acuity - Quick Start Guide

Get up and running with Acuity in 5 minutes!

## Step 1: Get an Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy it (you'll need it in step 3)

## Step 2: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

**Linux users**: You may need tkinter:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
```

## Step 3: Configure

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use any text editor
```

Your `.env` should look like:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
SCREENSHOT_INTERVAL=5
DB_PATH=./data/acuity.db
```

## Step 4: Run

```bash
python main.py
```

## Step 5: Use It!

1. Type what you're working on (e.g., "Writing documentation")
2. Click "Start Task"
3. Work normally
4. Every 5 minutes, Acuity will check if you're on-task
5. View your focus percentage in the dashboard

## That's It!

You're now tracking your focus automatically. The app will:
- Take screenshots every 5 minutes
- Use AI to check if you're on-task
- Show you daily statistics
- Help you stay focused on priorities

## Tips

- Click "Check Now" to test it immediately
- Click "Complete Task" when done, then start a new task
- Check your percentage throughout the day
- Adjust `SCREENSHOT_INTERVAL` in `.env` to change frequency

## Need Help?

See the full README.md for detailed documentation, troubleshooting, and advanced configuration.
