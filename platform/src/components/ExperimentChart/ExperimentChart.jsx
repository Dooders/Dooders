import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";
import Container from "@mui/material/Container";
import { useState, useEffect } from "react";

const ExperimentChart = ({ data }) => {
  const [chartData, setChartData] = useState([]);

  // put this in the app so I dont create two copies of same data
  useEffect(() => {
    // if data is empty then set chart data to default values
    if (data.length === 0) {
      setChartData([{ CycleCount: 0, DooderCount: 0, EnergyCount: 0 }]);
    }
    // otherwise set chart data to data
    else {
      setChartData(data);
    }
  }, [data]);

  // const data = [
  //   { StepCount: 0, AgentCount: 4000 },
  //   { StepCount: 1, AgentCount: 1243 },
  //   { StepCount: 2, AgentCount: 2234 },
  //   { StepCount: 3, AgentCount: 3456 },
  //   { StepCount: 4, AgentCount: 5678 },
  //   { StepCount: 5, AgentCount: 7891 },
  //   { StepCount: 6, AgentCount: 9012 },
  //   { StepCount: 7, AgentCount: 10123 },
  // ];

  console.log(chartData[chartData.length - 1]);

  return (
    <div>
      <Container maxWidth="lg">
        <Container maxWidth="lg">
          <LineChart width={1000} height={500} data={chartData}>
            <Line type="natural" dataKey="DooderCount" stroke="#0B5F0B" />
            <Line type="natural" dataKey="EnergyCount" stroke="#84210C" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="CycleCount" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        </Container>
      </Container>
    </div>
  );
};

export default ExperimentChart;
