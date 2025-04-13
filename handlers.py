
import os
import aiohttp
from aiogram import types, Bot
from ffmpeg_process import run_ffmpeg

VIDEO_DIR = "videos"
STATIC_URL = "https://raw.githubusercontent.com/Skshayed1/telegram_video_bot/main/static/"

async def download_file(file: types.File, bot: Bot, dest: str):
    await bot.download_file(file.file_path, destination=dest)

async def handle_videos(message: types.Message, bot: Bot):
    if not message.video and not message.document:
        await message.reply("দয়া করে ভিডিও পাঠান।")
        return

    os.makedirs(VIDEO_DIR, exist_ok=True)
    user_id = str(message.from_user.id)
    user_dir = os.path.join(VIDEO_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    video_files = [msg.video or msg.document async for msg in bot.get_chat_history(message.chat.id, limit=5) if msg.video or msg.document]
    if len(video_files) < 2:
        await message.reply("দয়া করে একসাথে ২টা ভিডিও পাঠান। (Main + MyVideo)")
        return

    v_path = os.path.join(user_dir, "v.mp4")
    myvideo_path = os.path.join(user_dir, "myvideo.mp4")

    await download_file(await bot.get_file(video_files[1].file_id), bot, v_path)
    await download_file(await bot.get_file(video_files[0].file_id), bot, myvideo_path)

    # Download static files
    for name in ["blocker.mp4", "ibg.mp4", "bg2.mp4"]:
        url = STATIC_URL + name
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                with open(os.path.join(user_dir, name), "wb") as f:
                    f.write(await resp.read())

    output_path = os.path.join(user_dir, "output.mp4")
    await run_ffmpeg(user_dir, output_path)

    if os.path.exists(output_path):
        await bot.send_video(chat_id=message.chat.id, video=FSInputFile(output_path), caption="এখানে তোমার প্রসেস করা ভিডিও!")
    else:
        await message.reply("কোনো সমস্যা হয়েছে প্রসেসিং এ।")
