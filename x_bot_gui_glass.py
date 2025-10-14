#!/usr/bin/env python3
"""
X Bot Glass GUI - Modern Transparent Interface for macOS
A beautiful glass-style interface for posting tweets
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
from x_bot import XBot
from datetime import datetime


class ModernXBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X Bot")
        self.root.geometry("650x700")
        
        # Make window transparent/translucent (macOS specific)
        self.root.attributes('-alpha', 0.95)  # 95% opacity
        
        # Remove window decorations for modern look (optional)
        # self.root.overrideredirect(True)
        
        # Set background to dark for glass effect
        self.root.configure(bg='#1a1a1a')
        
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
        """Create all GUI widgets with glass styling"""
        
        # Main container with padding
        main_container = tk.Frame(self.root, bg='#1a1a1a', padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title section
        title_frame = tk.Frame(main_container, bg='#1a1a1a')
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = tk.Label(
            title_frame,
            text="X Bot",
            font=("Arial", 32, "bold"),
            fg='white',
            bg='#1a1a1a'
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Tweet Composer",
            font=("Arial", 14),
            fg='#8899A6',
            bg='#1a1a1a'
        )
        subtitle.pack()
        
        # Status indicator with glow effect
        status_frame = tk.Frame(main_container, bg='#1a1a1a')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        if self.authenticated:
            status_symbol = "●"
            status_text = "Connected"
            status_color = "#17BF63"
        else:
            status_symbol = "●"
            status_text = "Not Connected"
            status_color = "#E0245E"
        
        status_label = tk.Label(
            status_frame,
            text=f"{status_symbol} {status_text}",
            font=("Arial", 13, "bold"),
            fg=status_color,
            bg='#1a1a1a'
        )
        status_label.pack()
        
        # Tweet composition area
        compose_label = tk.Label(
            main_container,
            text="Compose Tweet",
            font=("Arial", 16, "bold"),
            fg='white',
            bg='#1a1a1a',
            anchor='w'
        )
        compose_label.pack(fill=tk.X, pady=(0, 10))
        
        # Custom styled text area frame with visible border
        text_frame = tk.Frame(
            main_container, 
            bg='#38444D',
            highlightbackground='#1DA1F2', 
            highlightthickness=2,
            relief=tk.SOLID,
            borderwidth=1
        )
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.tweet_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Arial", 15),
            bg='#253341',
            fg='white',
            insertbackground='#1DA1F2',
            relief=tk.FLAT,
            padx=15,
            pady=15,
            height=8,
            borderwidth=0
        )
        self.tweet_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.tweet_text.bind('<KeyRelease>', self.update_character_count)
        
        # Character counter
        counter_frame = tk.Frame(main_container, bg='#1a1a1a')
        counter_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.char_count_label = tk.Label(
            counter_frame,
            text="0 / 280",
            font=("Arial", 13),
            fg='#8899A6',
            bg='#1a1a1a'
        )
        self.char_count_label.pack(side=tk.RIGHT)
        
        # Media section
        media_frame = tk.Frame(main_container, bg='#1a1a1a')
        media_frame.pack(fill=tk.X, pady=(0, 20))
        
        media_label = tk.Label(
            media_frame,
            text="Media",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#1a1a1a'
        )
        media_label.pack(anchor='w', pady=(0, 8))
        
        media_buttons = tk.Frame(media_frame, bg='#1a1a1a')
        media_buttons.pack(fill=tk.X)
        
        self.add_image_btn = self.create_glass_button(
            media_buttons,
            "📎 Add Images",
            self.add_images,
            '#1DA1F2'
        )
        self.add_image_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_images_btn = self.create_glass_button(
            media_buttons,
            "✕ Clear",
            self.clear_images,
            '#657786'
        )
        self.clear_images_btn.pack(side=tk.LEFT)
        
        self.images_label = tk.Label(
            media_frame,
            text="No images selected",
            font=("Arial", 12),
            fg='#8899A6',
            bg='#1a1a1a'
        )
        self.images_label.pack(anchor='w', pady=(8, 0))
        
        # Action buttons
        buttons_frame = tk.Frame(main_container, bg='#1a1a1a')
        buttons_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.post_button = self.create_glass_button(
            buttons_frame,
            "🚀 Post Tweet",
            self.post_tweet,
            '#1DA1F2',
            large=True
        )
        self.post_button.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.clear_button = self.create_glass_button(
            buttons_frame,
            "Clear",
            self.clear_text,
            '#657786'
        )
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.tweets_button = self.create_glass_button(
            buttons_frame,
            "My Tweets",
            self.get_tweets,
            '#17BF63'
        )
        self.tweets_button.pack(side=tk.LEFT)
        
        # Activity log
        log_label = tk.Label(
            main_container,
            text="Activity",
            font=("Arial", 14, "bold"),
            fg='white',
            bg='#1a1a1a'
        )
        log_label.pack(anchor='w', pady=(10, 8))
        
        log_frame = tk.Frame(
            main_container, 
            bg='#38444D',
            highlightbackground='#657786', 
            highlightthickness=1,
            relief=tk.SOLID,
            borderwidth=1
        )
        log_frame.pack(fill=tk.BOTH, pady=(0, 0))
        
        self.log_text = tk.Text(
            log_frame,
            wrap=tk.WORD,
            height=5,
            font=("Monaco", 11),
            bg='#253341',
            fg='#E8F5FD',
            relief=tk.FLAT,
            padx=10,
            pady=10,
            state=tk.DISABLED,
            borderwidth=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Add initial log entry
        if self.authenticated:
            self.log("✓ Bot authenticated successfully")
        else:
            self.log("✗ Authentication failed. Check credentials")
            
    def create_glass_button(self, parent, text, command, bg_color, large=False):
        """Create a modern glass-style button"""
        if large:
            font = ("Arial", 15, "bold")
            padx, pady = 20, 12
        else:
            font = ("Arial", 13)
            padx, pady = 15, 8
            
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg_color,
            fg='white',
            font=font,
            relief=tk.FLAT,
            cursor='hand2',
            padx=padx,
            pady=pady,
            activebackground=self.lighten_color(bg_color),
            activeforeground='white',
            borderwidth=0,
            highlightthickness=0
        )
        
        # Hover effects
        button.bind('<Enter>', lambda e: button.config(bg=self.lighten_color(bg_color)))
        button.bind('<Leave>', lambda e: button.config(bg=bg_color))
        
        return button
    
    def lighten_color(self, hex_color):
        """Lighten a hex color for hover effect"""
        # Simple lightening by increasing RGB values
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 20)
        g = min(255, g + 20)
        b = min(255, b + 20)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def update_character_count(self, event=None):
        """Update character count as user types"""
        text = self.tweet_text.get("1.0", tk.END).strip()
        char_count = len(text)
        
        self.char_count_label.config(text=f"{char_count} / 280")
        
        if char_count > 280:
            self.char_count_label.config(fg="#E0245E")  # Red
        elif char_count > 260:
            self.char_count_label.config(fg="#FFAD1F")  # Orange
        else:
            self.char_count_label.config(fg="#8899A6")  # Gray
            
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
            self.selected_images = list(files)[:4]
            count = len(self.selected_images)
            
            if count == 1:
                self.images_label.config(text=f"✓ 1 image selected", fg="#17BF63")
            else:
                self.images_label.config(text=f"✓ {count} images selected", fg="#17BF63")
            
            for img in self.selected_images:
                self.log(f"📎 Added: {img.split('/')[-1]}")
                
    def clear_images(self):
        """Clear selected images"""
        self.selected_images = []
        self.images_label.config(text="No images selected", fg="#8899A6")
        self.log("✗ Cleared all images")
        
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
        self.log("✗ Cleared tweet text")
        
    def post_tweet(self):
        """Post the tweet"""
        if not self.authenticated:
            messagebox.showerror(
                "Not Authenticated",
                "Bot is not authenticated. Please check your credentials."
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
                response = self.bot.post_tweet_with_media(tweet_text, self.selected_images)
            else:
                response = self.bot.post_tweet(tweet_text)
            
            self.root.after(0, self._post_success, response, tweet_text)
            
        except Exception as e:
            self.root.after(0, self._post_error, str(e))
            
    def _post_success(self, response, tweet_text):
        """Handle successful post"""
        self.post_button.config(state=tk.NORMAL, text="🚀 Post Tweet")
        
        if response and response.data:
            tweet_id = response.data.get('id', 'unknown')
            
            self.log(f"✓ Tweet posted successfully!")
            self.log(f"  ID: {tweet_id}")
            
            messagebox.showinfo(
                "Success! 🎉",
                f"Your tweet was posted successfully!\n\nTweet ID: {tweet_id}"
            )
            
            # Clear after successful post
            self.clear_text()
            self.clear_images()
        else:
            self.log("⚠ Tweet may have been posted")
            
    def _post_error(self, error_msg):
        """Handle post error"""
        self.post_button.config(state=tk.NORMAL, text="🚀 Post Tweet")
        self.log(f"✗ Error: {error_msg}")
        messagebox.showerror("Error", f"Failed to post tweet:\n\n{error_msg}")
        
    def get_tweets(self):
        """Get recent tweets"""
        if not self.authenticated:
            messagebox.showerror(
                "Not Authenticated",
                "Bot is not authenticated."
            )
            return
        
        self.log("📥 Fetching recent tweets...")
        
        thread = threading.Thread(target=self._get_tweets_thread)
        thread.daemon = True
        thread.start()
        
    def _get_tweets_thread(self):
        """Get tweets in background thread"""
        try:
            tweets = self.bot.get_my_tweets(max_results=5)
            self.root.after(0, self._show_tweets, tweets)
        except Exception as e:
            self.root.after(0, lambda: self.log(f"✗ Error fetching tweets: {e}"))
            
    def _show_tweets(self, tweets):
        """Display retrieved tweets"""
        if tweets:
            self.log(f"✓ Retrieved {len(tweets)} tweets")
            
            # Create popup window
            popup = tk.Toplevel(self.root)
            popup.title("Recent Tweets")
            popup.geometry("600x450")
            popup.configure(bg='#15202B')
            popup.attributes('-alpha', 0.95)
            
            # Container
            container = tk.Frame(popup, bg='#15202B', padx=20, pady=20)
            container.pack(fill=tk.BOTH, expand=True)
            
            title = tk.Label(
                container,
                text="Recent Tweets",
                font=("SF Pro Display", 20, "bold"),
                fg='white',
                bg='#15202B'
            )
            title.pack(pady=(0, 15))
            
            # Text area for tweets
            text_frame = tk.Frame(container, bg='#192734', highlightbackground='#38444D', highlightthickness=1)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            text_widget = tk.Text(
                text_frame,
                wrap=tk.WORD,
                font=("SF Pro Text", 12),
                bg='#192734',
                fg='white',
                padx=15,
                pady=15,
                relief=tk.FLAT
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            
            for i, tweet in enumerate(tweets, 1):
                text_widget.insert(tk.END, f"═══ Tweet #{i} ═══\n", "bold")
                text_widget.insert(tk.END, f"{tweet.text}\n\n")
                
                if hasattr(tweet, 'created_at'):
                    text_widget.insert(tk.END, f"📅 {tweet.created_at}\n")
                
                if hasattr(tweet, 'public_metrics'):
                    metrics = tweet.public_metrics
                    text_widget.insert(
                        tk.END,
                        f"❤️ {metrics['like_count']}  "
                        f"🔄 {metrics['retweet_count']}  "
                        f"💬 {metrics['reply_count']}\n"
                    )
                
                text_widget.insert(tk.END, "\n\n")
            
            text_widget.config(state=tk.DISABLED)
        else:
            self.log("⚠ No tweets found")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernXBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

