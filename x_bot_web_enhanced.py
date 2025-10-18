#!/usr/bin/env python3
"""
X Bot Enhanced Web GUI - Full-Featured with Scheduling and Auto-Reply
Beautiful dark glass UI with tabs for all features
"""

from flask import Flask, render_template_string, request, jsonify
from x_bot_enhanced import XBotEnhanced
import threading
import webbrowser
import os
from datetime import datetime
import json

app = Flask(__name__)

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
                # Start scheduler automatically
                if not bot.scheduler_running:
                    bot.start_scheduler()
        except Exception as e:
            print(f"Bot init: {e}")
            authenticated = False
    return bot, authenticated

# Enhanced HTML with all features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>X Bot Enhanced</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: url('https://i.pinimg.com/1200x/9b/10/4b/9b104b15789a07b8b595d552befd1c26.jpg') center center / cover no-repeat fixed;
            background-color: #0f0c29; /* Fallback color */
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            background: rgba(20, 20, 35, 0.85);
            backdrop-filter: blur(40px) saturate(150%);
            -webkit-backdrop-filter: blur(40px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6), 0 0 100px rgba(29, 161, 242, 0.15);
            max-width: 900px;
            margin: 0 auto;
            padding: 35px;
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
            font-size: 13px;
        }
        
        .tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 25px;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
            overflow-x: auto;
        }
        
        .tab {
            padding: 12px 18px;
            background: transparent;
            border: none;
            color: #8899A6;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            border-bottom: 2px solid transparent;
            margin-bottom: -2px;
            transition: all 0.3s;
            white-space: nowrap;
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
            margin-bottom: 6px;
            font-size: 13px;
        }
        
        textarea, input[type="text"], input[type="datetime-local"], input[type="number"] {
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
        
        textarea::placeholder, input::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }
        
        textarea:focus, input:focus {
            outline: none;
            border-color: #1DA1F2;
            background: rgba(45, 51, 89, 0.7);
            box-shadow: 0 0 15px rgba(29, 161, 242, 0.2);
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .char-count {
            text-align: right;
            margin-top: 4px;
            font-size: 12px;
            color: #8899A6;
        }
        
        .char-count.warning { color: #FFAD1F; }
        .char-count.error { color: #E0245E; }
        
        button {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-right: 8px;
            margin-bottom: 8px;
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
        
        .info-box {
            background: rgba(29, 161, 242, 0.1);
            border: 1px solid rgba(29, 161, 242, 0.3);
            border-radius: 8px;
            padding: 12px;
            color: #B8C5D0;
            font-size: 12px;
            margin-bottom: 15px;
        }
        
        .scheduled-list, .keyword-list {
            background: rgba(25, 39, 52, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            max-height: 350px;
            overflow-y: auto;
            margin-top: 15px;
        }
        
        .scheduled-item, .keyword-item-box {
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
            font-size: 11px;
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
            max-height: 180px;
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
            width: 18px;
            height: 18px;
            cursor: pointer;
        }
        
        .keyword-tag {
            display: inline-block;
            background: rgba(29, 161, 242, 0.2);
            border: 1px solid rgba(29, 161, 242, 0.4);
            border-radius: 16px;
            padding: 6px 12px;
            margin: 4px;
            color: #1DA1F2;
            font-size: 12px;
        }
        
        .keyword-tag button {
            background: none;
            border: none;
            color: #E0245E;
            cursor: pointer;
            margin: 0;
            padding: 0 0 0 8px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 X Bot Enhanced</h1>
            <p class="subtitle">Schedule · Auto-Reply · Monitor Keywords · Post with Images</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('compose')">✍️ Compose</button>
            <button class="tab" onclick="showTab('schedule')">📅 Schedule</button>
            <button class="tab" onclick="showTab('scheduled')">📋 Scheduled Tweets</button>
            <button class="tab" onclick="showTab('autoreply')">🤖 Auto-Reply</button>
        </div>
        
        <!-- Compose Tab -->
        <div id="compose" class="tab-content active">
            <form id="tweetForm">
                <div class="form-group">
                    <label>Compose Your Tweet</label>
                    <textarea id="tweetText" placeholder="What's happening?" maxlength="280"></textarea>
                    <div class="char-count" id="charCount">0 / 280</div>
                </div>
                
                <div class="form-group">
                    <label>Attach Images (up to 4)</label>
                    <input type="file" id="imageInput" accept="image/*" multiple>
                    <div id="selectedFiles" style="margin-top: 8px; color: #8899A6; font-size: 12px;">No images selected</div>
                </div>
                
                <button type="submit" class="btn-primary">🚀 Post Now</button>
                <button type="button" class="btn-secondary" onclick="clearCompose()">🗑️ Clear</button>
            </form>
        </div>
        
        <!-- Schedule Tab -->
        <div id="schedule" class="tab-content">
            <div class="info-box">
                📅 Schedule tweets to post automatically at a future date and time (with images!)
            </div>
            
            <form id="scheduleForm">
                <div class="form-group">
                    <label>Tweet Text</label>
                    <textarea id="scheduleTweet" placeholder="Your scheduled tweet..." maxlength="280"></textarea>
                    <div class="char-count" id="scheduleCharCount">0 / 280</div>
                </div>
                
                <div class="form-group">
                    <label>Attach Images (Optional - up to 4)</label>
                    <input type="file" id="scheduleImageInput" accept="image/*" multiple>
                    <div id="scheduleSelectedFiles" style="margin-top: 8px; color: #8899A6; font-size: 12px;">No images selected</div>
                </div>
                
                <div class="form-group">
                    <label>When to Post</label>
                    <input type="datetime-local" id="scheduleTime">
                </div>
                
                <button type="submit" class="btn-success">📅 Schedule Tweet</button>
                <button type="button" class="btn-secondary" onclick="clearSchedule()">🗑️ Clear</button>
            </form>
        </div>
        
        <!-- Scheduled Tweets Tab -->
        <div id="scheduled" class="tab-content">
            <div class="info-box">
                📋 View and manage your scheduled tweets. They will post automatically!
            </div>
            
            <button class="btn-primary" onclick="refreshScheduled()">🔄 Refresh List</button>
            
            <div class="scheduled-list" id="scheduledList">
                <p style="color: #8899A6; text-align: center;">Click refresh to load scheduled tweets</p>
            </div>
        </div>
        
        <!-- Auto-Reply Tab -->
        <div id="autoreply" class="tab-content">
            <div class="info-box">
                🤖 Automatically reply to tweets that mention specific keywords
            </div>
            
            <div class="form-group">
                <div class="checkbox-group">
                    <input type="checkbox" id="autoReplyEnabled">
                    <label for="autoReplyEnabled" style="margin-bottom: 0; cursor: pointer;">Enable Auto-Reply</label>
                </div>
            </div>
            
            <div class="form-group">
                <label>Keywords to Monitor</label>
                <div style="display: flex; gap: 8px;">
                    <input type="text" id="newKeyword" placeholder="Enter keyword (e.g., @yourbrand)">
                    <button type="button" class="btn-primary" onclick="addKeyword()">➕ Add</button>
                </div>
                <div id="keywordsList" style="margin-top: 10px;"></div>
            </div>
            
            <div class="form-group">
                <label>Reply Message Template</label>
                <textarea id="autoReplyMessage" placeholder="Thanks for mentioning us! We appreciate your support! 🙏"></textarea>
                <p style="color: #8899A6; font-size: 11px; margin-top: 4px;">
                    Tip: Use {username} to mention the user
                </p>
            </div>
            
            <div class="form-group">
                <label>Rate Limits (Safety)</label>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>
                        <input type="number" id="maxReplies" placeholder="10" min="1" max="50" value="10">
                        <p style="color: #8899A6; font-size: 11px; margin-top: 4px;">Max replies per hour</p>
                    </div>
                    <div>
                        <input type="number" id="cooldown" placeholder="30" min="1" max="120" value="30">
                        <p style="color: #8899A6; font-size: 11px; margin-top: 4px;">Cooldown (minutes)</p>
                    </div>
                </div>
            </div>
            
            <button class="btn-success" onclick="saveAutoReply()">💾 Save Settings</button>
            <button class="btn-danger" onclick="stopAutoReply()">⏹️ Stop Auto-Reply</button>
        </div>
        
        <div class="log" id="activityLog"></div>
    </div>
    
    <script>
        let keywords = [];
        const textarea = document.getElementById('tweetText');
        const charCount = document.getElementById('charCount');
        const scheduleTweet = document.getElementById('scheduleTweet');
        const scheduleCharCount = document.getElementById('scheduleCharCount');
        const activityLog = document.getElementById('activityLog');
        const imageInput = document.getElementById('imageInput');
        const selectedFiles = document.getElementById('selectedFiles');
        const scheduleImageInput = document.getElementById('scheduleImageInput');
        const scheduleSelectedFiles = document.getElementById('scheduleSelectedFiles');
        
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
        textarea.addEventListener('input', function() {
            updateCharCount(this.value, charCount);
        });
        
        scheduleTweet.addEventListener('input', function() {
            updateCharCount(this.value, scheduleCharCount);
        });
        
        function updateCharCount(text, element) {
            const count = text.length;
            element.textContent = count + ' / 280';
            element.classList.remove('warning', 'error');
            if (count > 280) element.classList.add('error');
            else if (count > 260) element.classList.add('warning');
        }
        
        // Image selection - Compose tab
        imageInput.addEventListener('change', function() {
            const count = this.files.length;
            if (count > 0) {
                const names = Array.from(this.files).slice(0, 4).map(f => f.name).join(', ');
                selectedFiles.innerHTML = `<span style="color: #17BF63;">✅ ${count} image${count > 1 ? 's' : ''} selected:</span> ${names}`;
            } else {
                selectedFiles.textContent = 'No images selected';
            }
        });
        
        // Image selection - Schedule tab
        scheduleImageInput.addEventListener('change', function() {
            const count = this.files.length;
            if (count > 0) {
                const names = Array.from(this.files).slice(0, 4).map(f => f.name).join(', ');
                scheduleSelectedFiles.innerHTML = `<span style="color: #17BF63;">✅ ${count} image${count > 1 ? 's' : ''} selected:</span> ${names}`;
            } else {
                scheduleSelectedFiles.textContent = 'No images selected';
            }
        });
        
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
            const text = textarea.value.trim();
            if (!text) {
                alert('Please write something!');
                return;
            }
            
            const postBtn = e.submitter;
            postBtn.disabled = true;
            postBtn.textContent = '⏳ Posting...';
            
            log('📤 Posting tweet...');
            
            try {
                const formData = new FormData();
                formData.append('text', text);
                
                const files = imageInput.files;
                if (files.length > 0) {
                    for (let i = 0; i < Math.min(files.length, 4); i++) {
                        formData.append('images', files[i]);
                    }
                    log(`📎 Uploading ${files.length} image${files.length > 1 ? 's' : ''}...`);
                }
                
                const response = await fetch('/post', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    log('✅ Tweet posted! ID: ' + data.tweet_id);
                    alert('Success! Tweet posted!');
                    clearCompose();
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
                alert('Error: ' + error);
            }
            
            postBtn.disabled = false;
            postBtn.textContent = '🚀 Post Now';
        });
        
        // Schedule tweet
        document.getElementById('scheduleForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const text = scheduleTweet.value.trim();
            const time = document.getElementById('scheduleTime').value;
            
            if (!text || !time) {
                alert('Please fill in both text and time!');
                return;
            }
            
            log('📅 Scheduling tweet...');
            
            try {
                const formData = new FormData();
                formData.append('text', text);
                formData.append('scheduled_time', time);
                
                // Add images if selected
                const files = scheduleImageInput.files;
                if (files.length > 0) {
                    for (let i = 0; i < Math.min(files.length, 4); i++) {
                        formData.append('images', files[i]);
                    }
                    log(`📎 Scheduling with ${files.length} image${files.length > 1 ? 's' : ''}...`);
                }
                
                const response = await fetch('/schedule', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    log('✅ Tweet scheduled for ' + new Date(time).toLocaleString());
                    alert('Success! Tweet scheduled!');
                    clearSchedule();
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
            }
        });
        
        // Refresh scheduled tweets
        async function refreshScheduled() {
            const list = document.getElementById('scheduledList');
            list.innerHTML = '<p style="color: #8899A6; text-align: center;">Loading...</p>';
            
            try {
                const response = await fetch('/get-scheduled');
                const data = await response.json();
                
                if (data.success && data.tweets.length > 0) {
                    list.innerHTML = '';
                    data.tweets.forEach(tweet => {
                        const item = document.createElement('div');
                        item.className = 'scheduled-item';
                        item.innerHTML = `
                            <div class="scheduled-time">📅 ${new Date(tweet.scheduled_time).toLocaleString()}</div>
                            <div class="scheduled-text">${tweet.text}</div>
                            <button class="btn-danger" style="font-size: 11px; padding: 6px 12px;" onclick="cancelScheduled(${tweet.id})">❌ Cancel</button>
                        `;
                        list.appendChild(item);
                    });
                    log(`✅ Loaded ${data.tweets.length} scheduled tweet${data.tweets.length > 1 ? 's' : ''}`);
                } else {
                    list.innerHTML = '<p style="color: #8899A6; text-align: center;">No scheduled tweets</p>';
                }
            } catch (error) {
                list.innerHTML = '<p style="color: #E0245E; text-align: center;">Error loading</p>';
            }
        }
        
        // Cancel scheduled tweet
        async function cancelScheduled(id) {
            if (!confirm('Cancel this scheduled tweet?')) return;
            
            try {
                const response = await fetch('/cancel-scheduled', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id})
                });
                
                const data = await response.json();
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
            log('➕ Added keyword: ' + keyword);
        }
        
        function removeKeyword(keyword) {
            keywords = keywords.filter(k => k !== keyword);
            updateKeywordsList();
            log('➖ Removed keyword: ' + keyword);
        }
        
        function updateKeywordsList() {
            const list = document.getElementById('keywordsList');
            
            if (keywords.length === 0) {
                list.innerHTML = '<p style="color: #8899A6; font-size: 12px; margin-top: 8px;">No keywords added yet</p>';
                return;
            }
            
            list.innerHTML = keywords.map(k => `
                <span class="keyword-tag">
                    ${k}
                    <button onclick="removeKeyword('${k}')">✕</button>
                </span>
            `).join('');
        }
        
        // Save auto-reply settings
        async function saveAutoReply() {
            const enabled = document.getElementById('autoReplyEnabled').checked;
            const message = document.getElementById('autoReplyMessage').value.trim();
            const maxReplies = parseInt(document.getElementById('maxReplies').value) || 10;
            const cooldown = parseInt(document.getElementById('cooldown').value) || 30;
            
            if (enabled && keywords.length === 0) {
                alert('Please add at least one keyword to monitor!');
                return;
            }
            
            if (enabled && !message) {
                alert('Please enter a reply message!');
                return;
            }
            
            log('💾 Saving auto-reply settings...');
            
            try {
                const response = await fetch('/save-autoreply', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        enabled,
                        keywords,
                        message,
                        max_replies: maxReplies,
                        cooldown
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    log('✅ Auto-reply ' + (enabled ? 'enabled' : 'saved') + '!');
                    alert('Settings saved!' + (enabled ? ' Auto-reply is now active!' : ''));
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
            }
        }
        
        // Stop auto-reply
        async function stopAutoReply() {
            if (!confirm('Stop auto-reply monitoring?')) return;
            
            try {
                const response = await fetch('/stop-autoreply', {
                    method: 'POST'
                });
                
                const data = await response.json();
                if (data.success) {
                    document.getElementById('autoReplyEnabled').checked = false;
                    log('⏹️ Auto-reply stopped');
                    alert('Auto-reply stopped!');
                }
            } catch (error) {
                alert('Error: ' + error);
            }
        }
        
        // Clear functions
        function clearCompose() {
            textarea.value = '';
            imageInput.value = '';
            selectedFiles.textContent = 'No images selected';
            updateCharCount('', charCount);
            log('🗑️ Cleared compose');
        }
        
        function clearSchedule() {
            scheduleTweet.value = '';
            document.getElementById('scheduleTime').value = '';
            scheduleImageInput.value = '';
            scheduleSelectedFiles.textContent = 'No images selected';
            updateCharCount('', scheduleCharCount);
            log('🗑️ Cleared schedule');
        }
        
        // Initialize
        updateKeywordsList();
        log('✨ Enhanced GUI ready! Scheduler running in background.');
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, authenticated=True)

@app.route('/post', methods=['POST'])
def post_tweet():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    text = request.form.get('text', '').strip()
    if not text:
        return jsonify({'success': False, 'error': 'Empty tweet'})
    
    try:
        images = request.files.getlist('images')
        
        if images and len(images) > 0:
            import tempfile
            image_paths = []
            
            for img in images[:4]:
                if img.filename:
                    temp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(img.filename)[1])
                    img.save(temp.name)
                    image_paths.append(temp.name)
                    temp.close()
            
            if image_paths:
                response = bot.post_tweet_with_media(text, image_paths)
                for path in image_paths:
                    try:
                        os.remove(path)
                    except:
                        pass
            else:
                response = bot.post_tweet(text)
        else:
            response = bot.post_tweet(text)
        
        # XBotEnhanced returns the tweet_id string directly, not a response object
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
    
    text = request.form.get('text', '').strip()
    scheduled_time = request.form.get('scheduled_time')
    
    if not text or not scheduled_time:
        return jsonify({'success': False, 'error': 'Missing data'})
    
    try:
        scheduled_dt = datetime.fromisoformat(scheduled_time)
        
        # Check for uploaded images
        images = request.files.getlist('images')
        
        if images and len(images) > 0:
            # Save images to permanent location for scheduled tweet
            import tempfile
            image_dir = os.path.join(os.path.dirname(__file__), 'scheduled_images')
            os.makedirs(image_dir, exist_ok=True)
            
            image_paths = []
            for img in images[:4]:
                if img.filename:
                    # Use timestamp in filename to make it unique
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"{timestamp}_{img.filename}"
                    filepath = os.path.join(image_dir, filename)
                    img.save(filepath)
                    image_paths.append(filepath)
            
            # Schedule with media files
            tweet_id = bot.schedule_tweet(text, scheduled_dt, media_files=image_paths if image_paths else None)
        else:
            # Schedule text only
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
        # Convert tuple format to dict format for frontend
        tweet_list = []
        for tweet in tweets:
            tweet_id, content, scheduled_time, media_files, reply_to_tweet_id = tweet
            tweet_list.append({
                'id': tweet_id,
                'text': content,
                'scheduled_time': scheduled_time
            })
        return jsonify({'success': True, 'tweets': tweet_list})
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
    max_replies = data.get('max_replies', 10)
    cooldown = data.get('cooldown', 30)
    
    try:
        bot.auto_reply_config['enabled'] = enabled
        bot.auto_reply_config['keywords'] = {kw: message for kw in keywords}
        bot.auto_reply_config['max_replies_per_hour'] = max_replies
        bot.auto_reply_config['cooldown_minutes'] = cooldown
        
        if enabled and not bot.auto_reply_running:
            bot.start_auto_reply()
        elif not enabled and bot.auto_reply_running:
            bot.stop_auto_reply()
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stop-autoreply', methods=['POST'])
def stop_autoreply():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        bot.stop_auto_reply()
        bot.auto_reply_config['enabled'] = False
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def open_browser():
    """Open browser after delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5003')

if __name__ == '__main__':
    # Get port from environment variable (for Railway/Heroku) or use 5003 locally
    port = int(os.environ.get('PORT', 5003))
    
    # Only open browser if running locally
    if port == 5003:
        threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n" + "="*60)
    print("🐦 X Bot Enhanced Web Interface")
    print("="*60)
    print(f"\n✨ Running on port: {port}")
    print("💡 Features: Post · Schedule · Auto-Reply · Images")
    print("\n🎯 Press Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', debug=False, port=port)

