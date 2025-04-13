
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from ffmpeg_process import run_ffmpeg
from handlers import handle_videos
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("স্বাগতম! দুইটা ভিডিও পাঠাও (Main + MyVideo), তারপর বট প্রসেস করে আউটপুট দিবে।")

@dp.message()
async def video_handler(message: types.Message):
    await handle_videos(message, bot)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
