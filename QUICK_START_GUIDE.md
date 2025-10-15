# X Bot - Quick Start Guide 🚀

## ✅ Working Version - Browser Interface

Your X Bot works perfectly in the browser! Here's how to use it:

### Step 1: Start the Server

```bash
cd ~/Documents/Coding\ Projects/x-twitter-bot
python3 x_bot_web.py
```

### Step 2: Open Browser

Open any browser (Safari, Chrome, Firefox) and go to:
```
http://127.0.0.1:5000
```
or
```
http://localhost:5000
```

### Step 3: Use the Beautiful Interface!

You'll see:
- 🌌 Purple gradient background
- 💎 Dark glass panel
- 📝 Text area to compose tweets
- 📸 File upload button for images
- 🚀 Post Tweet button

---

## 📸 Posting with Images

### In Browser:
1. Click "Choose File" button
2. Select up to 4 images
3. Write your tweet
4. Click "Post Tweet"

### Command Line (Alternative):
```bash
python3 x_bot.py --post "Your tweet" --media image.jpg
```

---

## 🎯 All Available Versions

| Version | Command | Best For |
|---------|---------|----------|
| **Web Browser** | `python3 x_bot_web.py` | ✅ **BEST - Works perfectly with images** |
| Desktop App (Instant) | `python3 x_bot_app_instant.py` | Text-only posting |
| Desktop App (Enhanced) | `python3 x_bot_app_enhanced.py` | Scheduling features |
| Command Line | `python3 x_bot.py --post "text"` | Quick posting with images |

---

## 🔧 Troubleshooting

### Browser Won't Open?
Manually type in browser: `http://127.0.0.1:5000`

### Port Already in Use?
The server might still be running. Kill it with:
```bash
pkill -f x_bot_web.py
```

### Rate Limit Error?
Wait 15 minutes, or the GUI will still open (just can't post yet)

---

## 💡 Recommended Workflow

**For Posting Tweets (especially with images):**
```bash
# Terminal 1: Start server
python3 x_bot_web.py

# Browser: Open http://127.0.0.1:5000
```

**For Quick Command-Line Posts:**
```bash
python3 x_bot.py --post "Quick tweet!"
```

---

**Your X Bot is fully functional and beautiful! 🐦✨**

