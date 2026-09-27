# Telegram Token Viability Bot

A Telegram bot for analyzing token/project viability with built-in referral system.

## Features
- Token link analysis (mock data)
- Referral tracking system
- Persistent data storage
- Environment variable support

## Local Development

```bash
pip install -r requirements.txt
```

Create `.env` file:
```
BOT_TOKEN=your_bot_token_here
```

Run:
```bash
python bot.py
```

## Deploy to Render.com

1. **Push to GitHub**
   - Initialize git and push this repo to GitHub

2. **Connect to Render**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the branch

3. **Configure on Render**
   - **Name:** `telegram-bot` (or your choice)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

4. **Set Environment Variables**
   - In Render dashboard, go to "Environment"
   - Add variable: `BOT_TOKEN` = your Telegram bot token
   - Deploy

5. **Keep Bot Running**
   - Free tier will spin down after 15 minutes of inactivity
   - For 24/7 uptime, use Render's paid tier (~$7/month)

## Files
- `bot.py` - Main bot code
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `.env.example` - Environment variable template
- `referral_db.json` - Persistent referral data (auto-created)

## Notes
- Referral data persists in `referral_db.json`
- Token is read from `BOT_TOKEN` environment variable
- Never commit `.env` file to GitHub
