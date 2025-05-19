import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN
from handlers import qual_questions


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Register routers
dp.include_router(qual_questions.router)

async def main():
    """Main function to start the bot"""
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())