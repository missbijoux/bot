# X Bot (Twitter Bot) 🐦

A simple, powerful Python bot for posting to X (formerly Twitter) via the API.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Credentials

Create a credentials file:

```bash
python3 x_bot.py --setup
```

Edit `x_credentials.json` with your X API credentials. See **[X_BOT_SETUP.md](X_BOT_SETUP.md)** for detailed instructions on getting API credentials.

### 3. Post Your First Tweet

**Option A: Use the GUI (Easy!)** 🎨

```bash
python3 x_bot_gui.py
```

**Option B: Use Command Line**

```bash
python3 x_bot.py --post "Hello from my X bot! 🤖"
```

---

## Features

✅ **Graphical Interface (GUI)** - User-friendly window to compose and post tweets  

✅ **Post Tweets** - Simple text tweets or with images  
✅ **Reply to Tweets** - Engage in conversations  
✅ **Delete Tweets** - Remove tweets programmatically  
✅ **Get Timeline** - Retrieve your recent tweets  
✅ **Media Support** - Upload up to 4 images per tweet  
✅ **Rate Limit Handling** - Automatic rate limit management  
✅ **Secure** - Credentials file not tracked in git  

---

## Usage Examples

### Graphical Interface (GUI) - Easiest Way! 🎨

Launch the GUI for a user-friendly experience:

```bash
python3 x_bot_gui.py
```

**GUI Features:**
- ✨ Large text area for composing tweets
- 📊 Real-time character counter (0/280)
- 📸 Add up to 4 images with file picker
- 🚀 One-click posting
- 📥 View recent tweets with engagement stats
- 📋 Activity log showing all actions

### Command Line

```bash
# Post a simple tweet
python3 x_bot.py --post "Hello World! 👋"

# Post with an image
python3 x_bot.py --post "Check this out!" --media photo.jpg

# Reply to a tweet
python3 x_bot.py --post "Thanks!" --reply-to 1234567890

# Get your recent tweets
python3 x_bot.py --get-tweets

# Delete a tweet
python3 x_bot.py --delete 1234567890
```

### Python Code

```python
from x_bot import XBot

# Initialize bot
bot = XBot()

# Post a tweet
bot.post_tweet("Hello from Python! 🐍")

# Post with media
bot.post_tweet_with_media("Check out these images!", ["img1.jpg", "img2.jpg"])

# Get your tweets
tweets = bot.get_my_tweets(max_results=10)

# Delete a tweet
bot.delete_tweet("1234567890")
```

---

## Documentation

📖 **[Complete Setup Guide](X_BOT_SETUP.md)** - Detailed instructions on getting API credentials and configuration  
📝 **[Examples](x_bot_examples.py)** - More examples including threads, scheduled posts, and more  

---

## API Credentials

You need X API credentials to use this bot. Get them from the [X Developer Portal](https://developer.twitter.com/).

### Free Tier Limits
- 50 tweets per 24 hours
- 10,000 read requests per month

See **[X_BOT_SETUP.md](X_BOT_SETUP.md)** for complete instructions.

---

## Security

⚠️ **Important**: Never commit your `x_credentials.json` file to version control!

The credentials file is already added to `.gitignore` for your protection.

---

## Troubleshooting

### Authentication Failed
- Double-check your credentials in `x_credentials.json`
- Ensure app has **Read and Write** permissions
- Regenerate access tokens if needed

### 403 Forbidden
- Verify app permissions are set to **Read and Write**
- Regenerate tokens after changing permissions
- Confirm your email on X

### Rate Limit Exceeded
- Free tier: 50 tweets per 24 hours
- Wait and try again
- Consider upgrading to paid tier for higher limits

See **[X_BOT_SETUP.md](X_BOT_SETUP.md)** for more troubleshooting.

---

## Command Reference

```bash
# Post a tweet
--post "text"              Post a tweet with the given text

# Add media
--media file1.jpg ...      Attach images to tweet (up to 4)

# Reply
--reply-to tweet_id        Reply to a specific tweet

# Get tweets
--get-tweets               Get your recent tweets
--max-results N            Number of tweets to retrieve (default: 10)

# Delete
--delete tweet_id          Delete a tweet by ID

# Setup
--setup                    Create credentials template file

# Custom credentials
--credentials path.json    Use custom credentials file path
```

---

## Examples

Run the interactive examples:

```bash
python3 x_bot_examples.py
```

Examples include:
1. Simple tweet
2. Tweet with image
3. Status update
4. Announcement
5. Get recent tweets
6. Reply to tweet
7. Scheduled posts
8. Thread simulation
9. Daily stats
10. Error handling

---

## Integration Ideas

- **Automated Status Updates**: Post system status, monitoring alerts
- **Social Media Automation**: Schedule announcements, updates
- **Bot Responses**: Auto-reply to mentions or keywords
- **Content Sharing**: Share blog posts, articles automatically
- **Daily Summaries**: Post daily stats, reports, or quotes
- **Monitoring Bot**: Tweet alerts from monitoring systems

---

## Resources

- [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
- [X API Documentation](https://developer.twitter.com/en/docs/twitter-api)
- [Tweepy Documentation](https://docs.tweepy.org/)

---

## Support

For detailed setup instructions and troubleshooting, see **[X_BOT_SETUP.md](X_BOT_SETUP.md)**.

---

**Happy Tweeting! 🐦✨**

