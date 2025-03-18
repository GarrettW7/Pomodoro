import yt_dlp


def download_video(url, numSessions, output_path="video.mp4"):
    # for i in range(numSessions):
    #     ydl_opts = {
    #         'outtmpl': f"{output_path}{i}" ,  # Save as "video.mp4"
    #         'format': 'bestvideo+bestaudio/best',  # Best quality video + audio
    #         'merge_output_format': 'mp4',  # Ensure MP4 format
    #     }
    ydl_opts = {
        'outtmpl': output_path,  # Save as "video.mp4"
        'format': 'bestvideo+bestaudio/best',  # Best quality video + audio
        'merge_output_format': 'mp4',  # Ensure MP4 format
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url, numSessions, output_path="audio"):
    # for i in range(numSessions):
    #     ydl_opts = {
    #         'outtmpl': f"{output_path}{i}" ,  # Save as "video.mp4"
    #         'format': 'bestvideo+bestaudio/best',  # Best quality video + audio
    #         'merge_output_format': 'mp4',  # Ensure MP4 format
    #     }
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

def playMusic2():
    """Starts playing music using ffplay in the background."""
    global intermission_process
    if intermission_process is None:  # Prevent multiple music instances
        intermission_process = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "intermission.wav"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def stopMusic2():
    """Stops the music process if it's running."""
    global intermission_process
    if intermission_process:
        intermission_process.terminate()  # Kill the process
        intermission_process = None


# Global variables to store the music process
music_process = None
intermission_process = None


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

