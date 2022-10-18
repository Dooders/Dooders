import Toolbar from "./Toolbar/Toolbar";
import Dashboard from "./Dashboard/Dashboard";
import Box from '@mui/material/Box';
import ExperimentChart from "./ExperimentChart/ExperimentChart";
import {
  useState,
  useEffect,
  useRef
} from "react";
import { useCubeQuery } from '@cubejs-client/react';
import { BarChart, XAxis, CartesianGrid, YAxis, Tooltip, Bar, Legend } from "recharts";


const ChartApp = () => {

  const { resultSet, isLoading, error, progress } = useCubeQuery({
    measures: ["SimulationResults.DooderCount"],
    dimensions: ["SimulationResults.CycleNumber"],
    order: [["SimulationResults.CycleNumber","asc"]]
  });
  if (isLoading) {
    return (
      <div>
        {(progress && progress.stage && progress.stage.stage) || "Loading..."}
      </div>
    );
  }

  if (error) {
    return <div>{error.toString()}</div>;
  }

  if (!resultSet) {
    return null;
  }

  return (
    <div>
      <BarChart width={1200} height={350} data={resultSet.series()[0].series}>
      <CartesianGrid strokeDasharray="5 5" />
      <XAxis dataKey="x">
      </XAxis>
      <YAxis />
      <Tooltip />
      <Legend verticalAlign="top" height={36} />
      <Bar name="DooderCount" dataKey="value" fill="#8884d8" />
      </BarChart>
    
      </div>
);
};

        


// export default ChartApp;


const App = () => {
    const [sessionData, setSessionData] = useState([]);
    const [previousResults, setPreviousResults] = useState([]);
    const webSocket = useRef(null);

    // const { resultSet, isLoading, error, progress } = useCubeQuery({
    // measures: ["SimulationResults.DooderCount"],
    // dimensions: ["SimulationResults.CycleNumber"],
    // order: [["SimulationResults.CycleNumber","asc"]]});

    // console.log(resultSet);

    // if (isLoading) {
    //   return (
    //     <div>
    //       {(progress && progress.stage && progress.stage.stage) || "Loading..."}
    //     </div>
    //   );
    // }
  
    // if (error) {
    //   return <div>{error.toString()}</div>;
    // }
  
    // if (!resultSet) {
    //   return null;
    // }
  
    // //Transform data for visualization
    // const labels = resultSet
    //   .seriesNames({
    //     x: [],
    //     y: ["Orders.createdAt"]
    //   })
    //   .map((column) => (column.value ? column.value : column.key));
  
    // const datasets = resultSet.series().map((item, i) => {
    //   return {
    //     label: item.title,
    //     data: item.series.map((item) => item.value)
    //   };
    // });


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
    <Box>
      <Toolbar socket={webSocket} setter={setSessionData}/>
      <Dashboard data={previousResults}/>
      <ExperimentChart data={sessionData} />
      <ChartApp />
    </Box>
  );
};

export default App;
