import time
import threading
from playMusic import ding, pauseMusic, resumeMusic, playMusic1, stopMusic2

def start_timer(minutes, callback):
    seconds = minutes * 60
    time.sleep(seconds)
    callback()

def oneFifth():
    print(f"Current time is: {time.strftime('%H:%M:%S')} One fifth of the way there!")

def twoFiths():
    print(f"Current time is: {time.strftime('%H:%M:%S')} Two fifths of the way there!")

def threeFiths():
    print(f"Current time is: {time.strftime('%H:%M:%S')} Three fifths of the way there!")

def fourFiths():
    print(f"Current time is: {time.strftime('%H:%M:%S')} Four fifths of the way there!")

def fiveFiths(oneFifthTime):
    print(f"Current time is: {time.strftime('%H:%M:%S')} You are done! Time to take a break!")
    print(f"Your break will end at {time.strftime('%H:%M:%S', time.localtime(time.time() + oneFifthTime * 60))}")
    ding()
    pauseMusic()

    
def oneFifthBreak(oneFifthTime):
    start_timer(oneFifthTime, fiveFiths)


def breakTime():
    playMusic1()
    print(f"Current time is: {time.strftime('%H:%M:%S')} --- Break is OVER! Time to get back to work!\n")
    ding()


def pomodoroTimer(totalTime):
    oneFifthTime = totalTime / 5

    start_timer(oneFifthTime, oneFifth)

    start_timer(oneFifthTime, twoFiths)
    start_timer(oneFifthTime, threeFiths)
    start_timer(oneFifthTime, fourFiths)
    start_timer(oneFifthTime, lambda: fiveFiths(oneFifthTime=oneFifthTime))
    # pauseMusic()

    """
    This ideally would play the intermission music for the duration of the break

    timer_thread = threading.Thread(target=oneFifthBreak, args=(oneFifthTime), daemon=True)
    intermission_music_thread = threading.Thread(target=playMusic2, daemon=True)
    timer_thread.start()
    intermission_music_thread.start()

    timer_thread.join()  # Wait for the timer thread to finish
    stopMusic2()
    intermission_music_thread.join() "
    """

    start_timer(oneFifthTime, breakTime)




# Example usage: start a timer for 1 minute
# start_timer(1, my_function)