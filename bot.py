
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from ffmpeg_command import run_ffmpeg

BOT_TOKEN = os.getenv("7566271591:AAH2D1vGfAIK8lZyEpacZEVWssA7KPSUpEY")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send your 'v.mp4' and 'myvideo.mp4'. Make sure to name them like that!")

video_files = {}

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("Please send a valid video file.")
        return

    file_name = file.file_name
    if file_name not in ["v.mp4", "myvideo.mp4"]:
        await update.message.reply_text("Send only v.mp4 and myvideo.mp4.")
        return

    file_path = f"{user_id}_{file_name}"
    new_file = await file.get_file()
    await new_file.download_to_drive(file_path)
    video_files.setdefault(user_id, {})[file_name] = file_path

    if "v.mp4" in video_files[user_id] and "myvideo.mp4" in video_files[user_id]:
        await update.message.reply_text("Processing your video...")
        output_path = f"{user_id}_output.mp4"
        try:
            run_ffmpeg(video_files[user_id]["v.mp4"], video_files[user_id]["myvideo.mp4"], output_path)
            await update.message.reply_video(video=open(output_path, 'rb'))
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        finally:
            os.remove(video_files[user_id]["v.mp4"])
            os.remove(video_files[user_id]["myvideo.mp4"])
            os.remove(output_path)
            video_files[user_id] = {}

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))

if __name__ == "__main__":
    app.run_polling()
