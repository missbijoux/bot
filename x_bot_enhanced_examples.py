#!/usr/bin/env python3
"""
X Bot Enhanced Examples
Demonstrates advanced features: scheduling, auto-replies, keyword monitoring
"""

from x_bot_enhanced import XBotEnhanced
from datetime import datetime, timedelta
import time
import json


def example_schedule_tweets():
    """Example 1: Schedule multiple tweets"""
    print("\n=== Example 1: Schedule Multiple Tweets ===")
    
    bot = XBotEnhanced()
    
    # Schedule tweets for different times
    now = datetime.now()
    
    # Schedule a tweet for 5 minutes from now
    tweet1_time = now + timedelta(minutes=5)
    bot.schedule_tweet("🚀 This tweet was scheduled 5 minutes in advance!", tweet1_time)
    
    # Schedule a tweet for tomorrow at 9 AM
    tomorrow_9am = (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    bot.schedule_tweet("🌅 Good morning! This is a scheduled morning tweet.", tomorrow_9am)
    
    # Schedule a tweet for next week
    next_week = now + timedelta(weeks=1)
    bot.schedule_tweet("📅 Weekly reminder: Don't forget to check your goals!", next_week)
    
    print("✓ Scheduled 3 tweets for different times")
    
    # Show scheduled tweets
    scheduled = bot.get_scheduled_tweets()
    print(f"\n📋 Currently {len(scheduled)} tweets scheduled:")
    for tweet in scheduled:
        print(f"  - {tweet[2]}: {tweet[1][:50]}...")


def example_auto_reply_rules():
    """Example 2: Set up auto-reply rules"""
    print("\n=== Example 2: Auto-Reply Rules ===")
    
    bot = XBotEnhanced()
    
    # Add various auto-reply rules
    bot.add_auto_reply_rule("hello", "👋 Hello! Thanks for reaching out!")
    bot.add_auto_reply_rule("help", "🆘 I'm here to help! What can I assist you with?")
    bot.add_auto_reply_rule("bot", "🤖 Yes, I'm an automated bot! How can I help you?")
    bot.add_auto_reply_rule("weather", "🌤️ I can't check weather, but I hope it's nice where you are!")
    bot.add_auto_reply_rule("thanks", "😊 You're welcome! Happy to help!")
    bot.add_auto_reply_rule("cool", "🔥 Thanks! I think you're pretty cool too!")
    
    print("✓ Added 6 auto-reply rules")
    
    # Show all rules
    rules = bot.get_auto_reply_rules()
    print(f"\n🤖 Auto-reply rules ({len(rules)} total):")
    for keyword, response in rules.items():
        print(f"  '{keyword}' → '{response}'")


def example_advanced_scheduling():
    """Example 3: Advanced scheduling patterns"""
    print("\n=== Example 3: Advanced Scheduling Patterns ===")
    
    bot = XBotEnhanced()
    
    now = datetime.now()
    
    # Create a series of related tweets (like a thread)
    thread_tweets = [
        "🧵 Starting a mini-thread about automation!",
        "1️⃣ Automation can save you hours every day",
        "2️⃣ Start with simple repetitive tasks",
        "3️⃣ Build up to more complex workflows",
        "4️⃣ Always test thoroughly before deployment",
        "5️⃣ Automation should enhance, not replace, human creativity"
    ]
    
    # Schedule each tweet 2 minutes apart
    for i, tweet in enumerate(thread_tweets):
        tweet_time = now + timedelta(minutes=2 + (i * 2))
        bot.schedule_tweet(tweet, tweet_time)
        print(f"✓ Scheduled tweet {i+1}/6 for {tweet_time.strftime('%H:%M')}")
    
    print("\n📅 Thread scheduled with 2-minute intervals")


def example_monitoring_demo():
    """Example 4: Demonstrate monitoring capabilities"""
    print("\n=== Example 4: Monitoring Demo ===")
    
    bot = XBotEnhanced()
    
    print("📊 Bot Status:")
    print(f"  - Authenticated: {'✓' if bot.api else '❌'}")
    print(f"  - Database: ✓ {bot.db_file}")
    
    # Show scheduled tweets
    scheduled = bot.get_scheduled_tweets()
    print(f"  - Scheduled tweets: {len(scheduled)}")
    
    # Show auto-reply rules
    rules = bot.get_auto_reply_rules()
    print(f"  - Auto-reply rules: {len(rules)}")
    
    # Show recent activity (if any)
    print(f"  - Scheduler running: {'✓' if bot.scheduler_running else '❌'}")
    print(f"  - Auto-reply running: {'✓' if bot.auto_reply_running else '❌'}")


def example_business_automation():
    """Example 5: Business automation scenarios"""
    print("\n=== Example 5: Business Automation Scenarios ===")
    
    bot = XBotEnhanced()
    
    # Morning announcements
    tomorrow_8am = (datetime.now() + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
    bot.schedule_tweet("🌅 Good morning! New day, new opportunities. Let's make it great! #MotivationMonday", tomorrow_8am)
    
    # Weekly reminders
    next_monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()))
    bot.schedule_tweet("📈 Weekly reminder: Review your goals and plan for the week ahead! #Productivity", next_monday)
    
    # End of day posts
    tonight_6pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    if tonight_6pm <= datetime.now():
        tonight_6pm += timedelta(days=1)
    bot.schedule_tweet("🌙 End of day check-in: What did you accomplish today? #Reflection", tonight_6pm)
    
    # Product announcements (example)
    next_week = datetime.now() + timedelta(weeks=1)
    bot.schedule_tweet("🎉 Exciting news coming next week! Stay tuned for our big announcement! #ComingSoon", next_week)
    
    print("✓ Scheduled business automation tweets:")
    print("  - Morning motivation")
    print("  - Weekly goal reminders") 
    print("  - End-of-day reflection")
    print("  - Product announcements")


def example_customer_service_bot():
    """Example 6: Customer service automation"""
    print("\n=== Example 6: Customer Service Bot ===")
    
    bot = XBotEnhanced()
    
    # Customer service auto-replies
    customer_service_rules = {
        "order": "📦 Thanks for your order inquiry! Please DM us your order number and we'll help right away.",
        "refund": "💰 For refund requests, please contact support@company.com with your order details.",
        "shipping": "🚚 Shipping questions? Check our tracking info or DM us your order number.",
        "support": "🆘 Need help? Our support team is here for you! DM us or email support@company.com",
        "hours": "🕒 We're open Monday-Friday 9AM-6PM EST. DM us anytime and we'll respond during business hours.",
        "contact": "📞 You can reach us via DM, email (support@company.com), or phone (555-0123)",
        "complaint": "😔 We're sorry to hear about your experience. Please DM us so we can make this right.",
        "praise": "😊 Thank you so much for the kind words! We really appreciate your support!"
    }
    
    for keyword, response in customer_service_rules.items():
        bot.add_auto_reply_rule(keyword, response)
    
    print(f"✓ Set up {len(customer_service_rules)} customer service auto-reply rules")
    print("🤖 Bot will now automatically respond to common customer inquiries")


def example_content_calendar():
    """Example 7: Content calendar automation"""
    print("\n=== Example 7: Content Calendar Automation ===")
    
    bot = XBotEnhanced()
    
    # Define content themes for different days
    content_themes = {
        "Monday": "💪 Motivation Monday: Start your week with energy!",
        "Tuesday": "💡 Tip Tuesday: Here's a productivity tip for you!",
        "Wednesday": "🎯 Wisdom Wednesday: Mid-week wisdom to keep you going!",
        "Thursday": "🙏 Thankful Thursday: What are you grateful for today?",
        "Friday": "🎉 Fun Friday: Let's celebrate making it through the week!",
        "Saturday": "🌟 Saturday Spotlight: Featuring something amazing!",
        "Sunday": "🔄 Sunday Reflection: Time to reflect and plan ahead!"
    }
    
    # Schedule daily posts for the next week
    for day_offset in range(7):
        post_date = datetime.now() + timedelta(days=day_offset)
        day_name = post_date.strftime("%A")
        
        # Schedule for 10 AM each day
        post_time = post_date.replace(hour=10, minute=0, second=0, microsecond=0)
        
        if day_name in content_themes:
            bot.schedule_tweet(content_themes[day_name], post_time)
            print(f"✓ Scheduled {day_name} post for {post_time.strftime('%Y-%m-%d %H:%M')}")
    
    print("\n📅 Content calendar created for the next 7 days!")


def example_social_media_campaign():
    """Example 8: Social media campaign automation"""
    print("\n=== Example 8: Social Media Campaign ===")
    
    bot = XBotEnhanced()
    
    # Campaign launch sequence
    campaign_tweets = [
        ("🚀 Big announcement coming in 3 days! Stay tuned...", 0),
        ("⏰ 2 days until our big reveal! The countdown begins...", 1),
        ("🔥 Tomorrow is the day! Get ready for something amazing...", 2),
        ("🎉 IT'S HERE! Introducing our revolutionary new product! Check it out: [link]", 3),
        ("💫 Thank you for all the excitement! Here's what makes our product special...", 4),
        ("📊 The response has been incredible! Here are some early results...", 5),
        ("🙏 Thank you to everyone who supported our launch! You're amazing!", 6)
    ]
    
    now = datetime.now()
    
    # Schedule campaign tweets daily
    for tweet_content, day_offset in campaign_tweets:
        tweet_time = now + timedelta(days=day_offset, hours=12)  # 12 PM each day
        bot.schedule_tweet(tweet_content, tweet_time)
        print(f"✓ Scheduled day {day_offset + 1} campaign tweet")
    
    print("\n🎯 7-day social media campaign scheduled!")


def interactive_demo():
    """Interactive demo of enhanced features"""
    print("\n" + "="*60)
    print("🚀 X BOT ENHANCED - INTERACTIVE DEMO")
    print("="*60)
    
    bot = XBotEnhanced()
    
    while True:
        print("\nChoose an option:")
        print("1. Schedule a tweet")
        print("2. Add auto-reply rule")
        print("3. View scheduled tweets")
        print("4. View auto-reply rules")
        print("5. Start scheduler")
        print("6. Start auto-reply monitor")
        print("7. View bot status")
        print("8. Exit")
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            content = input("Enter tweet content: ")
            try:
                minutes = int(input("Schedule for how many minutes from now? "))
                scheduled_time = datetime.now() + timedelta(minutes=minutes)
                bot.schedule_tweet(content, scheduled_time)
                print(f"✓ Tweet scheduled for {scheduled_time}")
            except ValueError:
                print("❌ Invalid number")
        
        elif choice == "2":
            keyword = input("Enter keyword: ")
            response = input("Enter auto-reply response: ")
            bot.add_auto_reply_rule(keyword, response)
            print("✓ Auto-reply rule added")
        
        elif choice == "3":
            tweets = bot.get_scheduled_tweets()
            if tweets:
                print(f"\n📅 {len(tweets)} scheduled tweets:")
                for tweet in tweets:
                    print(f"  {tweet[2]}: {tweet[1][:50]}...")
            else:
                print("No scheduled tweets found.")
        
        elif choice == "4":
            rules = bot.get_auto_reply_rules()
            if rules:
                print(f"\n🤖 {len(rules)} auto-reply rules:")
                for keyword, response in rules.items():
                    print(f"  '{keyword}' → '{response}'")
            else:
                print("No auto-reply rules found.")
        
        elif choice == "5":
            bot.start_scheduler()
            print("✓ Scheduler started (runs in background)")
        
        elif choice == "6":
            bot.start_auto_reply()
            print("✓ Auto-reply monitor started (runs in background)")
        
        elif choice == "7":
            print(f"\n📊 Bot Status:")
            print(f"  - Authenticated: {'✓' if bot.api else '❌'}")
            print(f"  - Scheduler: {'Running' if bot.scheduler_running else 'Stopped'}")
            print(f"  - Auto-reply: {'Running' if bot.auto_reply_running else 'Stopped'}")
            print(f"  - Database: {bot.db_file}")
        
        elif choice == "8":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice")


def main():
    """Run all examples"""
    print("🐦 X Bot Enhanced Examples")
    print("=" * 50)
    
    examples = [
        ("Schedule Multiple Tweets", example_schedule_tweets),
        ("Auto-Reply Rules", example_auto_reply_rules),
        ("Advanced Scheduling", example_advanced_scheduling),
        ("Monitoring Demo", example_monitoring_demo),
        ("Business Automation", example_business_automation),
        ("Customer Service Bot", example_customer_service_bot),
        ("Content Calendar", example_content_calendar),
        ("Social Media Campaign", example_social_media_campaign),
    ]
    
    print("Available examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print("  9. Interactive Demo")
    print("  0. Run All Examples")
    
    choice = input("\nEnter your choice (0-9): ").strip()
    
    if choice == "0":
        # Run all examples
        for name, func in examples:
            print(f"\n{'='*20} {name} {'='*20}")
            try:
                func()
            except Exception as e:
                print(f"❌ Error in {name}: {e}")
    
    elif choice == "9":
        interactive_demo()
    
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        # Run specific example
        name, func = examples[int(choice) - 1]
        print(f"\n{'='*20} {name} {'='*20}")
        try:
            func()
        except Exception as e:
            print(f"❌ Error: {e}")
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
