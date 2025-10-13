# X Bot Setup Guide 🐦

Complete guide to setting up and using the X (Twitter) Bot.

## Table of Contents
1. [Getting X API Credentials](#getting-x-api-credentials)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Troubleshooting](#troubleshooting)

---

## Getting X API Credentials

### Step 1: Apply for X Developer Account

1. Go to [developer.twitter.com](https://developer.twitter.com/)
2. Sign in with your X/Twitter account
3. Click **"Sign up for Free Account"** or **"Apply"**
4. Fill out the application form:
   - Select your use case (Hobbyist → Making a bot)
   - Describe what you plan to do with the API
   - Accept the terms and conditions
5. Verify your email address
6. Wait for approval (usually instant for basic access)

### Step 2: Create a Project and App

1. Once approved, go to the [Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Click **"+ Create Project"**
3. Name your project (e.g., "My X Bot")
4. Select use case that best fits
5. Provide a description
6. Click **"+ Create App"** within the project
7. Name your app (e.g., "X Poster Bot")

### Step 3: Get Your API Keys

1. After creating the app, you'll see your **API Key** and **API Secret**
   - **Save these immediately!** They won't be shown again
   - Store them securely

2. Generate **Access Token and Secret**:
   - Go to your app's settings
   - Navigate to **"Keys and Tokens"** tab
   - Under "Access Token and Secret", click **"Generate"**
   - Save both the **Access Token** and **Access Token Secret**

3. (Optional) Get **Bearer Token**:
   - Found in the same "Keys and Tokens" section
   - Useful for read-only operations

### Step 4: Set Permissions

1. In your app settings, go to **"Settings"** tab
2. Under **"User authentication settings"**, click **"Set up"**
3. Enable **OAuth 1.0a**
4. Set **App permissions** to:
   - ✅ **Read and Write** (to post tweets)
   - Or **Read, Write, and Direct Messages** if you need DM access
5. Add required URLs (can use placeholders for bot usage):
   - Callback URL: `http://localhost:3000/callback`
   - Website URL: `https://example.com`
6. Save changes

---

## Installation

### 1. Install Required Dependencies

```bash
pip install -r requirements.txt
```

Or install tweepy directly:
```bash
pip install tweepy
```

### 2. Set Up Credentials

Create a credentials file:

```bash
python3 x_bot.py --setup
```

This creates `x_credentials.json` with the following template:

```json
{
  "api_key": "YOUR_API_KEY_HERE",
  "api_secret": "YOUR_API_SECRET_HERE",
  "access_token": "YOUR_ACCESS_TOKEN_HERE",
  "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET_HERE",
  "bearer_token": "YOUR_BEARER_TOKEN_HERE (optional)"
}
```

### 3. Add Your Credentials

Edit `x_credentials.json` and replace the placeholder values with your actual credentials from the X Developer Portal.

---

## Configuration

### Option 1: Using Credentials File (Recommended)

Edit `x_credentials.json`:

```json
{
  "api_key": "abc123xyz...",
  "api_secret": "def456uvw...",
  "access_token": "123456-abc...",
  "access_token_secret": "xyz789qrs...",
  "bearer_token": "AAAAAAAAAAAAAAAAAAAAABc..."
}
```

### Option 2: Using Environment Variables

Alternatively, set environment variables:

```bash
export X_API_KEY="your_api_key"
export X_API_SECRET="your_api_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
export X_BEARER_TOKEN="your_bearer_token"  # optional
```

Or on Windows:
```cmd
set X_API_KEY=your_api_key
set X_API_SECRET=your_api_secret
set X_ACCESS_TOKEN=your_access_token
set X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

---

## Usage

### Command Line Usage

#### Post a Tweet

```bash
python3 x_bot.py --post "Hello from my X bot! 🤖"
```

#### Post a Tweet with Image

```bash
python3 x_bot.py --post "Check out this image!" --media photo.jpg
```

#### Post with Multiple Images (up to 4)

```bash
python3 x_bot.py --post "Here are some photos!" --media img1.jpg img2.png img3.jpg
```

#### Reply to a Tweet

```bash
python3 x_bot.py --post "Thanks for the mention!" --reply-to 1234567890
```

#### Get Your Recent Tweets

```bash
python3 x_bot.py --get-tweets
```

Get more tweets:
```bash
python3 x_bot.py --get-tweets --max-results 50
```

#### Delete a Tweet

```bash
python3 x_bot.py --delete 1234567890
```

### Using in Python Code

```python
from x_bot import XBot

# Initialize the bot
bot = XBot()

# Post a simple tweet
bot.post_tweet("Hello from Python! 🐍")

# Post a tweet with an image
bot.post_tweet_with_media(
    "Check out this screenshot!",
    ["screenshot.png"]
)

# Post with multiple images
bot.post_tweet_with_media(
    "Here's a thread of images!",
    ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]
)

# Reply to a tweet
bot.post_tweet(
    "Thanks for sharing!",
    reply_to="1234567890"
)

# Get your recent tweets
tweets = bot.get_my_tweets(max_results=20)

# Delete a tweet
bot.delete_tweet("1234567890")
```

### Advanced Usage Example

```python
from x_bot import XBot
from datetime import datetime

# Initialize bot
bot = XBot()

# Post a status update with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
bot.post_tweet(f"Bot status update at {timestamp} ✅")

# Post daily summary
summary = """
📊 Daily Summary - Oct 13, 2025

✅ Tasks completed: 15
🔄 In progress: 3
📈 Productivity: High

#automation #productivity
"""
bot.post_tweet(summary)

# Schedule-like behavior (you'd combine with a scheduler)
def post_good_morning():
    bot.post_tweet("Good morning! ☀️ Have a great day!")

def post_good_night():
    bot.post_tweet("Good night! 🌙 Rest well!")
```

---

## Features

### ✅ Supported Features

- ✅ Post text tweets (up to 280 characters)
- ✅ Post tweets with images (up to 4 images)
- ✅ Reply to tweets
- ✅ Delete tweets
- ✅ Retrieve your recent tweets
- ✅ View tweet metrics (likes, retweets, replies)
- ✅ Automatic character truncation
- ✅ Rate limit handling
- ✅ Secure credential management
- ✅ Command-line interface
- ✅ Python API

### 🔄 Coming Soon / Ideas

- 📹 Video uploads
- 🧵 Thread posting
- 📊 Poll creation
- 🔍 Search tweets
- ❤️ Like/Retweet functionality
- 📅 Scheduled tweets
- 🤖 Automated responses

---

## Troubleshooting

### Authentication Failed

**Problem**: `Authentication failed` error

**Solutions**:
1. Double-check your API credentials in `x_credentials.json`
2. Ensure there are no extra spaces or quotes
3. Verify your app has **Read and Write** permissions
4. Regenerate your access tokens in the Developer Portal
5. Make sure your X Developer account is active

### 403 Forbidden Error

**Problem**: `403 Forbidden` when posting

**Solutions**:
1. Check app permissions (Settings → User authentication settings)
2. Set permissions to **Read and Write**
3. After changing permissions, regenerate your access tokens
4. Verify your X account email is confirmed
5. Check if your account has any restrictions

### Rate Limit Exceeded

**Problem**: `429 Too Many Requests` error

**Solution**:
- X has rate limits for API usage
- Free tier: 50 tweets per 24 hours
- Wait and try again later
- The bot has `wait_on_rate_limit=True` to handle this automatically

### Media Upload Failed

**Problem**: Image upload errors

**Solutions**:
1. Ensure image file exists and path is correct
2. Check image format (supported: JPG, PNG, GIF, WEBP)
3. Verify image size is under 5MB
4. Ensure you have **Read and Write** permissions

### Tweet Too Long

**Problem**: Tweet exceeds 280 characters

**Solution**:
- The bot automatically truncates to 280 characters
- Manually shorten your message
- Use threads for longer content (feature coming soon)

### Credentials Not Found

**Problem**: `Credentials not found` warning

**Solutions**:
1. Run `python3 x_bot.py --setup` to create template
2. Make sure `x_credentials.json` is in the same directory
3. Or set environment variables
4. Use `--credentials` flag to specify custom file location

---

## API Limits (Free Tier)

X API Free Tier limits:
- **Tweets**: 50 posts per 24 hours
- **Read requests**: 10,000 per month
- **Users lookup**: 10,000 per month

For higher limits, consider upgrading to:
- **Basic**: $100/month (3,000 posts/month)
- **Pro**: $5,000/month (300,000 posts/month)

---

## Security Best Practices

1. **Never commit credentials to git**:
   ```bash
   # Add to .gitignore
   echo "x_credentials.json" >> .gitignore
   ```

2. **Use environment variables in production**

3. **Regenerate tokens if compromised**

4. **Use separate apps for dev/prod**

5. **Limit app permissions to what you need**

6. **Regularly audit your X apps** at [developer.twitter.com/en/portal/dashboard](https://developer.twitter.com/en/portal/dashboard)

---

## Examples

### Example 1: Daily Motivational Quotes

```python
import random
from x_bot import XBot

quotes = [
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Innovation distinguishes between a leader and a follower. - Steve Jobs",
    "Stay hungry, stay foolish. - Steve Jobs"
]

bot = XBot()
quote = random.choice(quotes)
bot.post_tweet(f"💡 Daily Quote:\n\n{quote}")
```

### Example 2: Status Monitoring

```python
from x_bot import XBot
import psutil

bot = XBot()

# Get system stats
cpu = psutil.cpu_percent()
memory = psutil.virtual_memory().percent

status = f"""
🖥️ System Status Update

CPU: {cpu}%
Memory: {memory}%
Status: {"✅ Healthy" if cpu < 80 else "⚠️ High Load"}

Last checked: {datetime.now().strftime("%H:%M:%S")}
"""

bot.post_tweet(status)
```

### Example 3: Automated Announcements

```python
from x_bot import XBot

bot = XBot()

announcement = """
📢 New Feature Released!

We just launched our new stress testing tool with:
• 4 intensity levels
• Real-time monitoring
• Cross-platform support

Check it out! 🚀

#coding #devtools
"""

bot.post_tweet(announcement)
```

---

## Support

If you encounter issues:

1. Check this guide's [Troubleshooting](#troubleshooting) section
2. Review X API documentation: [developer.twitter.com/en/docs](https://developer.twitter.com/en/docs)
3. Check X API status: [api.twitterstat.us](https://api.twitterstat.us/)
4. Review tweepy documentation: [docs.tweepy.org](https://docs.tweepy.org/)

---

## Resources

- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Tweepy Documentation](https://docs.tweepy.org/)
- [X API Rate Limits](https://developer.twitter.com/en/docs/twitter-api/rate-limits)

---

**Happy Tweeting! 🐦✨**

