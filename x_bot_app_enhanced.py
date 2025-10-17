#!/usr/bin/env python3
"""
X Bot Enhanced App - Full-Featured Desktop App
Features: Scheduling, Auto-Reply, Keyword Monitoring, Beautiful Dark Glass UI
"""

import webview
import threading
from flask import Flask, render_template_string, request, jsonify
from x_bot_enhanced import XBotEnhanced
from datetime import datetime, timedelta
import time

app = Flask(__name__)

# Initialize enhanced bot
bot = None
authenticated = False

def lazy_init_bot():
    """Initialize bot only when needed"""
    global bot, authenticated
    if bot is None:
        try:
            bot = XBotEnhanced()
            if bot.client:
                authenticated = True
        except Exception as e:
            print(f"Bot init note: {e}")
            authenticated = False
    return bot, authenticated

# Beautiful Enhanced HTML with all features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>X Bot Enhanced</title>
    <meta charset="utf-8">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: transparent;
            min-height: 100vh;
            padding: 20px;
            overflow-y: auto;
        }
        
        .container {
            background: rgba(20, 20, 35, 0.85);
            backdrop-filter: blur(40px) saturate(150%);
            -webkit-backdrop-filter: blur(40px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6);
            max-width: 800px;
            margin: 0 auto;
            padding: 30px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 25px;
        }
        
        h1 {
            color: #1DA1F2;
            font-size: 32px;
            margin-bottom: 5px;
            text-shadow: 0 0 20px rgba(29, 161, 242, 0.5);
        }
        
        .subtitle {
            color: #B8C5D0;
            font-size: 14px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 25px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        .tab {
            padding: 12px 20px;
            background: transparent;
            border: none;
            color: #8899A6;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            transition: all 0.3s;
        }
        
        .tab:hover {
            color: #B8C5D0;
        }
        
        .tab.active {
            color: #1DA1F2;
            border-bottom-color: #1DA1F2;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #E8F5FD;
            margin-bottom: 8px;
            font-size: 13px;
        }
        
        textarea, input[type="text"], input[type="datetime-local"], select {
            width: 100%;
            padding: 12px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            background: rgba(45, 51, 89, 0.5);
            color: white;
            transition: all 0.3s;
        }
        
        textarea {
            resize: vertical;
            min-height: 120px;
        }
        
        input::placeholder, textarea::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }
        
        textarea:focus, input:focus, select:focus {
            outline: none;
            border-color: #1DA1F2;
            background: rgba(45, 51, 89, 0.7);
            box-shadow: 0 0 15px rgba(29, 161, 242, 0.2);
        }
        
        select {
            cursor: pointer;
        }
        
        select option {
            background: #2D3359;
            color: white;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .char-count {
            text-align: right;
            margin-top: 5px;
            font-size: 12px;
            color: #8899A6;
            margin-bottom: 15px;
        }
        
        .char-count.warning { color: #FFAD1F; }
        .char-count.error { color: #E0245E; }
        
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #1DA1F2;
            color: white;
        }
        
        .btn-primary:hover {
            background: #1A91DA;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(29,161,242,0.4);
        }
        
        .btn-secondary {
            background: rgba(101, 119, 134, 0.3);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .btn-secondary:hover {
            background: rgba(101, 119, 134, 0.5);
        }
        
        .btn-success {
            background: #17BF63;
            color: white;
        }
        
        .btn-success:hover {
            background: #14A456;
        }
        
        .btn-danger {
            background: #E0245E;
            color: white;
        }
        
        .btn-danger:hover {
            background: #C21F4F;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
            margin-top: 15px;
        }
        
        .scheduled-list {
            background: rgba(25, 39, 52, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
        }
        
        .scheduled-item {
            background: rgba(45, 51, 89, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }
        
        .scheduled-item:last-child {
            margin-bottom: 0;
        }
        
        .scheduled-time {
            color: #1DA1F2;
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .scheduled-text {
            color: #E8F5FD;
            font-size: 13px;
            margin-bottom: 8px;
        }
        
        .log {
            background: rgba(25, 39, 52, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            max-height: 200px;
            overflow-y: auto;
            font-size: 12px;
            font-family: 'Monaco', 'Courier New', monospace;
            margin-top: 20px;
        }
        
        .log-entry {
            margin-bottom: 5px;
            color: #B8C5D0;
        }
        
        .log-entry .time {
            color: #657786;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        input[type="checkbox"] {
            width: auto;
            cursor: pointer;
        }
        
        .keyword-item {
            background: rgba(45, 51, 89, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 8px 12px;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin: 5px;
        }
        
        .keyword-text {
            color: #E8F5FD;
            font-size: 13px;
        }
        
        .remove-keyword {
            background: #E0245E;
            border: none;
            color: white;
            border-radius: 4px;
            padding: 2px 8px;
            cursor: pointer;
            font-size: 11px;
        }
        
        .info-box {
            background: rgba(29, 161, 242, 0.1);
            border: 1px solid rgba(29, 161, 242, 0.3);
            border-radius: 8px;
            padding: 12px;
            color: #B8C5D0;
            font-size: 12px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 X Bot Enhanced</h1>
            <p class="subtitle">Schedule · Auto-Reply · Monitor Keywords</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('compose')">✍️ Compose</button>
            <button class="tab" onclick="showTab('schedule')">📅 Schedule</button>
            <button class="tab" onclick="showTab('scheduled')">📋 Scheduled</button>
            <button class="tab" onclick="showTab('autoreply')">🤖 Auto-Reply</button>
        </div>
        
        <!-- Compose Tab -->
        <div id="compose" class="tab-content active">
            <form id="tweetForm">
                <div class="form-group">
                    <label for="tweetText">Compose Your Tweet</label>
                    <textarea id="tweetText" placeholder="What's happening?" maxlength="280"></textarea>
                    <div class="char-count" id="charCount">0 / 280</div>
                </div>
                
                <button type="submit" class="btn-primary">🚀 Post Now</button>
                <button type="button" class="btn-secondary" onclick="clearTweet()">🗑️ Clear</button>
            </form>
        </div>
        
        <!-- Schedule Tab -->
        <div id="schedule" class="tab-content">
            <div class="info-box">
                📅 Schedule tweets to post automatically at a specific date and time
            </div>
            
            <form id="scheduleForm">
                <div class="form-group">
                    <label for="scheduleTweet">Tweet Text</label>
                    <textarea id="scheduleTweet" placeholder="Your scheduled tweet..." maxlength="280"></textarea>
                    <div class="char-count" id="scheduleCharCount">0 / 280</div>
                </div>
                
                <div class="form-group">
                    <label for="scheduleTime">When to Post</label>
                    <input type="datetime-local" id="scheduleTime">
                </div>
                
                <button type="submit" class="btn-success">📅 Schedule Tweet</button>
                <button type="button" class="btn-secondary" onclick="clearSchedule()">🗑️ Clear</button>
            </form>
        </div>
        
        <!-- Scheduled Tweets Tab -->
        <div id="scheduled" class="tab-content">
            <div class="info-box">
                📋 View and manage your scheduled tweets
            </div>
            
            <button class="btn-primary" onclick="refreshScheduled()">🔄 Refresh List</button>
            
            <div class="scheduled-list" id="scheduledList" style="margin-top: 15px;">
                <p style="color: #8899A6; text-align: center;">Loading...</p>
            </div>
        </div>
        
        <!-- Auto-Reply Tab -->
        <div id="autoreply" class="tab-content">
            <div class="info-box">
                🤖 Automatically reply to tweets containing specific keywords
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="autoReplyEnabled">
                    <label for="autoReplyEnabled" style="margin-bottom: 0;">Enable Auto-Reply</label>
                </div>
            </div>
            
            <div class="form-group">
                <label>Keywords to Monitor</label>
                <input type="text" id="newKeyword" placeholder="Enter a keyword">
                <button type="button" class="btn-primary" onclick="addKeyword()" style="margin-top: 8px;">➕ Add Keyword</button>
                
                <div id="keywordsList" style="margin-top: 10px;"></div>
            </div>
            
            <div class="form-group">
                <label for="autoReplyMessage">Reply Message Template</label>
                <textarea id="autoReplyMessage" placeholder="Thanks for mentioning us! {username}"></textarea>
            </div>
            
            <button class="btn-success" onclick="saveAutoReply()">💾 Save Settings</button>
        </div>
        
        <div class="log" id="activityLog"></div>
    </div>
    
    <script>
        let keywords = [];
        
        // Tab switching
        function showTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            if (tabName === 'scheduled') {
                refreshScheduled();
            }
        }
        
        // Character counting
        document.getElementById('tweetText').addEventListener('input', function() {
            updateCharCount(this.value, 'charCount');
        });
        
        document.getElementById('scheduleTweet').addEventListener('input', function() {
            updateCharCount(this.value, 'scheduleCharCount');
        });
        
        function updateCharCount(text, elementId) {
            const count = text.length;
            const el = document.getElementById(elementId);
            el.textContent = count + ' / 280';
            
            el.classList.remove('warning', 'error');
            if (count > 280) el.classList.add('error');
            else if (count > 260) el.classList.add('warning');
        }
        
        // Logging
        function log(message) {
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span class="time">[${time}]</span> ${message}`;
            activityLog.insertBefore(entry, activityLog.firstChild);
        }
        
        // Post tweet
        document.getElementById('tweetForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const text = document.getElementById('tweetText').value.trim();
            
            if (!text) {
                alert('Please write something!');
                return;
            }
            
            log('📤 Posting tweet...');
            
            try {
                const res = await fetch('/post', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text})
                });
                
                const data = await res.json();
                
                if (data.success) {
                    log('✅ Tweet posted! ID: ' + data.tweet_id);
                    alert('Success! Tweet posted!');
                    clearTweet();
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
                alert('Error: ' + error);
            }
        });
        
        // Schedule tweet
        document.getElementById('scheduleForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const text = document.getElementById('scheduleTweet').value.trim();
            const time = document.getElementById('scheduleTime').value;
            
            if (!text || !time) {
                alert('Please fill in both fields!');
                return;
            }
            
            log('📅 Scheduling tweet...');
            
            try {
                const res = await fetch('/schedule', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text, scheduled_time: time})
                });
                
                const data = await res.json();
                
                if (data.success) {
                    log('✅ Tweet scheduled for ' + time);
                    alert('Success! Tweet scheduled!');
                    clearSchedule();
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
                alert('Error: ' + error);
            }
        });
        
        // Refresh scheduled tweets
        async function refreshScheduled() {
            const list = document.getElementById('scheduledList');
            list.innerHTML = '<p style="color: #8899A6; text-align: center;">Loading...</p>';
            
            try {
                const res = await fetch('/get-scheduled');
                const data = await res.json();
                
                if (data.success && data.tweets.length > 0) {
                    list.innerHTML = '';
                    data.tweets.forEach(tweet => {
                        const item = document.createElement('div');
                        item.className = 'scheduled-item';
                        item.innerHTML = `
                            <div class="scheduled-time">📅 ${new Date(tweet.scheduled_time).toLocaleString()}</div>
                            <div class="scheduled-text">${tweet.text}</div>
                            <button class="btn-danger" style="font-size: 12px; padding: 6px 12px;" onclick="cancelScheduled(${tweet.id})">❌ Cancel</button>
                        `;
                        list.appendChild(item);
                    });
                } else {
                    list.innerHTML = '<p style="color: #8899A6; text-align: center;">No scheduled tweets</p>';
                }
            } catch (error) {
                list.innerHTML = '<p style="color: #E0245E; text-align: center;">Error loading tweets</p>';
            }
        }
        
        // Cancel scheduled tweet
        async function cancelScheduled(id) {
            if (!confirm('Cancel this scheduled tweet?')) return;
            
            try {
                const res = await fetch('/cancel-scheduled', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id})
                });
                
                const data = await res.json();
                if (data.success) {
                    log('✅ Scheduled tweet cancelled');
                    refreshScheduled();
                }
            } catch (error) {
                alert('Error: ' + error);
            }
        }
        
        // Keyword management
        function addKeyword() {
            const input = document.getElementById('newKeyword');
            const keyword = input.value.trim();
            
            if (!keyword) return;
            if (keywords.includes(keyword)) {
                alert('Keyword already added!');
                return;
            }
            
            keywords.push(keyword);
            updateKeywordsList();
            input.value = '';
        }
        
        function removeKeyword(keyword) {
            keywords = keywords.filter(k => k !== keyword);
            updateKeywordsList();
        }
        
        function updateKeywordsList() {
            const list = document.getElementById('keywordsList');
            
            if (keywords.length === 0) {
                list.innerHTML = '<p style="color: #8899A6; font-size: 12px;">No keywords added</p>';
                return;
            }
            
            list.innerHTML = keywords.map(k => `
                <div class="keyword-item">
                    <span class="keyword-text">${k}</span>
                    <button class="remove-keyword" onclick="removeKeyword('${k}')">✕</button>
                </div>
            `).join('');
        }
        
        // Save auto-reply settings
        async function saveAutoReply() {
            const enabled = document.getElementById('autoReplyEnabled').checked;
            const message = document.getElementById('autoReplyMessage').value;
            
            log('💾 Saving auto-reply settings...');
            
            try {
                const res = await fetch('/save-autoreply', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({enabled, keywords, message})
                });
                
                const data = await res.json();
                if (data.success) {
                    log('✅ Auto-reply settings saved!');
                    alert('Settings saved!');
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
                alert('Error: ' + error);
            }
        }
        
        // Clear functions
        function clearTweet() {
            document.getElementById('tweetText').value = '';
            updateCharCount('', 'charCount');
        }
        
        function clearSchedule() {
            document.getElementById('scheduleTweet').value = '';
            document.getElementById('scheduleTime').value = '';
            updateCharCount('', 'scheduleCharCount');
        }
        
        // Initial setup
        updateKeywordsList();
        log('✨ Enhanced GUI ready!');
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/post', methods=['POST'])
def post_tweet():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    data = request.json
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'success': False, 'error': 'Empty tweet'})
    
    try:
        # XBotEnhanced returns the tweet_id string directly, not a response object
        response = bot.post_tweet(text)
        if response:
            return jsonify({'success': True, 'tweet_id': response})
        return jsonify({'success': False, 'error': 'Failed to post tweet'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/schedule', methods=['POST'])
def schedule_tweet():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    data = request.json
    text = data.get('text', '').strip()
    scheduled_time = data.get('scheduled_time')
    
    if not text or not scheduled_time:
        return jsonify({'success': False, 'error': 'Missing data'})
    
    try:
        # Convert to datetime
        scheduled_dt = datetime.fromisoformat(scheduled_time)
        tweet_id = bot.schedule_tweet(text, scheduled_dt)
        return jsonify({'success': True, 'id': tweet_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-scheduled')
def get_scheduled():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        tweets = bot.get_scheduled_tweets()
        return jsonify({'success': True, 'tweets': tweets})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/cancel-scheduled', methods=['POST'])
def cancel_scheduled():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    data = request.json
    tweet_id = data.get('id')
    
    try:
        bot.cancel_scheduled_tweet(tweet_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/save-autoreply', methods=['POST'])
def save_autoreply():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    data = request.json
    enabled = data.get('enabled', False)
    keywords = data.get('keywords', [])
    message = data.get('message', '')
    
    try:
        # Configure auto-reply
        bot.auto_reply_config['enabled'] = enabled
        bot.auto_reply_config['keywords'] = {kw: message for kw in keywords}
        
        if enabled and not bot.auto_reply_running:
            bot.start_auto_reply()
        elif not enabled and bot.auto_reply_running:
            bot.stop_auto_reply()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def start_flask():
    """Start Flask in background thread"""
    app.run(port=5001, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("\n🚀 X Bot Enhanced - Loading features...\n")
    
    # Start Flask server
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Give Flask time to start
    time.sleep(1)
    
    # Create native window
    window = webview.create_window(
        'X Bot Enhanced',
        'http://127.0.0.1:5001',
        width=850,
        height=900,
        resizable=True,
        min_size=(700, 800),
        transparent=True
    )
    
    # Start scheduler in background if bot is initialized
    def start_scheduler_thread():
        time.sleep(2)
        bot, auth = lazy_init_bot()
        if auth and bot:
            bot.start_scheduler()
    
    scheduler_thread = threading.Thread(target=start_scheduler_thread, daemon=True)
    scheduler_thread.start()
    
    # Start the application
    webview.start()

