# 🚨 CRITICAL SECURITY ALERT 🚨

## Exposed Telegram Bot Token Found in Git History

### What was found:
A Telegram bot token was discovered **hardcoded** in the git commit history:
- **Token**: `7933198908:AAGeEBuZ2-eNtEzeJOZatnuN0-b9J_vLXb0`
- **Location**: `config.py`
- **Commit**: `caed66c63364c802402e1ecf1c849079e5f2a909`
- **Additional Exposure**: Telegram Channel ID `-1003720624349` was also hardcoded in `racquet_notifier.py`

### Why this is critical:
✗ The token is permanently stored in Git history, even though it's been removed from the current code
✗ Anyone with access to this repository can see the token in the git history
✗ The token can be used to control your Telegram bot and send messages
✗ If this repository is public, the token is exposed to the entire world

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

The Telegram Channel ID `-1003720624349` was also exposed. While less critical than the bot token, you may want to:
- Make your channel private if it's currently public
- Change your channel settings if needed
- Update the channel ID in your environment variables

### Questions?

If you need help with any of these steps, please consult:
- Telegram Bot API documentation: https://core.telegram.org/bots/api
- GitHub documentation on removing sensitive data: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository

---

**Status**: The current code is now secure, but the exposed token in git history must be revoked immediately.
