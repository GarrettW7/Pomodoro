import { useEffect, useState } from 'react';
import './App.css';

function App() {

  //For the pomodoro session
  const [dataCompiled, setDataCompiled] = useState([]);
  const [sessionLength, setSessionLength] = useState(2);
  const [numSessions, setNumSessions] = useState(2);
  const [musicType, setMusicType] = useState("5 minutes of piano");
  const [currentTime, setCurrentTime] = useState(new Date().toLocaleTimeString());
  const [startTime, setStartTime] = useState(new Date().toLocaleTimeString());

  
  //For the loading screen
  const [showInput, setShowInput] = useState(false);
  const [showLoading, setShowLoading] = useState(false);
  const [showLoadingWords, setShowLoadingWords] = useState(false);
  
  //For the timer
  const [timeLeft, setTimeLeft] = useState(10 * 60); // 10 minutes in seconds

  window.addEventListener("beforeunload", () => {
    navigator.sendBeacon("http://127.0.0.1:5000/shutdown");
    console.log("Sent beacon");
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date().toLocaleTimeString());
    }, 1000);

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, []);


  const killMusic = () => {
    navigator.sendBeacon("http://127.0.0.1:5000/shutdown")
    console.log("Killing music!");
  }


  const updateData = () => {
    console.log("Data compiled:", sessionLength, numSessions, musicType);
    console.log("Data compiled:", dataCompiled);

    fetch("http://127.0.0.1:5000/processData", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dataUpdated: dataCompiled }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("Server response:", data);
        
      })
      .catch((err) => console.error("Error adding task:", err));
      setShowLoadingWords(true);
      setTimeLeft(sessionLength * 60); // Reset timer to session length in seconds
  };


  //The timer
  {
  useEffect(() => {
    if (timeLeft <= 0) return;

    const timer = setInterval(() => {
      setTimeLeft((prevTime) => prevTime - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft]);
}

  return (
    <div>

      <div>
        <p className='currentTime'>Current Time: {currentTime}</p>
        <button className='killButton' onClick={killMusic}>Stop Music</button>

        {showLoading == false ? (
          <div>
            <h1>Welcome to the Pomodoro Module!</h1>
            <p>Would you like to start a pomodoro session?</p>
            <button onClick={() => {setShowInput(true); setShowLoading(false)}}>Yes!</button>
          </div>
          ) : (
            <div>

              <h1>Session Details</h1>
              <h2>Session Length: {sessionLength} minutes</h2>
              <h2>Number of Sessions: {numSessions}</h2>
              <h2>Music Type: {musicType}</h2>
              {/* <p>Loading the music!</p> */}
            </div>            
          )}
          {showLoadingWords &&
            <div>
              <p>Loading... please wait</p>
              <div>
                {/* {setStartTime(new Date().toLocaleTimeString())} */}
                <p>Starting a {sessionLength} minute Pomodoro session at {startTime}</p>
                
                <p>The next break will be at {new Date(startTime + sessionLength * 60).toLocaleTimeString()} and will last {sessionLength/5} minutes.</p>
              </div>
            </div>
          }


        {showInput && (
          <form onSubmit={(e) => { e.preventDefault(); setShowInput(false); setShowLoading(true); updateData(); }}>
            <div>
              <label htmlFor="sessionLength">How long of a session do you want? (minutes) </label>
              <input
                type="number"
                id="sessionLength"
                name="sessionLength"
                value={sessionLength}
                onChange={(e) => setSessionLength(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="numSessions">How many sessions do you want to do? </label>
              <input
                type="number"
                id="numSessions"
                name="numSessions"
                value={numSessions}
                onChange={(e) => setNumSessions(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="musicType">What type of music do you want to listen to? 
                Type "000" if you want to reuse music </label>
              <input
                type="text"
                id="musicType"
                name="musicType"
                value={musicType}
                onChange={(e) => setMusicType(e.target.value)}
                required
              />
            </div>
            <button type="submit" onClick={() => setDataCompiled([sessionLength, numSessions, musicType]) } >Start Session</button>
          </form>
        )}
      </div>


{/* 
      <h1 className="Test">Here are some of my qualities</h1>
      <div className ="GettingData">
        <div>
          {data === null ? (
            <p>Loading...</p>
          ) : (
            data.tasks.map((task, i) => <p className="tempData" key={i}>{task}</p>)
          )}
        </div>
        <input
          type="text"
          placeholder="Enter more of your qualities"
          value={newTask}
          onChange={(e) => setNewTask(e.target.value)}
        />
        <button onClick={addTask}>Enter!</button>

      </div> */}
    </div>
  );
}

export default App;
