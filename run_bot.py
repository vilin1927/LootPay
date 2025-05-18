import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ["BOT_TOKEN"] = "7733706741:AAF18qUbqoKWPLzWECSQXsC3XkxKjeXPz5U"  # Replace with your actual bot token
os.environ["ADMIN_IDS"] = "1708729"  # Replace with your actual Telegram ID

from main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main()) 