import time
from playMusic import download_audio, startPomodoroSound, stopMusic1
from timer import pomodoroTimer
import threading
from AIsongFinder import getSong

def definePomodoro():
    print()
    print("Pomodoro is a time management technique that uses a timer to break down work into intervals, usually 25 or 50 minutes in length, separated by short breaks!")
    print("Would you like to start a Pomodoro session? (yes/no) " )
    response = input()
    if response == "yes":
        print("-----------------------")
        print("Note: Maximum efficiency pomodoros are 25 minutes or 50 minutes.")
        workTime = input("How long do you want your pomodoro to be? (in minutes) \n" )
        print()

        response = input("Would you like to:\n 1) Reuse the last used music \n 2) Get new music with AI help \n 3) Type in the URL of music you would like (Type \"1\", \"2\", or \"3\".) \n" )
        
        if response == "1":
            print("Reusing last music.")
        elif response == "2":
            print("Getting new music with AI help.")
            print("Please enter the genre of music you would like to listen to. \n" )
            genre = input()
            tempURL = getSong(genre)
            download_audio(tempURL)
            print("Music downloaded!")
        if response == "3":
            print("Please enter the URL of the youtube video you would like to download music from. \n" )
            url = input()
            download_audio(url)
            print("Music downloaded!")
        else:
            print("No new music downloaded.")

        numSessions = int(input("How many Pomodoro sessions would you like to do? \n" ))
        while numSessions > 0:
            print(f"Starting Pomodoro session {numSessions- numSessions + 1}!")
            startPomodoro(int(workTime))
            numSessions -= 1
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
    stopMusic1()
    music_thread.join()  # Wait for the music thread to finish

    print("Pomodoro session completed. Taking a break now.")


definePomodoro()

