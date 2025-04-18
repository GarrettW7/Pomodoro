import flask
from flask import request, jsonify
from flask_cors import CORS
import atexit
# -------------- Imports from main.py --------------
import time
from playMusic import download_audio, startPomodoroSound, stopMusic1, resumeMusic, pauseMusic, cheering, playMusic1,ding
from timer import pomodoroTimer
import threading
from AIsongFinder import search_youtube
# -------------------------------------------------


app = flask.Flask(__name__)
CORS(app) 

def onShutdown():
    print("\n\nEdits detected, shutting down the server...\n")
    print("Stopping music...\n\n")
    stopMusic1()
    # os.kill(os.getpid(), signal.SIGINT)  # Terminates the Flask process

atexit.register(onShutdown)
# Register the shutdown function to be called on exit

#---- Testing -----

sessionLength = 0
numSessions = 0
musicType = "Whatchu doing here"
dataCompiled = [sessionLength, numSessions, musicType]

@app.route("/shutdown", methods=["POST"])
def shutdown():
    print("Stopping music...")
    stopMusic1()
    
    # if request.method == "POST":
    #     os.kill(os.getpid(), signal.SIGINT)  # Terminates the Flask process
    return "Stopped music!", 200

@app.route('/processData', methods=['GET'])
def getData():
    return jsonify({"dataCompiled": dataCompiled})

@app.route('/processData', methods=['POST'])
def processData():
    if request.method == 'POST':
        data = request.json  # Get JSON data from request
        if "dataUpdated" not in data:  # Basic validation
            return jsonify({"error": "Missing 'dataUpdated' field"}), 400
        
        dataUpdated = data["dataUpdated"]
        print(dataUpdated)
        sessionLength = int(dataUpdated[0])
        numSessions = int(dataUpdated[1])
        musicType = dataUpdated[2]

        if musicType == "000":
            musicType = "Recycling music"

        print(f"Session Length: {sessionLength}")
        print(f"Number of Sessions: {numSessions}")
        print(f"Music Type: {musicType}")

        if musicType != "Recycling music":
            tempURLs = search_youtube(musicType, (sessionLength * numSessions))
            download_audio(tempURLs, numSessions)
            print("Music downloaded!\n-----------------------\n")


        tempFlag = True 
        sessionsPassed = 0
        while numSessions > sessionsPassed:
            print(f"Starting session number {sessionsPassed + 1} out of {numSessions}!")
            # for i in range(1, 6):
            #     timer_thread = threading.Thread(target=pomodoroTimer, args=(sessionLength,), daemon=True)
            #     music_thread = threading.Thread(target=startPomodoroSound, daemon=True)
            #     timer_thread.start()
            #     music_thread.start()

            #     timer_thread.join()  # Wait for the timer thread to finish
            # pauseMusic()
            # music_thread.join()  # Wait for the music thread to finish
            if tempFlag:
                musicThread = startPomodoro(int(sessionLength))
                tempFlag = False
            else:
                resumeMusic()
                resumePomodoro(int(sessionLength), musicThread)
            sessionsPassed += 1
        stopMusic1()
        cheering()
        print("All Pomodoro sessions completed!")
        ding()

        return jsonify({"message": "All the data was received", "dataUpdated": dataUpdated}), 201

    # Handle GET request (return tasks)
    return jsonify({"dataCompiled": dataCompiled})

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)