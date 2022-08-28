import { useState } from "react";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import Navbar from "./components/Navbar/Navbar";

const App = () => {
  const [data, setData] = useState("");
  const [err, setErr] = useState("");
  const [agent_count_list, SetList] = useState([]);

  const stopExperiment = () => {
    fetch("http://localhost:8080/stop")
      .then((res) => res.json())
      .then((res) => {
        setData(res);
      })
      .catch((err) => {
        setErr(err);
      });
  };

  const startExperiment = () => {
    fetch("http://localhost:8080/start")
      .then((res) => res.json())
      .then((res) => {
        setData(res);
      })
      .catch((err) => {
        setErr(err);
      });
  };

  const resetExperiment = () => {
    fetch("http://localhost:8080/reset")
      .then((res) => res.json())
      .then((res) => {
        setData(res);
      })
      .catch((err) => {
        setErr(err);
      });
  };

  const ws = new WebSocket("ws://localhost:8080/test");
  ws.onmessage = (event) => {
    const number = document.getElementById("number");
    const message = document.getElementById("message");
    const data = JSON.parse(event.data);
    SetList((current) => [...current, data]);
    number.innerHTML = data.agent_count;
    message.innerHTML = data.message;
  };
  const handleOnClick = () => {
    ws.send(
      JSON.stringify({
        message: "hello",
      })
    );
  };

  return (
    
    <div>
      <section className="bg-black ">
        <Container fixed>
          <div className="relative w-full max-w-xs m-auto">
            <Button variant="contained" onClick={startExperiment}>
              Start
            </Button>
          </div>
          <div className="relative w-full max-w-xs m-auto">
            <Button variant="contained" onClick={stopExperiment}>
              Stop
            </Button>
          </div>
          <Button variant="contained" onClick={resetExperiment}>
            Reset
          </Button>
        </Container>
      </section>

      {data && (
        <div>
          <h2>Data:</h2>
          <pre>{JSON.stringify(data, null, 4)}</pre>
        </div>
      )}

      <Button variant="contained" onClick={handleOnClick}>
        Click Me
      </Button>
      <div id="message">hi</div>
      <div id="number">0</div>

      <Container maxWidth="lg">
        <Container maxWidth="sm">
          <LineChart width={600} height={300} data={agent_count_list}>
            <Line type="monotone" dataKey="AgentCount" stroke="#8884d8" />
            <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
            <XAxis dataKey="StepCount" />
            <YAxis />
            <Tooltip />
            <Legend />
          </LineChart>
        </Container>

        <LineChart
          width={730}
          height={250}
          data={agent_count_list}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="StepCount" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="AgentCount" stroke="#8884d8" />
        </LineChart>
      </Container>
    </div>
  );
};

export default App;
