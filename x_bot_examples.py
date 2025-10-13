#!/usr/bin/env python3
"""
X Bot Examples
Various examples of how to use the X Bot
"""

from x_bot import XBot
from datetime import datetime
import time


def example_simple_tweet():
    """Example 1: Post a simple tweet"""
    print("\n=== Example 1: Simple Tweet ===")
    bot = XBot()
    bot.post_tweet("Hello from my X bot! 🤖 This is a test tweet.")


def example_tweet_with_image():
    """Example 2: Post a tweet with an image"""
    print("\n=== Example 2: Tweet with Image ===")
    bot = XBot()
    
    # Make sure you have an image file to test with
    image_path = "test_image.jpg"
    bot.post_tweet_with_media(
        "Check out this image! 📸",
        [image_path]
    )


def example_status_update():
    """Example 3: Post a status update with timestamp"""
    print("\n=== Example 3: Status Update ===")
    bot = XBot()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = f"""
🤖 Bot Status Update

✅ System Online
🕐 Time: {timestamp}
💚 All systems operational

#automation #bot
    """.strip()
    
    bot.post_tweet(status)


def example_announcement():
    """Example 4: Post an announcement"""
    print("\n=== Example 4: Announcement ===")
    bot = XBot()
    
    announcement = """
📢 New Feature Released!

We just launched X Bot with:
• Post tweets programmatically
• Upload media
• Reply to tweets
• Retrieve timeline

Check it out! 🚀

#python #automation
    """.strip()
    
    bot.post_tweet(announcement)


def example_get_recent_tweets():
    """Example 5: Get your recent tweets"""
    print("\n=== Example 5: Get Recent Tweets ===")
    bot = XBot()
    
    tweets = bot.get_my_tweets(max_results=5)
    print(f"\nRetrieved {len(tweets)} tweets")


def example_reply_to_tweet():
    """Example 6: Reply to a tweet"""
    print("\n=== Example 6: Reply to Tweet ===")
    bot = XBot()
    
    # Replace with an actual tweet ID you want to reply to
    tweet_id = "1234567890"  # Example ID
    bot.post_tweet(
        "Thanks for sharing! 🙏",
        reply_to=tweet_id
    )


def example_scheduled_posts():
    """Example 7: Simulated scheduled posting"""
    print("\n=== Example 7: Scheduled Posts (Demo) ===")
    bot = XBot()
    
    messages = [
        "🌅 Good morning! Starting the day strong.",
        "☕ Coffee break time! How's your day going?",
        "🌆 Afternoon check-in. Keep up the great work!",
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"\nPost {i}/{len(messages)}: {message}")
        bot.post_tweet(message)
        
        # In real scheduled posting, you'd use a proper scheduler
        # This is just a demo with delays
        if i < len(messages):
            print("Waiting 10 seconds before next post...")
            time.sleep(10)


def example_thread_simulation():
    """Example 8: Post a thread (multiple tweets)"""
    print("\n=== Example 8: Thread Simulation ===")
    bot = XBot()
    
    thread = [
        "🧵 Thread: Top 5 Python Tips\n\n1/5",
        "Tip #1: Use list comprehensions for cleaner code\n[x*2 for x in range(10)]\n\n2/5",
        "Tip #2: Use f-strings for formatting\nname = 'Python'\nprint(f'Hello, {name}!')\n\n3/5",
        "Tip #3: Use context managers (with statements)\nwith open('file.txt') as f:\n    data = f.read()\n\n4/5",
        "Tip #4: Use enumerate() instead of range(len())\nfor i, item in enumerate(items):\n    print(i, item)\n\n5/5",
        "That's it! Hope these tips help! 💡\n\nLike & RT if you found this useful! 🙏"
    ]
    
    previous_tweet_id = None
    
    for tweet in thread:
        response = bot.post_tweet(tweet, reply_to=previous_tweet_id)
        
        if response and response.data:
            previous_tweet_id = response.data['id']
            print(f"Posted tweet ID: {previous_tweet_id}")
            time.sleep(2)  # Be respectful of rate limits


def example_daily_stats():
    """Example 9: Post daily statistics"""
    print("\n=== Example 9: Daily Stats ===")
    bot = XBot()
    
    # In a real scenario, you'd calculate these from actual data
    stats = """
📊 Daily Report - {date}

✅ Tasks completed: 15
🔄 In progress: 3
⏸️ Pending: 2
📈 Productivity: 95%

Great day! 🎉

#productivity #automation
    """.format(date=datetime.now().strftime("%B %d, %Y"))
    
    bot.post_tweet(stats.strip())


def example_error_handling():
    """Example 10: Proper error handling"""
    print("\n=== Example 10: Error Handling ===")
    bot = XBot()
    
    # Example of handling potential errors
    try:
        # Try to post a very long tweet (will be automatically truncated)
        long_tweet = "This is a very long tweet! " * 50
        bot.post_tweet(long_tweet)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("But the bot handled it gracefully!")


def main():
    """Run examples"""
    print("╔════════════════════════════════════════╗")
    print("║         X Bot Examples                 ║")
    print("╚════════════════════════════════════════╝")
    print("\nChoose an example to run:")
    print("1. Simple tweet")
    print("2. Tweet with image")
    print("3. Status update")
    print("4. Announcement")
    print("5. Get recent tweets")
    print("6. Reply to tweet")
    print("7. Scheduled posts (demo)")
    print("8. Thread simulation")
    print("9. Daily stats")
    print("10. Error handling")
    print("0. Run all examples (be careful of rate limits!)")
    
    choice = input("\nEnter your choice (0-10): ").strip()
    
    examples = {
        '1': example_simple_tweet,
        '2': example_tweet_with_image,
        '3': example_status_update,
        '4': example_announcement,
        '5': example_get_recent_tweets,
        '6': example_reply_to_tweet,
        '7': example_scheduled_posts,
        '8': example_thread_simulation,
        '9': example_daily_stats,
        '10': example_error_handling,
    }
    
    if choice == '0':
        print("\n⚠️  Warning: Running all examples will post multiple tweets!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        if confirm == 'yes':
            for example in examples.values():
                try:
                    example()
                    time.sleep(5)  # Rate limit protection
                except Exception as e:
                    print(f"Error in example: {e}")
        else:
            print("Cancelled.")
    elif choice in examples:
        examples[choice]()
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()

