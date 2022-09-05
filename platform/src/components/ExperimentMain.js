import Toolbar from "./Toolbar/Toolbar";
import Dashboard from "./Dashboard/Dashboard";
import ExperimentChart from "./ExperimentChart/ExperimentChart";
import {
  useState,
  useEffect,
  useRef
} from "react";

const App = () => {
    const [sessionData, setSessionData] = useState([]);
    const [previousResults, setPreviousResults] = useState([]);
    const webSocket = useRef(null);

    // const sessionData = [
    //   { StepCount: 0, AgentCount: 4000 },
    //   { StepCount: 1, AgentCount: 1243 },
    //   { StepCount: 2, AgentCount: 2234 },
    //   { StepCount: 3, AgentCount: 3456 },
    //   { StepCount: 4, AgentCount: 5678 },
    //   { StepCount: 5, AgentCount: 7891 },
    //   { StepCount: 6, AgentCount: 9012 },
    //   { StepCount: 7, AgentCount: 10123 },
    // ];

    useEffect(() => {
      webSocket.current = new WebSocket("ws://localhost:8080/ExperimentData");
      webSocket.current.onopen = () => {
        console.log("Connected to server");
      }
      webSocket.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // console.log(data);
        setSessionData((current) => [...current, data]);
      }
      webSocket.current.onclose = () => {
        console.log("Disconnected from server");
        webSocket.current.close();
      }
      return () => {
        webSocket.current.close();
      }
    }, []);

    // console.log(sessionData[sessionData.length - 1]);

    useEffect(() => {
      if (sessionData.length === 0) {
        setPreviousResults([{
          CycleCount: 0,
          DooderCount: 0,
          EnergyCount: 0,
          DirectionCounts: {}
        }]);
      } else {
        setPreviousResults(sessionData[sessionData.length - 1]);
      }
    }, [sessionData]);

  
  return (
    <div>
      <Toolbar socket={webSocket} setter={setSessionData}/>
      <Dashboard data={previousResults}/>
      <ExperimentChart data={sessionData} />
    </div>
  );
};

export default App;
