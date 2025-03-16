import yt_dlp


def download_video(url, output_path="video.mp4"):
    ydl_opts = {
        'outtmpl': output_path,  # Save as "video.mp4"
        'format': 'bestvideo+bestaudio/best',  # Best quality video + audio
        'merge_output_format': 'mp4',  # Ensure MP4 format
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, output_path="audio"):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

#---------------------------------------------------#

import subprocess
import os
import signal

# def playMusic():
#     subprocess.run(["ffplay", "-nodisp", "-autoexit", "audio.wav.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def ding():
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "ding.wav"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Global variable to store the music process
music_process = None


def playMusic1():
    """Starts playing music using ffplay in the background."""
    global music_process
    if music_process is None:  # Prevent multiple music instances
        music_process = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "audio.wav"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def pauseMusic():
    """Pauses the currently playing music."""
    global music_process
    if music_process is not None:
        os.kill(music_process.pid, signal.SIGSTOP)  # Sends the pause signal


def resumeMusic():
    """Resumes the paused music."""
    global music_process
    if music_process is not None:
        os.kill(music_process.pid, signal.SIGCONT)  # Sends the continue signal

def stopMusic1():
    """Stops the music process if it's running."""
    global music_process
    if music_process:
        music_process.terminate()  # Kill the process
        music_process = None
        print("Music stopped.")


def startPomodoroSound():
    ding()
    playMusic1()

