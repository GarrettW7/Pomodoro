import time
from playMusic import download_audio, startPomodoroSound, stopMusic1, resumeMusic, pauseMusic, cheering, playMusic1
from timer import pomodoroTimer
import threading
from AIsongFinder import search_youtube

def definePomodoro():
    print()
    print("Pomodoro is a time management technique that uses a timer to break down work into intervals, usually 25 or 50 minutes in length, separated by short breaks!")
    print("Would you like to start a Pomodoro session? (yes/no) " )
    response = input()
    if response == "yes":
        print("-----------------------")
        print("Note: Maximum efficiency pomodoros are 25 minutes or 50 minutes.")
        workTime = input("How long do you want your pomodoro to be? (in minutes) \n" )
        numSessions = int(input("How many Pomodoro sessions would you like to do? \n" ))
        print()

        response = input("Would you like to:\n 1) Reuse the last used music \n 2) Get new music with AI help \n 3) Type in the URL of music you would like (Type \"1\", \"2\", or \"3\".) \n" )
        
        if response == "1":
            print("Reusing last music.")
        elif response == "2":
            print("Getting new music with AI help.")
            print("Please enter the genre of music you would like to listen to. \n" )
            genre = input()
            print()
            tempURLs = search_youtube(genre, (int(workTime) * numSessions))
            download_audio(tempURLs, numSessions)
            print("Music downloaded!\n-----------------------\n")
        elif response == "3":
            print("Please enter the URL of the youtube video you would like to download music from. \n" )
            url = input()
            download_audio(url, 1)
            print("Music downloaded!\n-----------------------\n")
        else:
            print("No new music downloaded!\n-----------------------\n")

        tempFlag = True 
        sessionsPassed = 0
        while numSessions > sessionsPassed:
            print(f"Starting session number {sessionsPassed + 1} out of {numSessions}!")
            if tempFlag:
                musicThread = startPomodoro(int(workTime))
                tempFlag = False
            else:
                resumeMusic()
                resumePomodoro(int(workTime), musicThread)
            sessionsPassed += 1
        stopMusic1()
        cheering()
        print("All Pomodoro sessions completed!")
    else:
        print("Maybe next time!")

def startPomodoro(workTime):
    breakTime = workTime / 5
    print()
    print('----------------------------')
    print("Starting a " + str(workTime) + " minute Pomodoro session at " + time.strftime("%H:%M:%S"))
    print(f"The next break wille be at {time.strftime('%H:%M:%S', time.localtime(time.time() + workTime * 60))} and will last {breakTime} minutes.")
    print('----------------------------')
    print()

    
    timer_thread = threading.Thread(target=pomodoroTimer, args=(workTime,), daemon=True)
    music_thread = threading.Thread(target=startPomodoroSound, daemon=True)
    timer_thread.start()
    music_thread.start()

    timer_thread.join()  # Wait for the timer thread to finish
    pauseMusic()
    music_thread.join()  # Wait for the music thread to finish

    print("Pomodoro session completed. Taking a break now.\n-----------------------\n")
    return music_thread

def resumePomodoro(workTime, musicThread):
    playMusic1()
    breakTime = workTime / 5
    print()
    print('----------------------------')
    print("Starting a " + str(workTime) + " minute Pomodoro session at " + time.strftime("%H:%M:%S"))
    print(f"The next break wille be at {time.strftime('%H:%M:%S', time.localtime(time.time() + workTime * 60))} and will last {breakTime} minutes.")
    print('----------------------------')
    print()

    
    timer_thread = threading.Thread(target=pomodoroTimer, args=(workTime,), daemon=True)

    timer_thread.start()


    timer_thread.join()  # Wait for the timer thread to finish
    pauseMusic()
    musicThread.join()  # Wait for the music thread to finish


    print("Pomodoro session completed. Taking a break now.")

definePomodoro()

