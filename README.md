# Cheappo - Telegram Bot for Badminton Equipment Deals

A Telegram bot that monitors and notifies users about badminton equipment sales and deals.

## Features

- 🏸 Monitor Yonex badminton racquets from SunriseClick
- 🏸 Track Li-Ning badminton equipment deals
- 📱 Telegram bot interface for easy interaction
- 🔔 Automated channel notifications for new deals

## Setup

### 1. Prerequisites

- Python 3.7+
- A Telegram account
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/m5x4/cheappo.git
cd cheappo

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   TELEGRAM_CHAT_ID=your_chat_id
   TELEGRAM_CHANNEL_ID=your_channel_id  # For channel notifications
   ```

3. **How to get your Telegram Chat ID:**
   - Send a message to [@userinfobot](https://t.me/userinfobot)
   - It will reply with your user ID

4. **How to get your Channel ID (for racquet_notifier.py):**
   - Create a channel
   - Add your bot as an admin to the channel
   - Forward any message from the channel to [@userinfobot](https://t.me/userinfobot)
   - Or use the channel username like `@YourChannelName`

### 4. Running the Bot

**Interactive Bot:**
```bash
python bot.py
```

**Channel Notifier (automated deal posting):**
```bash
# Check for new deals and post them
python racquet_notifier.py

# Post all current deals (for initial setup)
python racquet_notifier.py --all

# Test mode (check without posting)
python racquet_notifier.py --test
```

**Automated Scheduling:**

Set up a cron job to check for deals periodically:
```bash
# Edit crontab
crontab -e

# Add this line to check every 6 hours
0 */6 * * * cd /path/to/cheappo && ./venv/bin/python racquet_notifier.py
```

## Available Commands

- `/start` - Start the bot
- `/help` - Show help message
- `/nike` - Show Nike badminton shoes deals
- `/yonex` - Show Yonex racquet deals
- `/lining` - Show Li-Ning equipment deals

## Security

⚠️ **IMPORTANT**: Never commit your `.env` file or expose your bot token!

- Your bot token is like a password - keep it secret
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Use environment variables for all sensitive data
- If your token is exposed, revoke it immediately using [@BotFather](https://t.me/BotFather)

## GitHub Actions

This repository includes GitHub Actions workflows that use GitHub Secrets for secure credential management. To set up:

1. Go to your repository Settings → Secrets and variables → Actions
2. Add these secrets:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`

## License

This project is open source and available for personal use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
