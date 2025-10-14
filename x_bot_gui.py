#!/usr/bin/env python3
"""
X Bot GUI - Graphical Interface for Posting Tweets
A user-friendly GUI to compose and post tweets without using the terminal
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from x_bot import XBot
from datetime import datetime


class XBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X Bot - Tweet Composer 🐦")
        self.root.geometry("700x650")
        self.root.resizable(True, True)
        
        # Initialize bot
        self.bot = None
        self.authenticated = False
        self.selected_images = []
        
        # Try to authenticate
        self.authenticate_bot()
        
        # Create GUI
        self.create_widgets()
        
    def authenticate_bot(self):
        """Try to authenticate with X API"""
        try:
            self.bot = XBot()
            if self.bot.client:
                self.authenticated = True
        except Exception as e:
            self.authenticated = False
            
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Set background color for root
        self.root.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(self.root, bg="#1DA1F2", height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🐦 X Bot - Tweet Composer",
            font=("Arial", 18, "bold"),
            bg="#1DA1F2",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main content frame
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status indicator
        status_frame = tk.Frame(main_frame, bg='white')
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        status_label = tk.Label(
            status_frame,
            text="Status:",
            font=("Arial", 10, "bold"),
            bg='white'
        )
        status_label.pack(side=tk.LEFT)
        
        if self.authenticated:
            status_text = "✅ Connected"
            status_color = "green"
        else:
            status_text = "❌ Not Connected (Check credentials)"
            status_color = "red"
            
        self.status_indicator = tk.Label(
            status_frame,
            text=status_text,
            font=("Arial", 10),
            fg=status_color,
            bg='white'
        )
        self.status_indicator.pack(side=tk.LEFT, padx=5)
        
        # Tweet composition area
        tweet_label = tk.Label(
            main_frame,
            text="Compose Your Tweet:",
            font=("Arial", 12, "bold"),
            bg='white'
        )
        tweet_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Text area with scrollbar
        self.tweet_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=8,
            font=("Arial", 12),
            relief=tk.SOLID,
            borderwidth=1,
            bg='white',
            fg='black'
        )
        self.tweet_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.tweet_text.bind('<KeyRelease>', self.update_character_count)
        
        # Character counter
        counter_frame = tk.Frame(main_frame, bg='white')
        counter_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.char_count_label = tk.Label(
            counter_frame,
            text="0 / 280 characters",
            font=("Arial", 10),
            fg="gray",
            bg='white'
        )
        self.char_count_label.pack(side=tk.RIGHT)
        
        # Media section
        media_frame = tk.LabelFrame(
            main_frame,
            text="Attach Images (Optional)",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10,
            bg='white'
        )
        media_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_add_image = tk.Button(
            media_frame,
            text="📎 Add Images (up to 4)",
            command=self.add_images,
            bg="#1DA1F2",
            fg="white",
            font=("Arial", 11),
            cursor="hand2",
            padx=10,
            pady=5,
            highlightthickness=0
        )
        btn_add_image.pack(side=tk.LEFT, padx=5)
        
        btn_clear_images = tk.Button(
            media_frame,
            text="🗑️ Clear Images",
            command=self.clear_images,
            bg="#E1E8ED",
            font=("Arial", 11),
            cursor="hand2",
            padx=10,
            pady=5,
            highlightthickness=0
        )
        btn_clear_images.pack(side=tk.LEFT, padx=5)
        
        self.images_label = tk.Label(
            media_frame,
            text="No images selected",
            font=("Arial", 10),
            fg="gray",
            bg='white'
        )
        self.images_label.pack(side=tk.LEFT, padx=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Post button
        self.post_button = tk.Button(
            buttons_frame,
            text="🚀 Post Tweet",
            command=self.post_tweet,
            bg="#1DA1F2",
            fg="white",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            padx=20,
            pady=10,
            highlightthickness=0
        )
        self.post_button.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        btn_clear = tk.Button(
            buttons_frame,
            text="🗑️ Clear",
            command=self.clear_text,
            bg="#E1E8ED",
            font=("Arial", 12),
            cursor="hand2",
            padx=15,
            pady=10,
            highlightthickness=0
        )
        btn_clear.pack(side=tk.LEFT, padx=5)
        
        # Get tweets button
        btn_get_tweets = tk.Button(
            buttons_frame,
            text="📥 My Recent Tweets",
            command=self.get_tweets,
            bg="#17BF63",
            fg="white",
            font=("Arial", 12),
            cursor="hand2",
            padx=15,
            pady=10,
            highlightthickness=0
        )
        btn_get_tweets.pack(side=tk.LEFT, padx=5)
        
        # Activity log
        log_label = tk.Label(
            main_frame,
            text="Activity Log:",
            font=("Arial", 11, "bold"),
            bg='white'
        )
        log_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            width=60,
            height=6,
            font=("Monaco", 10),
            bg="#F7F9FA",
            fg='black',
            relief=tk.SOLID,
            borderwidth=1,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, pady=(0, 10))
        
        # Add initial log entry
        if self.authenticated:
            self.log("✅ Bot authenticated successfully!")
        else:
            self.log("❌ Authentication failed. Check x_credentials.json")
            
    def update_character_count(self, event=None):
        """Update character count as user types"""
        text = self.tweet_text.get("1.0", tk.END).strip()
        char_count = len(text)
        
        self.char_count_label.config(text=f"{char_count} / 280 characters")
        
        if char_count > 280:
            self.char_count_label.config(fg="red")
        elif char_count > 260:
            self.char_count_label.config(fg="orange")
        else:
            self.char_count_label.config(fg="gray")
            
    def add_images(self):
        """Open file dialog to select images"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if files:
            # Limit to 4 images
            self.selected_images = list(files)[:4]
            count = len(self.selected_images)
            
            if count == 1:
                self.images_label.config(text=f"1 image selected", fg="green")
            else:
                self.images_label.config(text=f"{count} images selected", fg="green")
            
            # Log the files
            for img in self.selected_images:
                self.log(f"📎 Added image: {img.split('/')[-1]}")
                
    def clear_images(self):
        """Clear selected images"""
        self.selected_images = []
        self.images_label.config(text="No images selected", fg="gray")
        self.log("🗑️ Cleared all images")
        
    def log(self, message):
        """Add message to activity log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def clear_text(self):
        """Clear the tweet text area"""
        self.tweet_text.delete("1.0", tk.END)
        self.update_character_count()
        self.log("🗑️ Cleared tweet text")
        
    def post_tweet(self):
        """Post the tweet"""
        if not self.authenticated:
            messagebox.showerror(
                "Not Authenticated",
                "Bot is not authenticated. Please check your x_credentials.json file."
            )
            return
        
        tweet_text = self.tweet_text.get("1.0", tk.END).strip()
        
        if not tweet_text:
            messagebox.showwarning("Empty Tweet", "Please write something to tweet!")
            return
        
        # Disable button while posting
        self.post_button.config(state=tk.DISABLED, text="Posting...")
        self.root.update()
        
        # Post in background thread
        thread = threading.Thread(target=self._post_tweet_thread, args=(tweet_text,))
        thread.daemon = True
        thread.start()
        
    def _post_tweet_thread(self, tweet_text):
        """Post tweet in background thread"""
        try:
            if self.selected_images:
                # Post with media
                response = self.bot.post_tweet_with_media(tweet_text, self.selected_images)
            else:
                # Post text only
                response = self.bot.post_tweet(tweet_text)
            
            # Update UI in main thread
            self.root.after(0, self._post_success, response, tweet_text)
            
        except Exception as e:
            self.root.after(0, self._post_error, str(e))
            
    def _post_success(self, response, tweet_text):
        """Handle successful post"""
        self.post_button.config(state=tk.NORMAL, text="🚀 Post Tweet")
        
        if response and response.data:
            tweet_id = response.data.get('id', 'unknown')
            url = f"https://twitter.com/i/web/status/{tweet_id}"
            
            self.log(f"✅ Tweet posted successfully!")
            self.log(f"🔗 URL: {url}")
            
            messagebox.showinfo(
                "Success! 🎉",
                f"Tweet posted successfully!\n\nTweet ID: {tweet_id}\n\nClick OK to view on X.",
            )
            
            # Clear after successful post
            self.clear_text()
            self.clear_images()
        else:
            self.log("⚠️ Tweet may have been posted but no confirmation received")
            
    def _post_error(self, error_msg):
        """Handle post error"""
        self.post_button.config(state=tk.NORMAL, text="🚀 Post Tweet")
        self.log(f"❌ Error: {error_msg}")
        messagebox.showerror("Error Posting Tweet", f"Failed to post tweet:\n\n{error_msg}")
        
    def get_tweets(self):
        """Get recent tweets"""
        if not self.authenticated:
            messagebox.showerror(
                "Not Authenticated",
                "Bot is not authenticated. Please check your x_credentials.json file."
            )
            return
        
        self.log("📥 Fetching recent tweets...")
        
        # Run in background thread
        thread = threading.Thread(target=self._get_tweets_thread)
        thread.daemon = True
        thread.start()
        
    def _get_tweets_thread(self):
        """Get tweets in background thread"""
        try:
            tweets = self.bot.get_my_tweets(max_results=5)
            self.root.after(0, self._show_tweets, tweets)
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ Error fetching tweets: {e}"))
            
    def _show_tweets(self, tweets):
        """Display retrieved tweets"""
        if tweets:
            self.log(f"✅ Retrieved {len(tweets)} tweets")
            
            # Create popup window
            popup = tk.Toplevel(self.root)
            popup.title("Recent Tweets")
            popup.geometry("600x400")
            
            text_widget = scrolledtext.ScrolledText(
                popup,
                wrap=tk.WORD,
                font=("Helvetica", 10),
                padx=10,
                pady=10
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            for i, tweet in enumerate(tweets, 1):
                text_widget.insert(tk.END, f"Tweet #{i}\n", "bold")
                text_widget.insert(tk.END, f"{tweet.text}\n\n")
                
                if hasattr(tweet, 'created_at'):
                    text_widget.insert(tk.END, f"Posted: {tweet.created_at}\n")
                
                if hasattr(tweet, 'public_metrics'):
                    metrics = tweet.public_metrics
                    text_widget.insert(
                        tk.END,
                        f"❤️ {metrics['like_count']} | "
                        f"🔄 {metrics['retweet_count']} | "
                        f"💬 {metrics['reply_count']}\n"
                    )
                
                text_widget.insert(tk.END, "\n" + "="*60 + "\n\n")
            
            text_widget.config(state=tk.DISABLED)
        else:
            self.log("⚠️ No tweets found")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = XBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

