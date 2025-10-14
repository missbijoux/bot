#!/usr/bin/env python3
"""
X Bot Enhanced GUI - Advanced Graphical Interface
Features: Tweet scheduling, auto-reply management, keyword monitoring
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import json
from datetime import datetime, timedelta
from x_bot_enhanced import XBotEnhanced
import os


class XBotEnhancedGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("X Bot Enhanced - Tweet Composer & Scheduler 🐦")
        self.root.geometry("900x800")
        self.root.resizable(True, True)
        
        # Initialize bot
        self.bot = None
        self.authenticated = False
        self.selected_images = []
        
        # Try to authenticate
        self.authenticate_bot()
        
        # Create GUI
        self.create_widgets()
        
        # Start background processes if authenticated
        if self.authenticated:
            self.start_background_processes()
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        # Configure root window
        self.root.configure(bg='#1e1e1e')
        
        # Create custom style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure colors for dark theme
        self.colors = {
            'bg': '#1e1e1e',           # Main background
            'fg': '#ffffff',           # Text color
            'select_bg': '#404040',    # Selection background
            'select_fg': '#ffffff',    # Selection text
            'entry_bg': '#2d2d2d',     # Entry background
            'entry_fg': '#ffffff',     # Entry text
            'button_bg': '#404040',    # Button background
            'button_fg': '#ffffff',    # Button text
            'accent': '#1DA1F2',       # Twitter blue
            'accent_hover': '#0d8bd9', # Twitter blue hover
            'success': '#00d4aa',      # Success green
            'warning': '#ffad1f',      # Warning orange
            'error': '#f4212e',        # Error red
            'border': '#404040',       # Border color
            'header_bg': '#1DA1F2',    # Header background
            'header_fg': '#ffffff',    # Header text
            'frame_bg': '#252525',     # Frame background
            'tree_bg': '#2d2d2d',      # Treeview background
            'tree_select': '#404040'   # Treeview selection
        }
        
        # Configure ttk styles
        self.style.configure('TNotebook', background=self.colors['bg'])
        self.style.configure('TNotebook.Tab', background=self.colors['bg'], foreground=self.colors['fg'])
        self.style.map('TNotebook.Tab', background=[('selected', self.colors['accent'])])
        
        # Frame styles
        self.style.configure('TFrame', background=self.colors['bg'])
        self.style.configure('Dark.TFrame', background=self.colors['frame_bg'])
        
        # Label styles
        self.style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        self.style.configure('Header.TLabel', background=self.colors['header_bg'], foreground=self.colors['header_fg'], font=('Arial', 16, 'bold'))
        self.style.configure('Status.TLabel', background=self.colors['bg'], foreground=self.colors['fg'], font=('Arial', 10))
        
        # Button styles
        self.style.configure('TButton', background=self.colors['button_bg'], foreground=self.colors['button_fg'])
        self.style.map('TButton', background=[('active', self.colors['accent_hover'])])
        self.style.configure('Accent.TButton', background=self.colors['accent'], foreground='white')
        self.style.map('Accent.TButton', background=[('active', self.colors['accent_hover'])])
        
        # Entry styles
        self.style.configure('TEntry', fieldbackground=self.colors['entry_bg'], foreground=self.colors['entry_fg'], bordercolor=self.colors['border'])
        
        # Treeview styles
        self.style.configure('Treeview', background=self.colors['tree_bg'], foreground=self.colors['fg'], fieldbackground=self.colors['tree_bg'])
        self.style.map('Treeview', background=[('selected', self.colors['tree_select'])])
        
        # Scrollbar styles
        self.style.configure('Vertical.TScrollbar', background=self.colors['bg'], troughcolor=self.colors['frame_bg'], bordercolor=self.colors['border'])
        
        # LabelFrame styles
        self.style.configure('TLabelframe', background=self.colors['frame_bg'])
        self.style.configure('TLabelframe.Label', background=self.colors['frame_bg'], foreground=self.colors['fg'])
        
    def authenticate_bot(self):
        """Try to authenticate with X API"""
        try:
            self.bot = XBotEnhanced()
            if self.bot.api:
                self.authenticated = True
                print("✓ Authenticated successfully")
        except Exception as e:
            self.authenticated = False
            print(f"❌ Authentication failed: {e}")
            
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_compose_tab()
        self.create_schedule_tab()
        self.create_auto_reply_tab()
        self.create_monitor_tab()
        
        # Status bar
        self.create_status_bar()
        
    def create_compose_tab(self):
        """Create the main tweet composition tab"""
        compose_frame = ttk.Frame(self.notebook)
        self.notebook.add(compose_frame, text="📝 Compose")
        
        # Header
        header_frame = tk.Frame(compose_frame, bg=self.colors['header_bg'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🐦 X Bot Enhanced - Compose Tweet",
            font=("Arial", 16, "bold"),
            fg=self.colors['header_fg'],
            bg=self.colors['header_bg']
        )
        title_label.pack(pady=15)
        
        # Main content
        main_frame = ttk.Frame(compose_frame, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tweet composition area
        compose_label = ttk.Label(main_frame, text="What's happening?", font=("Arial", 12, "bold"))
        compose_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.tweet_text = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            width=60,
            font=("Arial", 11),
            wrap=tk.WORD,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['select_bg'],
            selectforeground=self.colors['select_fg']
        )
        self.tweet_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Character count
        self.char_count_label = ttk.Label(main_frame, text="0/280 characters", font=("Arial", 10))
        self.char_count_label.pack(anchor=tk.E)
        
        # Bind character count update
        self.tweet_text.bind('<KeyRelease>', self.update_char_count)
        
        # Media section
        media_frame = ttk.LabelFrame(main_frame, text="📸 Media Files", padding=10)
        media_frame.pack(fill=tk.X, pady=(15, 10))
        
        media_buttons_frame = ttk.Frame(media_frame)
        media_buttons_frame.pack(fill=tk.X)
        
        ttk.Button(
            media_buttons_frame,
            text="Add Images",
            command=self.add_images
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            media_buttons_frame,
            text="Clear Images",
            command=self.clear_images
        ).pack(side=tk.LEFT)
        
        self.media_listbox = tk.Listbox(
            media_frame, 
            height=3,
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            selectbackground=self.colors['select_bg'],
            selectforeground=self.colors['select_fg']
        )
        self.media_listbox.pack(fill=tk.X, pady=(10, 0))
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="🚀 Post Tweet",
            command=self.post_tweet,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="📅 Schedule Tweet",
            command=self.schedule_tweet_dialog
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_tweet
        ).pack(side=tk.LEFT)
        
    def create_schedule_tab(self):
        """Create the tweet scheduling tab"""
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="📅 Schedule")
        
        # Header
        header_frame = tk.Frame(schedule_frame, bg=self.colors['header_bg'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📅 Tweet Scheduler",
            font=("Arial", 16, "bold"),
            fg=self.colors['header_fg'],
            bg=self.colors['header_bg']
        )
        title_label.pack(pady=15)
        
        # Main content
        main_frame = ttk.Frame(schedule_frame, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Scheduler controls
        control_frame = ttk.LabelFrame(main_frame, text="Scheduler Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.scheduler_status = ttk.Label(control_frame, text="Status: Stopped", font=("Arial", 10))
        self.scheduler_status.pack(anchor=tk.W, pady=(0, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_scheduler_btn = ttk.Button(
            button_frame,
            text="▶️ Start Scheduler",
            command=self.start_scheduler
        )
        self.start_scheduler_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_scheduler_btn = ttk.Button(
            button_frame,
            text="⏹️ Stop Scheduler",
            command=self.stop_scheduler,
            state=tk.DISABLED
        )
        self.stop_scheduler_btn.pack(side=tk.LEFT)
        
        # Scheduled tweets list
        list_frame = ttk.LabelFrame(main_frame, text="Scheduled Tweets", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for scheduled tweets
        columns = ("ID", "Content", "Scheduled Time", "Status")
        self.schedule_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=150)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=scrollbar.set)
        
        self.schedule_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Refresh button
        ttk.Button(
            list_frame,
            text="🔄 Refresh List",
            command=self.refresh_scheduled_tweets
        ).pack(pady=(10, 0))
        
        # Load initial data
        self.refresh_scheduled_tweets()
        
    def create_auto_reply_tab(self):
        """Create the auto-reply management tab"""
        reply_frame = ttk.Frame(self.notebook)
        self.notebook.add(reply_frame, text="🤖 Auto-Reply")
        
        # Header
        header_frame = tk.Frame(reply_frame, bg=self.colors['header_bg'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Auto-Reply Manager",
            font=("Arial", 16, "bold"),
            fg=self.colors['header_fg'],
            bg=self.colors['header_bg']
        )
        title_label.pack(pady=15)
        
        # Main content
        main_frame = ttk.Frame(reply_frame, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Auto-reply controls
        control_frame = ttk.LabelFrame(main_frame, text="Auto-Reply Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.auto_reply_status = ttk.Label(control_frame, text="Status: Stopped", font=("Arial", 10))
        self.auto_reply_status.pack(anchor=tk.W, pady=(0, 10))
        
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X)
        
        self.start_auto_reply_btn = ttk.Button(
            button_frame,
            text="▶️ Start Auto-Reply",
            command=self.start_auto_reply
        )
        self.start_auto_reply_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_auto_reply_btn = ttk.Button(
            button_frame,
            text="⏹️ Stop Auto-Reply",
            command=self.stop_auto_reply,
            state=tk.DISABLED
        )
        self.stop_auto_reply_btn.pack(side=tk.LEFT)
        
        # Add new rule section
        rule_frame = ttk.LabelFrame(main_frame, text="Add New Auto-Reply Rule", padding=10)
        rule_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Keyword input
        ttk.Label(rule_frame, text="Keyword:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.keyword_entry = ttk.Entry(rule_frame, width=30)
        self.keyword_entry.grid(row=0, column=1, padx=(0, 10))
        
        # Response input
        ttk.Label(rule_frame, text="Response:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.response_entry = ttk.Entry(rule_frame, width=50)
        self.response_entry.grid(row=1, column=1, padx=(0, 10), pady=(10, 0))
        
        # Add rule button
        ttk.Button(
            rule_frame,
            text="➕ Add Rule",
            command=self.add_auto_reply_rule
        ).grid(row=1, column=2, padx=(10, 0), pady=(10, 0))
        
        # Rules list
        rules_frame = ttk.LabelFrame(main_frame, text="Auto-Reply Rules", padding=10)
        rules_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for rules
        rule_columns = ("Keyword", "Response")
        self.rules_tree = ttk.Treeview(rules_frame, columns=rule_columns, show="headings", height=8)
        
        for col in rule_columns:
            self.rules_tree.heading(col, text=col)
            self.rules_tree.column(col, width=200)
        
        # Scrollbar for rules treeview
        rules_scrollbar = ttk.Scrollbar(rules_frame, orient=tk.VERTICAL, command=self.rules_tree.yview)
        self.rules_tree.configure(yscrollcommand=rules_scrollbar.set)
        
        self.rules_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        rules_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load initial rules
        self.refresh_auto_reply_rules()
        
    def create_monitor_tab(self):
        """Create the monitoring tab"""
        monitor_frame = ttk.Frame(self.notebook)
        self.notebook.add(monitor_frame, text="📊 Monitor")
        
        # Header
        header_frame = tk.Frame(monitor_frame, bg=self.colors['header_bg'], height=60)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="📊 Activity Monitor",
            font=("Arial", 16, "bold"),
            fg=self.colors['header_fg'],
            bg=self.colors['header_bg']
        )
        title_label.pack(pady=15)
        
        # Main content
        main_frame = ttk.Frame(monitor_frame, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Status information
        status_frame = ttk.LabelFrame(main_frame, text="Bot Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.auth_status = ttk.Label(status_frame, text="Authentication: Checking...", font=("Arial", 10))
        self.auth_status.pack(anchor=tk.W, pady=(0, 5))
        
        self.scheduler_status_monitor = ttk.Label(status_frame, text="Scheduler: Stopped", font=("Arial", 10))
        self.scheduler_status_monitor.pack(anchor=tk.W, pady=(0, 5))
        
        self.auto_reply_status_monitor = ttk.Label(status_frame, text="Auto-Reply: Stopped", font=("Arial", 10))
        self.auto_reply_status_monitor.pack(anchor=tk.W)
        
        # Recent activity
        activity_frame = ttk.LabelFrame(main_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill=tk.BOTH, expand=True)
        
        self.activity_text = scrolledtext.ScrolledText(
            activity_frame,
            height=15,
            width=80,
            font=("Consolas", 9),
            bg=self.colors['entry_bg'],
            fg=self.colors['entry_fg'],
            insertbackground=self.colors['fg'],
            selectbackground=self.colors['select_bg'],
            selectforeground=self.colors['select_fg']
        )
        self.activity_text.pack(fill=tk.BOTH, expand=True)
        
        # Add some initial activity
        self.log_activity("Bot initialized")
        if self.authenticated:
            self.log_activity("✓ Successfully authenticated with X API")
        else:
            self.log_activity("❌ Authentication failed - check credentials")
        
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(
            self.status_bar,
            text="Ready" if self.authenticated else "Authentication Required",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
    # ===== EVENT HANDLERS =====
    
    def update_char_count(self, event=None):
        """Update character count"""
        count = len(self.tweet_text.get("1.0", tk.END).strip())
        self.char_count_label.config(text=f"{count}/280 characters")
        
        # Change color if approaching limit
        if count > 260:
            self.char_count_label.config(foreground="red")
        elif count > 240:
            self.char_count_label.config(foreground="orange")
        else:
            self.char_count_label.config(foreground="black")
    
    def add_images(self):
        """Add images to the tweet"""
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        for file in files:
            if len(self.selected_images) < 4:  # Twitter limit
                self.selected_images.append(file)
                self.media_listbox.insert(tk.END, os.path.basename(file))
            else:
                messagebox.showwarning("Too Many Images", "Twitter allows maximum 4 images per tweet")
                break
    
    def clear_images(self):
        """Clear selected images"""
        self.selected_images.clear()
        self.media_listbox.delete(0, tk.END)
    
    def post_tweet(self):
        """Post the current tweet"""
        if not self.authenticated:
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        content = self.tweet_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter some content")
            return
        
        if len(content) > 280:
            messagebox.showerror("Error", "Tweet is too long (max 280 characters)")
            return
        
        # Post tweet in a separate thread
        threading.Thread(target=self._post_tweet_thread, args=(content,), daemon=True).start()
    
    def _post_tweet_thread(self, content):
        """Post tweet in background thread"""
        try:
            if self.selected_images:
                tweet_id = self.bot.post_tweet_with_media(content, self.selected_images)
            else:
                tweet_id = self.bot.post_tweet(content)
            
            if tweet_id:
                self.root.after(0, lambda: messagebox.showinfo("Success", "Tweet posted successfully!"))
                self.root.after(0, self.clear_tweet)
                self.root.after(0, lambda: self.log_activity(f"✓ Tweet posted: {content[:50]}..."))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "Failed to post tweet"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to post tweet: {e}"))
    
    def schedule_tweet_dialog(self):
        """Open schedule tweet dialog"""
        if not self.authenticated:
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        content = self.tweet_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "Please enter some content")
            return
        
        if len(content) > 280:
            messagebox.showerror("Error", "Tweet is too long (max 280 characters)")
            return
        
        # Create schedule dialog
        dialog = ScheduleDialog(self.root, content, self.selected_images, self.bot)
        if dialog.result:
            self.refresh_scheduled_tweets()
            self.log_activity(f"📅 Tweet scheduled: {content[:50]}...")
    
    def clear_tweet(self):
        """Clear the tweet composition"""
        self.tweet_text.delete("1.0", tk.END)
        self.clear_images()
        self.update_char_count()
    
    def start_scheduler(self):
        """Start the tweet scheduler"""
        if not self.authenticated:
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        try:
            self.bot.start_scheduler()
            self.scheduler_status.config(text="Status: Running")
            self.scheduler_status_monitor.config(text="Scheduler: Running")
            self.start_scheduler_btn.config(state=tk.DISABLED)
            self.stop_scheduler_btn.config(state=tk.NORMAL)
            self.log_activity("✓ Tweet scheduler started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start scheduler: {e}")
    
    def stop_scheduler(self):
        """Stop the tweet scheduler"""
        try:
            self.bot.stop_scheduler()
            self.scheduler_status.config(text="Status: Stopped")
            self.scheduler_status_monitor.config(text="Scheduler: Stopped")
            self.start_scheduler_btn.config(state=tk.NORMAL)
            self.stop_scheduler_btn.config(state=tk.DISABLED)
            self.log_activity("⏹️ Tweet scheduler stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop scheduler: {e}")
    
    def start_auto_reply(self):
        """Start auto-reply monitoring"""
        if not self.authenticated:
            messagebox.showerror("Error", "Please authenticate first")
            return
        
        try:
            self.bot.start_auto_reply()
            self.auto_reply_status.config(text="Status: Running")
            self.auto_reply_status_monitor.config(text="Auto-Reply: Running")
            self.start_auto_reply_btn.config(state=tk.DISABLED)
            self.stop_auto_reply_btn.config(state=tk.NORMAL)
            self.log_activity("✓ Auto-reply monitor started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start auto-reply: {e}")
    
    def stop_auto_reply(self):
        """Stop auto-reply monitoring"""
        try:
            self.bot.stop_auto_reply()
            self.auto_reply_status.config(text="Status: Stopped")
            self.auto_reply_status_monitor.config(text="Auto-Reply: Stopped")
            self.start_auto_reply_btn.config(state=tk.NORMAL)
            self.stop_auto_reply_btn.config(state=tk.DISABLED)
            self.log_activity("⏹️ Auto-reply monitor stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop auto-reply: {e}")
    
    def add_auto_reply_rule(self):
        """Add a new auto-reply rule"""
        keyword = self.keyword_entry.get().strip()
        response = self.response_entry.get().strip()
        
        if not keyword or not response:
            messagebox.showwarning("Warning", "Please enter both keyword and response")
            return
        
        try:
            self.bot.add_auto_reply_rule(keyword, response)
            self.keyword_entry.delete(0, tk.END)
            self.response_entry.delete(0, tk.END)
            self.refresh_auto_reply_rules()
            self.log_activity(f"➕ Added auto-reply rule: '{keyword}' → '{response}'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add rule: {e}")
    
    def refresh_scheduled_tweets(self):
        """Refresh the scheduled tweets list"""
        try:
            # Clear existing items
            for item in self.schedule_tree.get_children():
                self.schedule_tree.delete(item)
            
            # Get scheduled tweets
            tweets = self.bot.get_scheduled_tweets()
            for tweet in tweets:
                tweet_id, content, scheduled_time, media_files, reply_to_tweet_id = tweet
                self.schedule_tree.insert("", tk.END, values=(
                    tweet_id,
                    content[:50] + "..." if len(content) > 50 else content,
                    scheduled_time,
                    "Pending"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh scheduled tweets: {e}")
    
    def refresh_auto_reply_rules(self):
        """Refresh the auto-reply rules list"""
        try:
            # Clear existing items
            for item in self.rules_tree.get_children():
                self.rules_tree.delete(item)
            
            # Get auto-reply rules
            rules = self.bot.get_auto_reply_rules()
            for keyword, response in rules.items():
                self.rules_tree.insert("", tk.END, values=(keyword, response))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to refresh auto-reply rules: {e}")
    
    def start_background_processes(self):
        """Start background monitoring processes"""
        # Update status
        self.auth_status.config(text="Authentication: ✓ Connected")
        
        # Refresh data
        self.refresh_scheduled_tweets()
        self.refresh_auto_reply_rules()
    
    def log_activity(self, message):
        """Log activity to the monitor tab"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.activity_text.insert(tk.END, log_message)
        self.activity_text.see(tk.END)


class ScheduleDialog:
    """Dialog for scheduling tweets"""
    
    def __init__(self, parent, content, media_files, bot):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Schedule Tweet")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        
        # Center the dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create widgets
        self.create_widgets(content, media_files, bot)
        
        # Center dialog on parent
        self.center_on_parent(parent)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self, content, media_files, bot):
        """Create dialog widgets"""
        # Apply dark theme to dialog
        self.dialog.configure(bg='#1e1e1e')
        
        main_frame = ttk.Frame(self.dialog, padding=20, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Content preview
        ttk.Label(main_frame, text="Tweet Content:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        content_text = tk.Text(
            main_frame, 
            height=4, 
            width=50, 
            wrap=tk.WORD,
            bg='#2d2d2d',
            fg='#ffffff',
            insertbackground='#ffffff',
            selectbackground='#404040',
            selectforeground='#ffffff'
        )
        content_text.pack(fill=tk.X, pady=(5, 15))
        content_text.insert("1.0", content)
        content_text.config(state=tk.DISABLED)
        
        # Schedule time
        ttk.Label(main_frame, text="Schedule for:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        time_frame = ttk.Frame(main_frame)
        time_frame.pack(fill=tk.X, pady=(5, 15))
        
        # Date entry
        ttk.Label(time_frame, text="Date:").pack(side=tk.LEFT, padx=(0, 5))
        self.date_entry = ttk.Entry(time_frame, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Time entry
        ttk.Label(time_frame, text="Time:").pack(side=tk.LEFT, padx=(0, 5))
        self.time_entry = ttk.Entry(time_frame, width=8)
        self.time_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.time_entry.insert(0, (datetime.now() + timedelta(minutes=5)).strftime("%H:%M"))
        
        # Quick options
        quick_frame = ttk.Frame(main_frame)
        quick_frame.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Button(quick_frame, text="+5 min", command=lambda: self.add_minutes(5)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="+15 min", command=lambda: self.add_minutes(15)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="+1 hour", command=lambda: self.add_minutes(60)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_frame, text="Tomorrow", command=self.set_tomorrow).pack(side=tk.LEFT, padx=(0, 5))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Schedule", command=lambda: self.schedule_tweet(bot, content, media_files)).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # Store references
        self.bot = bot
        self.content = content
        self.media_files = media_files
    
    def center_on_parent(self, parent):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = (parent.winfo_x() + (parent.winfo_width() // 2) - (self.dialog.winfo_width() // 2))
        y = (parent.winfo_y() + (parent.winfo_height() // 2) - (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
    
    def add_minutes(self, minutes):
        """Add minutes to current time"""
        try:
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            dt = datetime.fromisoformat(f"{date_str} {time_str}")
            new_dt = dt + timedelta(minutes=minutes)
            
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, new_dt.strftime("%Y-%m-%d"))
            self.time_entry.delete(0, tk.END)
            self.time_entry.insert(0, new_dt.strftime("%H:%M"))
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format")
    
    def set_tomorrow(self):
        """Set time to tomorrow at 9 AM"""
        tomorrow = datetime.now() + timedelta(days=1)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, tomorrow.strftime("%Y-%m-%d"))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, "09:00")
    
    def schedule_tweet(self, bot, content, media_files):
        """Schedule the tweet"""
        try:
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            scheduled_time = datetime.fromisoformat(f"{date_str} {time_str}")
            
            if scheduled_time <= datetime.now():
                messagebox.showerror("Error", "Scheduled time must be in the future")
                return
            
            bot.schedule_tweet(content, scheduled_time, media_files)
            self.result = True
            messagebox.showinfo("Success", "Tweet scheduled successfully!")
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date/time format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule tweet: {e}")


def main():
    """Main function to run the enhanced GUI"""
    root = tk.Tk()
    
    # Create and run the application
    app = XBotEnhancedGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nShutting down...")
        if app.bot:
            app.bot.stop_scheduler()
            app.bot.stop_auto_reply()


if __name__ == "__main__":
    main()
