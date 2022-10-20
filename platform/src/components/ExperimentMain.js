import Toolbar from "./Toolbar/Toolbar";
import Dashboard from "./Dashboard/Dashboard";
import Box from "@mui/material/Box";
import ExperimentChart from "./ExperimentChart/ExperimentChart";
import { useState, useEffect, useRef } from "react";
import DooderCycle from "./Charts/DooderCycle";
import EnergyCycle from "./Charts/EnergyCycle";
import Grid from "@mui/material/Grid";

const App = () => {
  const [sessionData, setSessionData] = useState([]);
  const [previousResults, setPreviousResults] = useState([]);
  const webSocket = useRef(null);

  useEffect(() => {
    webSocket.current = new WebSocket("ws://localhost:8080/ExperimentData");
    webSocket.current.onopen = () => {
      console.log("Connected to server");
    };
    webSocket.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // console.log(data);
      setSessionData((current) => [...current, data]);
    };
    webSocket.current.onclose = () => {
      console.log("Disconnected from server");
      webSocket.current.close();
    };
    return () => {
      webSocket.current.close();
    };
  }, []);

  // console.log(sessionData[sessionData.length - 1]);

  useEffect(() => {
    if (sessionData.length === 0) {
      setPreviousResults([
        {
          CycleCount: 0,
          DooderCount: 0,
          EnergyCount: 0,
          DirectionCounts: {},
        },
      ]);
    } else {
      setPreviousResults(sessionData[sessionData.length - 1]);
    }
  }, [sessionData]);

  return (
    <div>
      <Toolbar socket={webSocket} setter={setSessionData} />
      <Dashboard data={previousResults} />
      <ExperimentChart data={sessionData} />
      <Grid container spacing={2}>
        <Grid item sm={6}>
          <Box textAlign="center">
            <EnergyCycle />
          </Box>
        </Grid>
        <Grid item sm={6}>
          <Box textAlign="center">
            <DooderCycle />
          </Box>
        </Grid>
      </Grid>
    </div>
  );
};

export default App;
