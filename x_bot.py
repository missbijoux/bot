#!/usr/bin/env python3
"""
X (Twitter) Bot
A simple bot to post tweets to X/Twitter using the API
"""

import tweepy
import os
import sys
from datetime import datetime
import argparse
import json
from pathlib import Path


class XBot:
    """X/Twitter Bot for posting tweets"""
    
    def __init__(self, credentials_file=None):
        """
        Initialize the X Bot with credentials
        
        Args:
            credentials_file: Path to JSON file with credentials (optional)
        """
        self.client = None
        self.api = None
        self.credentials_file = credentials_file or "x_credentials.json"
        self._load_credentials()
    
    def _load_credentials(self):
        """Load credentials from file or environment variables"""
        credentials = {}
        
        # Try loading from file first
        if os.path.exists(self.credentials_file):
            try:
                with open(self.credentials_file, 'r') as f:
                    credentials = json.load(f)
                print(f"✓ Loaded credentials from {self.credentials_file}")
            except Exception as e:
                print(f"⚠ Warning: Could not load {self.credentials_file}: {e}")
        
        # Get credentials from file or environment variables
        self.api_key = credentials.get('api_key') or os.getenv('X_API_KEY')
        self.api_secret = credentials.get('api_secret') or os.getenv('X_API_SECRET')
        self.access_token = credentials.get('access_token') or os.getenv('X_ACCESS_TOKEN')
        self.access_token_secret = credentials.get('access_token_secret') or os.getenv('X_ACCESS_TOKEN_SECRET')
        self.bearer_token = credentials.get('bearer_token') or os.getenv('X_BEARER_TOKEN')
        
        # Check if we have minimum required credentials
        if not self.api_key or not self.api_secret:
            print("\n⚠ WARNING: API credentials not found!")
            print("Please set up your credentials. See X_BOT_SETUP.md for instructions.\n")
            return
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with X/Twitter API"""
        try:
            # Create Client for API v2 (recommended)
            if self.bearer_token or (self.access_token and self.access_token_secret):
                self.client = tweepy.Client(
                    bearer_token=self.bearer_token,
                    consumer_key=self.api_key,
                    consumer_secret=self.api_secret,
                    access_token=self.access_token,
                    access_token_secret=self.access_token_secret,
                    wait_on_rate_limit=True
                )
                
                # Test authentication
                if self.access_token and self.access_token_secret:
                    try:
                        me = self.client.get_me()
                        if me.data:
                            print(f"✓ Authenticated as: @{me.data.username}")
                    except Exception as e:
                        print(f"⚠ Authentication test failed: {e}")
                else:
                    print("✓ Client authenticated (read-only mode)")
            
            # Create API for API v1.1 (for media upload if needed)
            if self.access_token and self.access_token_secret:
                auth = tweepy.OAuth1UserHandler(
                    self.api_key, 
                    self.api_secret,
                    self.access_token,
                    self.access_token_secret
                )
                self.api = tweepy.API(auth)
                
        except Exception as e:
            print(f"✗ Authentication failed: {e}")
            sys.exit(1)
    
    def post_tweet(self, text, reply_to=None):
        """
        Post a tweet to X/Twitter
        
        Args:
            text: The text content of the tweet (max 280 characters)
            reply_to: Tweet ID to reply to (optional)
        
        Returns:
            Response object from the API
        """
        if not self.client:
            print("✗ Error: Client not authenticated. Cannot post tweets.")
            return None
        
        if not text:
            print("✗ Error: Tweet text cannot be empty.")
            return None
        
        if len(text) > 280:
            print(f"⚠ Warning: Tweet is {len(text)} characters (max 280). Truncating...")
            text = text[:277] + "..."
        
        try:
            response = self.client.create_tweet(
                text=text,
                in_reply_to_tweet_id=reply_to
            )
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✓ Tweet posted successfully!")
                print(f"  Tweet ID: {tweet_id}")
                print(f"  Content: {text}")
                print(f"  URL: https://twitter.com/i/web/status/{tweet_id}")
                return response
            else:
                print("✗ Failed to post tweet")
                return None
                
        except Exception as e:
            print(f"✗ Error posting tweet: {e}")
            return None
    
    def post_tweet_with_media(self, text, media_paths, reply_to=None):
        """
        Post a tweet with media (images)
        
        Args:
            text: The text content of the tweet
            media_paths: List of paths to media files (up to 4 images)
            reply_to: Tweet ID to reply to (optional)
        
        Returns:
            Response object from the API
        """
        if not self.client or not self.api:
            print("✗ Error: Not authenticated for media upload.")
            return None
        
        if not media_paths:
            return self.post_tweet(text, reply_to)
        
        try:
            # Upload media using v1.1 API
            media_ids = []
            for media_path in media_paths[:4]:  # Max 4 images
                if not os.path.exists(media_path):
                    print(f"⚠ Warning: Media file not found: {media_path}")
                    continue
                
                media = self.api.media_upload(media_path)
                media_ids.append(media.media_id)
                print(f"✓ Uploaded media: {media_path}")
            
            if not media_ids:
                print("✗ No media was uploaded successfully")
                return None
            
            # Post tweet with media using v2 API
            response = self.client.create_tweet(
                text=text,
                media_ids=media_ids,
                in_reply_to_tweet_id=reply_to
            )
            
            if response.data:
                tweet_id = response.data['id']
                print(f"✓ Tweet with media posted successfully!")
                print(f"  Tweet ID: {tweet_id}")
                print(f"  Media count: {len(media_ids)}")
                print(f"  URL: https://twitter.com/i/web/status/{tweet_id}")
                return response
            
        except Exception as e:
            print(f"✗ Error posting tweet with media: {e}")
            return None
    
    def delete_tweet(self, tweet_id):
        """
        Delete a tweet
        
        Args:
            tweet_id: The ID of the tweet to delete
        
        Returns:
            Boolean indicating success
        """
        if not self.client:
            print("✗ Error: Client not authenticated.")
            return False
        
        try:
            response = self.client.delete_tweet(tweet_id)
            if response.data and response.data.get('deleted'):
                print(f"✓ Tweet {tweet_id} deleted successfully")
                return True
            else:
                print(f"✗ Failed to delete tweet {tweet_id}")
                return False
        except Exception as e:
            print(f"✗ Error deleting tweet: {e}")
            return False
    
    def get_my_tweets(self, max_results=10):
        """
        Get recent tweets from authenticated user
        
        Args:
            max_results: Maximum number of tweets to retrieve (default: 10)
        
        Returns:
            List of tweets
        """
        if not self.client:
            print("✗ Error: Client not authenticated.")
            return []
        
        try:
            me = self.client.get_me()
            if not me.data:
                print("✗ Could not get user info")
                return []
            
            user_id = me.data.id
            tweets = self.client.get_users_tweets(
                user_id,
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics']
            )
            
            if tweets.data:
                print(f"\n✓ Retrieved {len(tweets.data)} tweets:")
                for tweet in tweets.data:
                    print(f"\n  [{tweet.created_at}]")
                    print(f"  {tweet.text}")
                    if hasattr(tweet, 'public_metrics'):
                        metrics = tweet.public_metrics
                        print(f"  ❤️  {metrics['like_count']} | 🔄 {metrics['retweet_count']} | 💬 {metrics['reply_count']}")
                
                return tweets.data
            else:
                print("No tweets found")
                return []
                
        except Exception as e:
            print(f"✗ Error retrieving tweets: {e}")
            return []


def create_credentials_template():
    """Create a template credentials file"""
    template = {
        "api_key": "YOUR_API_KEY_HERE",
        "api_secret": "YOUR_API_SECRET_HERE",
        "access_token": "YOUR_ACCESS_TOKEN_HERE",
        "access_token_secret": "YOUR_ACCESS_TOKEN_SECRET_HERE",
        "bearer_token": "YOUR_BEARER_TOKEN_HERE (optional)"
    }
    
    filename = "x_credentials.json"
    if os.path.exists(filename):
        print(f"⚠ {filename} already exists. Not overwriting.")
        return
    
    with open(filename, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"✓ Created {filename}")
    print("  Please edit this file and add your X API credentials.")
    print("  See X_BOT_SETUP.md for instructions on getting credentials.")


def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(
        description='X (Twitter) Bot - Post tweets from the command line',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post a simple tweet
  python3 x_bot.py --post "Hello from my X bot!"
  
  # Post a tweet with media
  python3 x_bot.py --post "Check out this image!" --media image.jpg
  
  # Get your recent tweets
  python3 x_bot.py --get-tweets
  
  # Create credentials template
  python3 x_bot.py --setup
  
  # Delete a tweet
  python3 x_bot.py --delete 1234567890
        """
    )
    
    parser.add_argument('--post', type=str, help='Post a tweet with the given text')
    parser.add_argument('--media', nargs='+', help='Media files to attach to the tweet')
    parser.add_argument('--reply-to', type=str, help='Tweet ID to reply to')
    parser.add_argument('--delete', type=str, help='Delete a tweet by ID')
    parser.add_argument('--get-tweets', action='store_true', help='Get your recent tweets')
    parser.add_argument('--max-results', type=int, default=10, help='Max tweets to retrieve (default: 10)')
    parser.add_argument('--setup', action='store_true', help='Create credentials template file')
    parser.add_argument('--credentials', type=str, help='Path to credentials JSON file (default: x_credentials.json)')
    
    args = parser.parse_args()
    
    # Handle setup command
    if args.setup:
        create_credentials_template()
        return
    
    # Initialize bot
    bot = XBot(credentials_file=args.credentials)
    
    # Handle different commands
    if args.post:
        if args.media:
            bot.post_tweet_with_media(args.post, args.media, args.reply_to)
        else:
            bot.post_tweet(args.post, args.reply_to)
    
    elif args.delete:
        bot.delete_tweet(args.delete)
    
    elif args.get_tweets:
        bot.get_my_tweets(args.max_results)
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

