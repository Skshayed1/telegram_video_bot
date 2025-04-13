
import os
import telebot
import subprocess

TOKEN = os.getenv("7566271591:AAH2D1vGfAIK8lZyEpacZEVWssA7KPSUpEY")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send the main video file (v.mp4) to get started.")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        input_path = "/app/v.mp4"
        with open(input_path, 'wb') as f:
            f.write(downloaded_file)

        cmd = ("ffmpeg -y -i /app/v.mp4 -i /app/blocker.mp4 -i /app/myvideo.mp4 "
               "-filter_complex "[0:v]crop=iw/1.2:ih/1.2, scale=392x315, setpts=PTS/1,hflip[v]; "
               "movie=/app/ibg.mp4:loop=999,setpts=N/(FRAME_RATE*TB)[bg];[bg][v]overlay=shortest=1:x=2:y=107,setsar=1:1[vmain]; "
               "[1:v]scale=854x480,setsar=1:1[vblock]; [2:v]scale=854x480,setsar=1:1[vgam]; "
               "[0:a]atempo=1,bass=frequency=200:gain=-90,volume=+20dB,aecho=1:0.6:2:0.4,"
               "bass=g=3:f=110:w=20,bass=g=10:f=500:w=20,bass=g=3:f=300:w=30,bass=g=10:f=110:w=20,"
               "bass=g=20:f=110:w=40,firequalizer=gain_entry='entry(0,-23);entry(250,-11.5);entry(6000,0);"
               "entry(12000,8);entry(16000,16)',compand=attacks=7:decays=1:points=-90/-90 -70/-60 -15/-15 "
               "0/-10:soft-knee=1:volume=-70:gain=3,pan=stereo|FL<FL+0.5*FC+0.6*BL+0.6*SL|FR<FR+2*FC+1*BR+2*SR,"
               "highpass=f=300,lowpass=f=700,volume=6[a1];amovie=/app/bg2.mp4:loop=9999,volume=1[a2];"
               "[a1][a2]amix=duration=shortest[amain];[vmain][amain][vblock][1:a][vgam][2:a]concat=n=3:v=1:a=1" "
               "-vcodec libx264 -pix_fmt yuv420p -r 30 -g 60 -b:v 1000k -shortest -acodec aac -b:a 128k "
               "-ar 44100 -threads 0 /app/'Half Screen Successful By STech Pro.mp4'")

        subprocess.run(cmd, shell=True)
        with open("/app/Half Screen Successful By STech Pro.mp4", "rb") as out:
            bot.send_video(message.chat.id, out)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

bot.polling()
