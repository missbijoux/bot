#!/usr/bin/env python3
"""
X Bot Web GUI - Beautiful web interface that works perfectly on Mac!
Opens in your browser - no tkinter issues!
"""

from flask import Flask, render_template_string, request, jsonify
from x_bot import XBot
import threading
import webbrowser
import os
from datetime import datetime

app = Flask(__name__)
bot = None
authenticated = False

def lazy_init_bot():
    """Initialize bot only when needed - avoids rate limit at startup"""
    global bot, authenticated
    if bot is None:
        try:
            bot = XBot()
            if bot.client:
                authenticated = True
        except Exception as e:
            print(f"Bot init: {e}")
            authenticated = False
    return bot, authenticated

# HTML Template - Beautiful, modern design
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>X Bot - Tweet Composer</title>
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
            background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: rgba(20, 20, 35, 0.85);
            backdrop-filter: blur(40px) saturate(150%);
            -webkit-backdrop-filter: blur(40px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6), 
                        0 0 100px rgba(29, 161, 242, 0.15);
            max-width: 600px;
            width: 100%;
            padding: 40px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            color: #1DA1F2;
            font-size: 36px;
            margin-bottom: 5px;
            text-shadow: 0 0 20px rgba(29, 161, 242, 0.5);
        }
        
        .subtitle {
            color: #B8C5D0;
            font-size: 16px;
        }
        
        .status {
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        .status.connected {
            background: #E8F5E9;
            color: #2E7D32;
        }
        
        .status.disconnected {
            background: #FFEBEE;
            color: #C62828;
        }
        
        label {
            display: block;
            font-weight: 600;
            color: #E8F5FD;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 150px;
            transition: all 0.3s;
            background: rgba(45, 51, 89, 0.5);
            color: white;
        }
        
        textarea::placeholder {
            color: rgba(255, 255, 255, 0.4);
        }
        
        textarea:focus {
            outline: none;
            border-color: #1DA1F2;
            background: rgba(45, 51, 89, 0.7);
            box-shadow: 0 0 15px rgba(29, 161, 242, 0.2);
        }
        
        .char-count {
            text-align: right;
            margin-top: 5px;
            font-size: 14px;
            color: #8899A6;
            margin-bottom: 20px;
        }
        
        .char-count.warning {
            color: #FFAD1F;
            text-shadow: 0 0 10px rgba(255, 173, 31, 0.5);
        }
        
        .char-count.error {
            color: #E0245E;
            text-shadow: 0 0 10px rgba(224, 36, 94, 0.5);
        }
        
        .file-input {
            margin-bottom: 20px;
        }
        
        input[type="file"] {
            display: none;
        }
        
        .file-label {
            display: inline-block;
            padding: 10px 20px;
            background: rgba(29, 161, 242, 0.3);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .file-label:hover {
            background: rgba(29, 161, 242, 0.5);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .selected-files {
            margin-top: 10px;
            font-size: 14px;
            color: #8899A6;
        }
        
        button {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-bottom: 10px;
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
        
        .btn-primary:disabled {
            background: #AAB8C2;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: rgba(101, 119, 134, 0.3);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .btn-secondary:hover {
            background: rgba(101, 119, 134, 0.5);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .btn-success {
            background: #17BF63;
            color: white;
        }
        
        .btn-success:hover {
            background: #14A456;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
        }
        
        .btn-group button {
            flex: 1;
        }
        
        .activity {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #E1E8ED;
        }
        
        .activity h3 {
            color: #E8F5FD;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .log {
            background: rgba(25, 39, 52, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            max-height: 200px;
            overflow-y: auto;
            font-size: 13px;
            font-family: 'Monaco', 'Courier New', monospace;
        }
        
        .log-entry {
            margin-bottom: 5px;
            color: #B8C5D0;
        }
        
        .log-entry .time {
            color: #657786;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal.show {
            display: flex;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 15px;
            max-width: 500px;
            width: 90%;
            text-align: center;
        }
        
        .modal-content h2 {
            color: #1DA1F2;
            margin-bottom: 15px;
        }
        
        .modal-content button {
            margin-top: 20px;
            width: auto;
            padding: 10px 30px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 X Bot</h1>
            <p class="subtitle">Tweet Composer</p>
        </div>
        
        <div class="status {% if authenticated %}connected{% else %}disconnected{% endif %}">
            {% if authenticated %}
                ✅ Connected & Authenticated
            {% else %}
                ❌ Not Connected - Check Credentials
            {% endif %}
        </div>
        
        <form id="tweetForm">
            <label for="tweetText">Compose Your Tweet</label>
            <textarea 
                id="tweetText" 
                name="text" 
                placeholder="What's happening?"
                maxlength="280"
            ></textarea>
            <div class="char-count" id="charCount">0 / 280</div>
            
            <div class="file-input">
                <label class="file-label" for="imageInput">
                    📎 Attach Images (up to 4)
                </label>
                <input type="file" id="imageInput" accept="image/*" multiple>
                <div class="selected-files" id="selectedFiles">No images selected</div>
            </div>
            
            <button type="submit" class="btn-primary" id="postBtn">
                🚀 Post Tweet
            </button>
        </form>
        
        <div class="btn-group">
            <button class="btn-secondary" onclick="clearTweet()">🗑️ Clear</button>
            <button class="btn-success" onclick="getMyTweets()">📥 My Tweets</button>
        </div>
        
        <div class="activity">
            <h3>Activity Log</h3>
            <div class="log" id="activityLog"></div>
        </div>
    </div>
    
    <div class="modal" id="successModal">
        <div class="modal-content">
            <h2>🎉 Success!</h2>
            <p id="modalMessage"></p>
            <button class="btn-primary" onclick="closeModal()">OK</button>
        </div>
    </div>
    
    <script>
        const textarea = document.getElementById('tweetText');
        const charCount = document.getElementById('charCount');
        const imageInput = document.getElementById('imageInput');
        const selectedFiles = document.getElementById('selectedFiles');
        const activityLog = document.getElementById('activityLog');
        
        // Character counter
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            charCount.textContent = count + ' / 280';
            
            if (count > 280) {
                charCount.classList.add('error');
                charCount.classList.remove('warning');
            } else if (count > 260) {
                charCount.classList.add('warning');
                charCount.classList.remove('error');
            } else {
                charCount.classList.remove('error', 'warning');
            }
        });
        
        // File selection
        imageInput.addEventListener('change', function() {
            const count = this.files.length;
            if (count > 0) {
                selectedFiles.textContent = `✅ ${count} image${count > 1 ? 's' : ''} selected`;
                selectedFiles.style.color = '#17BF63';
            } else {
                selectedFiles.textContent = 'No images selected';
                selectedFiles.style.color = '#657786';
            }
        });
        
        // Log function
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
                alert('Please write something to tweet!');
                return;
            }
            
            const postBtn = document.getElementById('postBtn');
            postBtn.disabled = true;
            postBtn.textContent = '⏳ Posting...';
            
            log('📤 Posting tweet...');
            
            try {
                const response = await fetch('/post', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text})
                });
                
                const data = await response.json();
                
                if (data.success) {
                    log('✅ Tweet posted successfully!');
                    log(`🔗 Tweet ID: ${data.tweet_id}`);
                    showModal('Your tweet was posted successfully!<br>Tweet ID: ' + data.tweet_id);
                    clearTweet();
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Network error: ' + error);
                alert('Network error: ' + error);
            }
            
            postBtn.disabled = false;
            postBtn.textContent = '🚀 Post Tweet';
        });
        
        function clearTweet() {
            textarea.value = '';
            charCount.textContent = '0 / 280';
            charCount.classList.remove('error', 'warning');
            imageInput.value = '';
            selectedFiles.textContent = 'No images selected';
            selectedFiles.style.color = '#657786';
            log('🗑️ Cleared tweet');
        }
        
        async function getMyTweets() {
            log('📥 Fetching your tweets...');
            
            try {
                const response = await fetch('/get-tweets');
                const data = await response.json();
                
                if (data.success) {
                    log(`✅ Retrieved ${data.tweets.length} tweets`);
                    let msg = 'Your recent tweets:\\n\\n';
                    data.tweets.forEach((t, i) => {
                        msg += `${i+1}. ${t.text.substring(0, 50)}...\\n`;
                    });
                    alert(msg);
                } else {
                    log('❌ Error: ' + data.error);
                    alert('Error: ' + data.error);
                }
            } catch (error) {
                log('❌ Error: ' + error);
                alert('Error: ' + error);
            }
        }
        
        function showModal(message) {
            document.getElementById('modalMessage').innerHTML = message;
            document.getElementById('successModal').classList.add('show');
        }
        
        function closeModal() {
            document.getElementById('successModal').classList.remove('show');
        }
        
        // Initial log
        log('{% if authenticated %}✅ Bot authenticated successfully!{% else %}❌ Not authenticated{% endif %}');
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, authenticated=authenticated)

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
        response = bot.post_tweet(text)
        if response and response.data:
            tweet_id = response.data.get('id')
            return jsonify({'success': True, 'tweet_id': tweet_id})
        else:
            return jsonify({'success': False, 'error': 'No response from API'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/get-tweets')
def get_tweets():
    bot, auth = lazy_init_bot()
    if not auth or not bot:
        return jsonify({'success': False, 'error': 'Not authenticated'})
    
    try:
        tweets = bot.get_my_tweets(max_results=5)
        tweet_list = [{'text': t.text, 'id': t.id} for t in tweets] if tweets else []
        return jsonify({'success': True, 'tweets': tweet_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def open_browser():
    """Open browser after short delay"""
    import time
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n" + "="*60)
    print("🐦 X Bot Web Interface Starting...")
    print("="*60)
    print("\n✨ Opening in your browser at: http://127.0.0.1:5000")
    print("\n💡 Press Ctrl+C to stop the server\n")
    
    # Run Flask app
    app.run(debug=False, port=5000)

