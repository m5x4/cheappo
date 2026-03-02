# 🚨 CRITICAL SECURITY ALERT 🚨

## Exposed Telegram Bot Token Found in Git History

### What was found:
A Telegram bot token was discovered **hardcoded** in the git commit history:
- **Bot Token** (CRITICAL): `7933198908:AAGeEBuZ2-eNtEzeJOZatnuN0-b9J_vLXb0`
- **Channel ID** (HIGH): `-1003720624349`
- **Location**: `config.py` and `racquet_notifier.py`
- **Commit**: `caed66c63364c802402e1ecf1c849079e5f2a909`

### Why this is critical:
✗ The bot token is permanently stored in Git history, even though it's been removed from the current code
✗ Anyone with access to this repository can see both the token and channel ID in the git history
✗ The bot token can be used to control your Telegram bot and send messages as your bot
✗ The channel ID exposure allows anyone to identify your specific channel and potentially:
  - Monitor channel activity
  - Send spam or unwanted messages (if they gain bot access)
  - Target the channel for attacks or monitoring
✗ If this repository is public, both credentials are exposed to the entire world

### What you need to do IMMEDIATELY:

#### 1. **REVOKE THE EXPOSED TOKEN** (Most Important!)
   ```
   1. Open Telegram and message @BotFather
   2. Send the command: /mybots
   3. Select your bot (@cheappoBot)
   4. Choose "API Token"
   5. Click "Revoke current token"
   6. Get your new token
   7. Update your environment variables with the new token
   ```

#### 2. **Set up your new token securely**
   ```bash
   # Create a .env file (already in .gitignore)
   echo "TELEGRAM_BOT_TOKEN=your_new_token_here" > .env
   echo "TELEGRAM_CHAT_ID=your_chat_id" >> .env
   echo "TELEGRAM_CHANNEL_ID=your_channel_id" >> .env
   ```

#### 3. **Update GitHub Actions Secrets** (if using)
   ```
   1. Go to: Repository Settings → Secrets and variables → Actions
   2. Update TELEGRAM_BOT_TOKEN with your new token
   3. Ensure TELEGRAM_CHANNEL_ID is also set
   ```

#### 4. **(Optional but Recommended) Clean Git History**
   
   **WARNING**: This will rewrite git history and require force-push. Only do this if you understand the implications.
   
   To completely remove the token from git history, you would need to use tools like:
   - `git filter-branch` or `git filter-repo`
   - BFG Repo-Cleaner
   
   However, if the repository has already been cloned by others or is public, the token is already compromised regardless.

### What has been fixed in this PR:

✓ Removed hardcoded token from `config.py` - now requires environment variable
✓ Removed hardcoded channel ID from `racquet_notifier.py`
✓ Added `.env.example` template for secure configuration
✓ Updated `.gitignore` to prevent future `.env` commits
✓ Created comprehensive `README.md` with security instructions
✓ Added validation to ensure TOKEN environment variable is set

### Prevention for the future:

1. **Never** commit secrets, tokens, or API keys to git
2. **Always** use environment variables for sensitive data
3. **Use** pre-commit hooks to scan for secrets (e.g., `git-secrets`, `detect-secrets`)
4. **Review** code before committing to ensure no secrets are included
5. **Use** GitHub's secret scanning if available (automatically enabled for public repos)

### Additional Channel Security Note:

The Telegram Channel ID `-1003720624349` was also exposed. This is a **HIGH severity** issue because:
- Anyone can identify which specific channel your bot is posting to
- If combined with the bot token, they could send messages to your channel
- The channel could be targeted for monitoring or spam

**Recommended Actions:**
1. **Option A - Create a new channel (Most Secure)**:
   - Create a completely new Telegram channel
   - Add your bot (with the new token) as admin
   - Update your TELEGRAM_CHANNEL_ID environment variable
   - Migrate your subscribers to the new channel if needed
   - Delete or archive the old channel

2. **Option B - Secure the existing channel (Less Secure)**:
   - Make your channel private (if currently public)
   - Review and remove any suspicious members
   - Enable "Sign messages" to make it clear who posted what
   - Monitor for any unauthorized posts
   - Update the channel ID in your environment variables (even though it's the same, this ensures consistency)

**Which option to choose?**
- If your channel is public or has many unknown members: Choose Option A
- If your channel is small and you know all members: Option B may be acceptable
- When in doubt: Choose Option A for maximum security

### Questions?

If you need help with any of these steps, please consult:
- Telegram Bot API documentation: https://core.telegram.org/bots/api
- GitHub documentation on removing sensitive data: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

---

**Status**: The current code is now secure, but the exposed token in git history must be revoked immediately.
