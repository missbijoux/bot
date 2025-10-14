#!/usr/bin/env python3
"""
X Bot Instant App - Opens immediately, no rate limit waiting!
Beautiful dark glass GUI that works even during rate limits
"""

import webview
import threading
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# We'll initialize the bot ONLY when posting, not at startup
bot = None
authenticated = False

def lazy_init_bot():
    """Initialize bot only when needed"""
    global bot, authenticated
    if bot is None:
        try:
            from x_bot import XBot
            bot = XBot()
            if bot.client:
                authenticated = True
        except:
            authenticated = False
    return bot, authenticated

# Beautiful dark glass HTML
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>X Bot</title>
    <meta charset="utf-8">
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
            background: rgba(20, 20, 35, 0.75);
            backdrop-filter: blur(40px) saturate(150%);
            -webkit-backdrop-filter: blur(40px) saturate(150%);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6), 
                        0 0 100px rgba(29, 161, 242, 0.15),
                        inset 0 0 80px rgba(29, 161, 242, 0.05);
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
            box-shadow: 0 0 20px rgba(29, 161, 242, 0.2);
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
            border-top: 2px solid rgba(255, 255, 255, 0.1);
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
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐦 X Bot</h1>
            <p class="subtitle">Tweet Composer</p>
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
            
            <label style="margin-top: 15px;">Attach Images (up to 4)</label>
            <input type="file" id="imageInput" accept="image/*" multiple style="width: 100%; padding: 10px; background: rgba(45, 51, 89, 0.5); border: 2px solid rgba(255, 255, 255, 0.1); border-radius: 8px; color: white; cursor: pointer; margin-bottom: 5px;">
            <div id="imagePreview" style="margin-bottom: 15px; color: #8899A6; font-size: 12px;"></div>
            
            <button type="submit" class="btn-primary" id="postBtn">
                🚀 Post Tweet
            </button>
        </form>
        
        <div class="btn-group">
            <button class="btn-secondary" onclick="clearTweet()">🗑️ Clear</button>
            <button class="btn-secondary" onclick="clearImages()">🖼️ Clear Images</button>
        </div>
        
        <div class="activity">
            <h3>Activity Log</h3>
            <div class="log" id="activityLog"></div>
        </div>
    </div>
    
    <script>
        const textarea = document.getElementById('tweetText');
        const charCount = document.getElementById('charCount');
        const activityLog = document.getElementById('activityLog');
        const imageInput = document.getElementById('imageInput');
        const imagePreview = document.getElementById('imagePreview');
        
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
        
        imageInput.addEventListener('change', function() {
            const count = this.files.length;
            if (count > 0) {
                const fileNames = Array.from(this.files).slice(0, 4).map(f => f.name).join(', ');
                imagePreview.innerHTML = `<span style="color: #17BF63;">✅ ${count} image${count > 1 ? 's' : ''} selected:</span> ${fileNames}`;
                log(`📎 Attached ${count} image${count > 1 ? 's' : ''}`);
            } else {
                imagePreview.innerHTML = '';
            }
        });
        
        function log(message) {
            const time = new Date().toLocaleTimeString();
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span class="time">[${time}]</span> ${message}`;
            activityLog.insertBefore(entry, activityLog.firstChild);
        }
        
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
            
            log('📤 Attempting to post tweet...');
            
            try {
                const formData = new FormData();
                formData.append('text', text);
                
                // Add images if selected
                const files = imageInput.files;
                for (let i = 0; i < Math.min(files.length, 4); i++) {
                    formData.append('images', files[i]);
                }
                
                const response = await fetch('/post', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    log('✅ Tweet posted successfully!');
                    log(`🔗 Tweet ID: ${data.tweet_id}`);
                    alert('Success! Your tweet was posted!\\nTweet ID: ' + data.tweet_id);
                    clearTweet();
                    clearImages();
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
            log('🗑️ Cleared tweet');
        }
        
        function clearImages() {
            imageInput.value = '';
            imagePreview.innerHTML = '';
            log('🖼️ Cleared images');
        }
        
        log('✨ GUI ready! Compose your tweet above.');
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
        return jsonify({'success': False, 'error': 'Not authenticated. Check credentials.'})
    
    text = request.form.get('text', '').strip()
    
    if not text:
        return jsonify({'success': False, 'error': 'Empty tweet'})
    
    try:
        # Check if images were uploaded
        images = request.files.getlist('images')
        
        if images and len(images) > 0:
            # Save images temporarily
            import tempfile
            image_paths = []
            for img in images[:4]:  # Max 4 images
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(img.filename)[1])
                img.save(temp_file.name)
                image_paths.append(temp_file.name)
            
            # Post with media
            response = bot.post_tweet_with_media(text, image_paths)
            
            # Clean up temp files
            for path in image_paths:
                try:
                    os.remove(path)
                except:
                    pass
        else:
            # Post text only
            response = bot.post_tweet(text)
        
        if response and response.data:
            tweet_id = response.data.get('id')
            return jsonify({'success': True, 'tweet_id': tweet_id})
        else:
            return jsonify({'success': False, 'error': 'No response from API'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def start_flask():
    """Start Flask in background thread"""
    app.run(port=5002, debug=False, use_reloader=False)

if __name__ == '__main__':
    print("\n🚀 X Bot Instant - Opening now!\n")
    
    # Start Flask server in background thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Give Flask time to start
    import time
    time.sleep(1)
    
    # Create native window - Opens INSTANTLY!
    window = webview.create_window(
        'X Bot - Tweet Composer',
        'http://127.0.0.1:5002',
        width=700,
        height=800,
        resizable=True,
        min_size=(600, 700)
    )
    
    # Start the application
    webview.start()

