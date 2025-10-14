#!/usr/bin/env python3
"""
X Bot Simple GUI - Guaranteed macOS Compatible
Basic, clean interface that actually works
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import threading
from x_bot import XBot
from datetime import datetime


class SimpleXBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X Bot - Tweet Composer")
        self.root.geometry("600x700")
        self.root.configure(bg='white')
        
        # Initialize bot
        self.bot = None
        self.authenticated = False
        self.selected_images = []
        
        # Authenticate
        try:
            self.bot = XBot()
            if self.bot.client:
                self.authenticated = True
        except:
            self.authenticated = False
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        """Create simple, visible widgets"""
        
        # Padding frame
        main = tk.Frame(self.root, bg='white', padx=30, pady=20)
        main.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            main,
            text="🐦 X Bot",
            font=("Arial", 28, "bold"),
            bg='white',
            fg='#1DA1F2'
        )
        title.pack(pady=(0, 5))
        
        subtitle = tk.Label(
            main,
            text="Tweet Composer",
            font=("Arial", 14),
            bg='white',
            fg='gray'
        )
        subtitle.pack(pady=(0, 20))
        
        # Status
        status_text = "✅ Connected" if self.authenticated else "❌ Not Connected"
        status_color = "green" if self.authenticated else "red"
        
        status = tk.Label(
            main,
            text=status_text,
            font=("Arial", 12, "bold"),
            bg='white',
            fg=status_color
        )
        status.pack(pady=(0, 20))
        
        # Compose label
        compose_label = tk.Label(
            main,
            text="Compose Your Tweet:",
            font=("Arial", 14, "bold"),
            bg='white',
            fg='black',
            anchor='w'
        )
        compose_label.pack(fill=tk.X, pady=(0, 5))
        
        # Tweet text area - SUPER VISIBLE VERSION
        self.tweet_text = tk.Text(
            main,
            font=("Arial", 16),
            wrap=tk.WORD,
            height=10,
            width=45,
            bg='lightyellow',
            fg='black',
            insertbackground='blue',
            relief=tk.SOLID,
            borderwidth=3,
            highlightthickness=2,
            highlightbackground='blue',
            highlightcolor='blue',
            padx=15,
            pady=15
        )
        self.tweet_text.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        self.tweet_text.bind('<KeyRelease>', self.update_count)
        
        # Character counter
        self.count_label = tk.Label(
            main,
            text="0 / 280 characters",
            font=("Arial", 11),
            bg='white',
            fg='gray',
            anchor='e'
        )
        self.count_label.pack(fill=tk.X, pady=(0, 15))
        
        # Media section
        media_label = tk.Label(
            main,
            text="Attach Images (Optional):",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='black',
            anchor='w'
        )
        media_label.pack(fill=tk.X, pady=(10, 5))
        
        media_btns = tk.Frame(main, bg='white')
        media_btns.pack(fill=tk.X, pady=(0, 5))
        
        btn_add = tk.Button(
            media_btns,
            text="📎 Add Images",
            command=self.add_images,
            font=("Arial", 12),
            bg='#1DA1F2',
            fg='white',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_add.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_clear_imgs = tk.Button(
            media_btns,
            text="✕ Clear Images",
            command=self.clear_images,
            font=("Arial", 12),
            bg='lightgray',
            fg='black',
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn_clear_imgs.pack(side=tk.LEFT)
        
        self.img_label = tk.Label(
            main,
            text="No images selected",
            font=("Arial", 11),
            bg='white',
            fg='gray',
            anchor='w'
        )
        self.img_label.pack(fill=tk.X, pady=(0, 15))
        
        # Main action buttons
        btn_frame = tk.Frame(main, bg='white')
        btn_frame.pack(fill=tk.X, pady=(10, 15))
        
        self.post_btn = tk.Button(
            btn_frame,
            text="🚀 POST TWEET",
            command=self.post_tweet,
            font=("Arial", 14, "bold"),
            bg='#1DA1F2',
            fg='white',
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.post_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        btn_clear = tk.Button(
            btn_frame,
            text="Clear",
            command=self.clear_text,
            font=("Arial", 12),
            bg='lightgray',
            fg='black',
            padx=20,
            pady=12,
            cursor='hand2'
        )
        btn_clear.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_tweets = tk.Button(
            btn_frame,
            text="My Tweets",
            command=self.get_tweets,
            font=("Arial", 12),
            bg='#17BF63',
            fg='white',
            padx=20,
            pady=12,
            cursor='hand2'
        )
        btn_tweets.pack(side=tk.LEFT)
        
        # Activity log
        log_label = tk.Label(
            main,
            text="Activity Log:",
            font=("Arial", 12, "bold"),
            bg='white',
            fg='black',
            anchor='w'
        )
        log_label.pack(fill=tk.X, pady=(10, 5))
        
        self.log_text = tk.Text(
            main,
            font=("Monaco", 11),
            wrap=tk.WORD,
            height=6,
            width=45,
            bg='lightblue',
            fg='black',
            relief=tk.SOLID,
            borderwidth=2,
            highlightthickness=1,
            highlightbackground='gray',
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, pady=(0, 0))
        
        # Initial log
        if self.authenticated:
            self.log("✅ Bot authenticated successfully!")
        else:
            self.log("❌ Authentication failed. Check credentials.")
    
    def update_count(self, event=None):
        """Update character count"""
        text = self.tweet_text.get("1.0", tk.END).strip()
        count = len(text)
        self.count_label.config(text=f"{count} / 280 characters")
        
        if count > 280:
            self.count_label.config(fg='red')
        elif count > 260:
            self.count_label.config(fg='orange')
        else:
            self.count_label.config(fg='gray')
    
    def add_images(self):
        """Add images"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.gif"), ("All", "*.*")]
        )
        if files:
            self.selected_images = list(files)[:4]
            count = len(self.selected_images)
            self.img_label.config(
                text=f"✅ {count} image{'s' if count > 1 else ''} selected",
                fg='green'
            )
            for img in self.selected_images:
                self.log(f"📎 Added: {img.split('/')[-1]}")
    
    def clear_images(self):
        """Clear images"""
        self.selected_images = []
        self.img_label.config(text="No images selected", fg='gray')
        self.log("🗑️ Cleared images")
    
    def clear_text(self):
        """Clear tweet text"""
        self.tweet_text.delete("1.0", tk.END)
        self.update_count()
        self.log("🗑️ Cleared text")
    
    def log(self, msg):
        """Add to log"""
        time = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"[{time}] {msg}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def post_tweet(self):
        """Post tweet"""
        if not self.authenticated:
            messagebox.showerror("Error", "Not authenticated!")
            return
        
        text = self.tweet_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Empty", "Please write something!")
            return
        
        self.post_btn.config(state=tk.DISABLED, text="Posting...")
        threading.Thread(target=self._post, args=(text,), daemon=True).start()
    
    def _post(self, text):
        """Post in thread"""
        try:
            if self.selected_images:
                resp = self.bot.post_tweet_with_media(text, self.selected_images)
            else:
                resp = self.bot.post_tweet(text)
            
            self.root.after(0, self._post_success, resp)
        except Exception as e:
            self.root.after(0, self._post_error, str(e))
    
    def _post_success(self, resp):
        """Handle success"""
        self.post_btn.config(state=tk.NORMAL, text="🚀 POST TWEET")
        if resp and resp.data:
            tweet_id = resp.data.get('id')
            self.log(f"✅ Tweet posted! ID: {tweet_id}")
            messagebox.showinfo("Success!", f"Tweet posted!\nID: {tweet_id}")
            self.clear_text()
            self.clear_images()
        else:
            self.log("⚠️ Posted but no confirmation")
    
    def _post_error(self, error):
        """Handle error"""
        self.post_btn.config(state=tk.NORMAL, text="🚀 POST TWEET")
        self.log(f"❌ Error: {error}")
        messagebox.showerror("Error", f"Failed:\n{error}")
    
    def get_tweets(self):
        """Get tweets"""
        if not self.authenticated:
            messagebox.showerror("Error", "Not authenticated!")
            return
        
        self.log("📥 Fetching tweets...")
        threading.Thread(target=self._get_tweets, daemon=True).start()
    
    def _get_tweets(self):
        """Get tweets in thread"""
        try:
            tweets = self.bot.get_my_tweets(max_results=5)
            self.root.after(0, self._show_tweets, tweets)
        except Exception as e:
            self.root.after(0, lambda: self.log(f"❌ Error: {e}"))
    
    def _show_tweets(self, tweets):
        """Show tweets"""
        if tweets:
            self.log(f"✅ Got {len(tweets)} tweets")
            msg = "\n\n".join([f"Tweet {i}:\n{t.text}" for i, t in enumerate(tweets, 1)])
            messagebox.showinfo("Recent Tweets", msg[:500])
        else:
            self.log("⚠️ No tweets found")


def main():
    root = tk.Tk()
    app = SimpleXBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

