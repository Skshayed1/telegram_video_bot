
import subprocess
import os

async def run_ffmpeg(dir_path, output_path):
    cmd = f"""ffmpeg -y -i {dir_path}/v.mp4 -i {dir_path}/blocker.mp4 -i {dir_path}/myvideo.mp4 -filter_complex \
"[0:v]crop=iw/1.2:ih/1.2, scale=392x315, setpts=PTS/1[v]; \
movie={dir_path}/ibg.mp4:loop=999,setpts=N/(FRAME_RATE*TB) [bg];[bg][v]overlay=shortest=1:x=2:y=107,setsar=1:1[vmain]; \
[1:v]scale=854x480,setsar=1:1[vblock];[2:v]scale=854x480,setsar=1:1[vgam]; \
[0:a]atempo=1,bass=frequency=200:gain=-90,volume=+20dB,aecho=1:0.6:2:0.4,bass=g=3:f=110:w=20, \
bass=g=10:f=500:w=20,bass=g=3:f=300:w=30,bass=g=10:f=110:w=20,bass=g=20:f=110:w=40, \
firequalizer=gain_entry='entry(0,-23);entry(250,-11.5);entry(6000,0);entry(12000,8);entry(16000,16)', \
compand=attacks=7:decays=1:points=-90/-90 -70/-60 -15/-15 0/-10: soft-knee=1:volume=-70:gain=3, \
pan=stereo| FL < FL + 0.5*FC + 0.6*BL + 0.6*SL | FR < FR + 2*FC + 1*BR + 2*SR,highpass=f=300,lowpass=f=700,volume=6[a1]; \
amovie={dir_path}/bg2.mp4:loop=9999,volume=1[a2];[a1][a2]amix=duration=shortest[amain]; \
[vmain][amain][vblock][1:a][vgam][2:a]concat=n=3:v=1:a=1" \
-vcodec libx264 -pix_fmt yuv420p -r 30 -g 60 -b:v 1000k -shortest -acodec aac -b:a 128k -ar 44100 -threads 0 {output_path}
"""
    subprocess.call(cmd, shell=True)
