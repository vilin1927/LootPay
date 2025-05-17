import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot.main import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main()) 