#!/usr/bin/env python3
"""
X Bot Enhanced - Advanced Twitter Bot with Scheduling and Auto-Reply
Features: Tweet scheduling, automated replies, keyword monitoring
"""

import tweepy
import os
import sys
import json
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
import argparse
import schedule
from typing import List, Dict, Optional
import re


class XBotEnhanced:
    """Enhanced X/Twitter Bot with scheduling and auto-reply capabilities"""
    
    def __init__(self, credentials_file=None, db_file="x_bot.db"):
        """
        Initialize the Enhanced X Bot
        
        Args:
            credentials_file: Path to JSON file with credentials
            db_file: Path to SQLite database for storing scheduled tweets
        """
        self.client = None
        self.api = None
        self.credentials_file = credentials_file or "x_credentials.json"
        self.db_file = db_file
        self.scheduler_running = False
        self.auto_reply_running = False
        
        # Load credentials and initialize database
        self._load_credentials()
        self._init_database()
        
        # Auto-reply configuration
        self.auto_reply_config = {
            'enabled': False,
            'keywords': {},
            'cooldown_minutes': 30,
            'max_replies_per_hour': 10
        }
        
        # Rate limiting tracking
        self.reply_count = 0
        self.last_reply_reset = datetime.now()
    
    def _load_credentials(self):
        """Load credentials from file"""
        credentials = {}
        
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r') as f:
                    credentials = json.load(f)
                print(f"✓ Loaded credentials from {self.credentials_file}")
            except Exception as e:
                print(f"⚠ Warning: Could not load {self.credentials_file}: {e}")
        
        # Get credentials
        self.api_key = credentials.get('api_key')
        self.api_secret = credentials.get('api_secret')
        self.access_token = credentials.get('access_token')
        self.access_token_secret = credentials.get('access_token_secret')
        self.bearer_token = credentials.get('bearer_token')
        
        # Authenticate with Twitter API
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Twitter API"""
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            print("❌ Missing credentials. Run with --setup to create credentials file.")
            return False
        
        try:
            # OAuth 1.0a User Context (for posting)
            auth = tweepy.OAuth1UserHandler(
                self.api_key, self.api_secret,
                self.access_token, self.access_token_secret
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)
            
            # OAuth 2.0 Bearer Token (for reading)
            if self.bearer_token:
                self.client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                    wait_on_rate_limit=True
                )
            
            # Verify credentials
            user = self.api.verify_credentials()
            print(f"✓ Authenticated as @{user.screen_name}")
            return True
            
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def _init_database(self):
        """Initialize SQLite database for scheduled tweets"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create scheduled tweets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                media_files TEXT,
                reply_to_tweet_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                posted_at DATETIME
            )
        ''')
        
        # Create auto-reply rules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auto_reply_rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL,
                response TEXT NOT NULL,
                enabled BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create reply history table (for rate limiting)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reply_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_tweet_id TEXT NOT NULL,
                reply_tweet_id TEXT NOT NULL,
                replied_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ Database initialized: {self.db_file}")
    
    # ===== SCHEDULING METHODS =====
    
    def schedule_tweet(self, content: str, scheduled_time: datetime, 
                      media_files: List[str] = None, reply_to_tweet_id: str = None):
        """
        Schedule a tweet for later posting
        
        Args:
            content: Tweet content
            scheduled_time: When to post the tweet
            media_files: List of image file paths
            reply_to_tweet_id: ID of tweet to reply to
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        media_json = json.dumps(media_files) if media_files else None
        
        cursor.execute('''
            INSERT INTO scheduled_tweets 
            (content, scheduled_time, media_files, reply_to_tweet_id)
            VALUES (?, ?, ?, ?)
        ''', (content, scheduled_time, media_json, reply_to_tweet_id))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Tweet scheduled for {scheduled_time}")
        return cursor.lastrowid
    
    def get_scheduled_tweets(self, status='pending'):
        """Get scheduled tweets from database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, content, scheduled_time, media_files, reply_to_tweet_id
            FROM scheduled_tweets 
            WHERE status = ? 
            ORDER BY scheduled_time ASC
        ''', (status,))
        
        tweets = cursor.fetchall()
        conn.close()
        return tweets
    
    def post_scheduled_tweet(self, tweet_id: int):
        """Post a scheduled tweet and update its status"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get tweet details
        cursor.execute('''
            SELECT content, media_files, reply_to_tweet_id
            FROM scheduled_tweets WHERE id = ?
        ''', (tweet_id,))
        
        result = cursor.fetchone()
        if not result:
            conn.close()
            return False
        
        content, media_files_json, reply_to_tweet_id = result
        
        try:
            media_files = json.loads(media_files_json) if media_files_json else None
            
            # Post the tweet
            tweet_result = None
            if media_files:
                tweet_result = self.post_tweet_with_media(content, media_files, reply_to_tweet_id)
            else:
                tweet_result = self.post_tweet(content, reply_to_tweet_id)
            
            # Check if post was successful
            if tweet_result:
                # Update status to posted
                cursor.execute('''
                    UPDATE scheduled_tweets 
                    SET status = 'posted', posted_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (tweet_id,))
                
                conn.commit()
                print(f"✓ Posted scheduled tweet #{tweet_id}")
                return True
            else:
                # Post failed (returned None)
                print(f"❌ Failed to post scheduled tweet #{tweet_id}: Post method returned None")
                cursor.execute('''
                    UPDATE scheduled_tweets SET status = 'failed'
                    WHERE id = ?
                ''', (tweet_id,))
                conn.commit()
                return False
            
        except Exception as e:
            print(f"❌ Failed to post scheduled tweet #{tweet_id}: {e}")
            cursor.execute('''
                UPDATE scheduled_tweets SET status = 'failed'
                WHERE id = ?
            ''', (tweet_id,))
            conn.commit()
            return False
        finally:
            conn.close()
    
    def start_scheduler(self):
        """Start the background scheduler"""
        if self.scheduler_running:
            print("⚠ Scheduler is already running")
            return
        
        self.scheduler_running = True
        scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        scheduler_thread.start()
        print("✓ Tweet scheduler started")
    
    def stop_scheduler(self):
        """Stop the background scheduler"""
        self.scheduler_running = False
        print("✓ Tweet scheduler stopped")
    
    def _scheduler_loop(self):
        """Main scheduler loop - runs in background thread"""
        while self.scheduler_running:
            try:
                # Get pending tweets that are due
                now = datetime.now()
                tweets = self.get_scheduled_tweets('pending')
                
                for tweet in tweets:
                    tweet_id, content, scheduled_time, media_files, reply_to_tweet_id = tweet
                    scheduled_dt = datetime.fromisoformat(scheduled_time)
                    
                    if scheduled_dt <= now:
                        self.post_scheduled_tweet(tweet_id)
                
                # Sleep for 1 minute before checking again
                time.sleep(60)
                
            except Exception as e:
                print(f"❌ Scheduler error: {e}")
                time.sleep(60)
    
    # ===== AUTO-REPLY METHODS =====
    
    def add_auto_reply_rule(self, keyword: str, response: str):
        """Add a new auto-reply rule"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO auto_reply_rules (keyword, response)
            VALUES (?, ?)
        ''', (keyword, response))
        
        conn.commit()
        conn.close()
        print(f"✓ Added auto-reply rule for keyword: '{keyword}'")
    
    def get_auto_reply_rules(self):
        """Get all auto-reply rules"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT keyword, response FROM auto_reply_rules WHERE enabled = 1
        ''')
        
        rules = cursor.fetchall()
        conn.close()
        return dict(rules)
    
    def start_auto_reply(self):
        """Start monitoring for mentions and auto-replying"""
        if self.auto_reply_running:
            print("⚠ Auto-reply is already running")
            return
        
        if not self.client:
            print("❌ Bearer token required for auto-reply functionality")
            return
        
        self.auto_reply_running = True
        reply_thread = threading.Thread(target=self._auto_reply_loop, daemon=True)
        reply_thread.start()
        print("✓ Auto-reply monitor started")
    
    def stop_auto_reply(self):
        """Stop the auto-reply monitor"""
        self.auto_reply_running = False
        print("✓ Auto-reply monitor stopped")
    
    def _auto_reply_loop(self):
        """Main auto-reply loop - monitors mentions"""
        last_mention_id = None
        
        while self.auto_reply_running:
            try:
                # Check rate limiting
                self._check_rate_limits()
                
                # Get recent mentions
                mentions = self.client.get_mentions(
                    max_results=10,
                    since_id=last_mention_id
                )
                
                if mentions.data:
                    last_mention_id = mentions.data[0].id
                    self._process_mentions(mentions.data)
                
                # Sleep for 2 minutes before checking again
                time.sleep(120)
                
            except Exception as e:
                print(f"❌ Auto-reply error: {e}")
                time.sleep(120)
    
    def _process_mentions(self, mentions):
        """Process mentions and send auto-replies"""
        rules = self.get_auto_reply_rules()
        
        for mention in mentions:
            # Check if we already replied to this tweet
            if self._already_replied(mention.id):
                continue
            
            # Check for keywords in the mention text
            mention_text = mention.text.lower()
            
            for keyword, response in rules.items():
                if keyword.lower() in mention_text:
                    self._send_auto_reply(mention.id, response, mention.author_id)
                    break
    
    def _send_auto_reply(self, original_tweet_id: str, response: str, author_id: str):
        """Send an auto-reply"""
        try:
            # Post reply
            reply_tweet = self.api.update_status(
                status=response,
                in_reply_to_status_id=original_tweet_id
            )
            
            # Record the reply
            self._record_reply(original_tweet_id, reply_tweet.id_str)
            
            print(f"✓ Auto-reply sent to tweet {original_tweet_id}")
            self.reply_count += 1
            
        except Exception as e:
            print(f"❌ Failed to send auto-reply: {e}")
    
    def _already_replied(self, tweet_id: str) -> bool:
        """Check if we already replied to this tweet"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM reply_history 
            WHERE original_tweet_id = ?
        ''', (tweet_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    
    def _record_reply(self, original_tweet_id: str, reply_tweet_id: str):
        """Record a reply in the database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reply_history (original_tweet_id, reply_tweet_id)
            VALUES (?, ?)
        ''', (original_tweet_id, reply_tweet_id))
        
        conn.commit()
        conn.close()
    
    def _check_rate_limits(self):
        """Check and reset rate limiting counters"""
        now = datetime.now()
        if now - self.last_reply_reset >= timedelta(hours=1):
            self.reply_count = 0
            self.last_reply_reset = now
    
    def cancel_scheduled_tweet(self, tweet_id: int):
        """Cancel a scheduled tweet"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE scheduled_tweets 
                SET status = 'cancelled'
                WHERE id = ?
            ''', (tweet_id,))
            
            conn.commit()
            print(f"✓ Scheduled tweet #{tweet_id} cancelled")
            return True
        except Exception as e:
            print(f"❌ Failed to cancel tweet #{tweet_id}: {e}")
            return False
        finally:
            conn.close()
    
    # ===== BASIC TWEET METHODS (from original bot) =====
    
    def post_tweet(self, content: str, reply_to_tweet_id: str = None):
        """Post a simple text tweet"""
        if not self.client:
            print("❌ Not authenticated. Check your credentials.")
            return None
        
        try:
            # Use v2 API Client (works with Free tier)
            response = self.client.create_tweet(
                text=content,
                in_reply_to_tweet_id=reply_to_tweet_id
            )
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✓ Tweet posted: {tweet_id}")
                return str(tweet_id)
            else:
                print("❌ No response data from API")
                return None
            
        except tweepy.TooManyRequests:
            print("❌ Rate limit exceeded. Please wait before posting again.")
        except Exception as e:
            print(f"❌ Failed to post tweet: {e}")
        return None
    
    def post_tweet_with_media(self, content: str, media_files: List[str], 
                             reply_to_tweet_id: str = None):
        """Post a tweet with media"""
        if not self.client or not self.api:
            print("❌ Not authenticated. Check your credentials.")
            return None
        
        if not media_files:
            return self.post_tweet(content, reply_to_tweet_id)
        
        try:
            # Upload media files using v1.1 API (media upload still supported on Free tier)
            media_ids = []
            for media_file in media_files:
                if os.path.exists(media_file):
                    media = self.api.media_upload(media_file)
                    media_ids.append(media.media_id)
                    print(f"✓ Uploaded media: {media_file}")
                else:
                    print(f"⚠ Media file not found: {media_file}")
            
            if not media_ids:
                print("❌ No valid media files found")
                return None
            
            # Post tweet with media using v2 API Client (works with Free tier)
            response = self.client.create_tweet(
                text=content,
                media_ids=media_ids,
                in_reply_to_tweet_id=reply_to_tweet_id
            )
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✓ Tweet with media posted: {tweet_id}")
                return str(tweet_id)
            else:
                print("❌ No response data from API")
                return None
            
        except Exception as e:
            print(f"❌ Failed to post tweet with media: {e}")
        return None
    
    def delete_tweet(self, tweet_id: str):
        """Delete a tweet by ID"""
        if not self.api:
            print("❌ Not authenticated. Check your credentials.")
            return False
        
        try:
            self.api.destroy_status(tweet_id)
            print(f"✓ Tweet deleted: {tweet_id}")
            return True
        except Exception as e:
            print(f"❌ Failed to delete tweet: {e}")
            return False
    
    def get_my_tweets(self, max_results: int = 10):
        """Get your recent tweets"""
        if not self.api:
            print("❌ Not authenticated. Check your credentials.")
            return []
        
        try:
            tweets = self.api.user_timeline(count=max_results)
            return tweets
        except Exception as e:
            print(f"❌ Failed to get tweets: {e}")
            return []


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description="Enhanced X Bot with Scheduling and Auto-Reply")
    parser.add_argument('--setup', action='store_true', help='Create credentials template file')
    parser.add_argument('--post', type=str, help='Post a tweet')
    parser.add_argument('--schedule', type=str, help='Schedule a tweet (format: "content|YYYY-MM-DD HH:MM")')
    parser.add_argument('--add-reply-rule', nargs=2, metavar=('KEYWORD', 'RESPONSE'), 
                       help='Add auto-reply rule')
    parser.add_argument('--start-scheduler', action='store_true', help='Start tweet scheduler')
    parser.add_argument('--start-auto-reply', action='store_true', help='Start auto-reply monitor')
    parser.add_argument('--list-scheduled', action='store_true', help='List scheduled tweets')
    parser.add_argument('--list-rules', action='store_true', help='List auto-reply rules')
    
    args = parser.parse_args()
    
    if args.setup:
        # Create credentials template
        credentials = {
            "api_key": "YOUR_API_KEY_HERE",
            "api_secret": "YOUR_API_SECRET_HERE",
            "access_token": "YOUR_ACCESS_TOKEN_HERE",
            "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET_HERE",
            "bearer_token": "YOUR_BEARER_TOKEN_HERE (optional)"
        }
        
        with open("x_credentials.json", "w") as f:
            json.dump(credentials, f, indent=2)
        
        print("✓ Created x_credentials.json")
        print("Please edit this file and add your X API credentials.")
        return
    
    # Initialize bot
    bot = XBotEnhanced()
    
    if args.post:
        bot.post_tweet(args.post)
    
    elif args.schedule:
        try:
            content, scheduled_time = args.schedule.split('|', 1)
            scheduled_dt = datetime.fromisoformat(scheduled_time)
            bot.schedule_tweet(content.strip(), scheduled_dt)
        except ValueError:
            print("❌ Invalid schedule format. Use: 'content|YYYY-MM-DD HH:MM'")
    
    elif args.add_reply_rule:
        keyword, response = args.add_reply_rule
        bot.add_auto_reply_rule(keyword, response)
    
    elif args.start_scheduler:
        bot.start_scheduler()
        print("Scheduler running... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.stop_scheduler()
    
    elif args.start_auto_reply:
        bot.start_auto_reply()
        print("Auto-reply monitor running... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            bot.stop_auto_reply()
    
    elif args.list_scheduled:
        tweets = bot.get_scheduled_tweets()
        if tweets:
            print("\n📅 Scheduled Tweets:")
            for tweet in tweets:
                print(f"  ID: {tweet[0]} | {tweet[2]} | {tweet[1][:50]}...")
        else:
            print("No scheduled tweets found.")
    
    elif args.list_rules:
        rules = bot.get_auto_reply_rules()
        if rules:
            print("\n🤖 Auto-Reply Rules:")
            for keyword, response in rules.items():
                print(f"  '{keyword}' → '{response}'")
        else:
            print("No auto-reply rules found.")


if __name__ == "__main__":
    main()
