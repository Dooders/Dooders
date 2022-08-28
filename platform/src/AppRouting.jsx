import * as React from "react";
import {
  useState,
  useEffect,
  useRef
} from "react";
import { Routes, Route, Link } from "react-router-dom";
import Layout from "./Layout";
import Toolbar from "./components/Toolbar/Toolbar";
import Dashboard from "./components/Dashboard/Dashboard";
import ExperimentChart from "./components/ExperimentChart/ExperimentChart";

export default function App() {
  const [sessionData, setSessionData] = useState([]);
  const [previousResults, setPreviousResults] = useState([]);
  const webSocket = useRef(null);

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

  useEffect(() => {
    if (sessionData.length === 0) {
      setPreviousResults([{
        AgentCount: 0,
        StepCount: 0
      }]);
    } else {
      setPreviousResults(sessionData[sessionData.length - 1]);
    }
  }, [sessionData]);

  webSocket.current.send(JSON.stringify({'Testing': 'Testing'}));

  return (
    <div>

      {/* Routes nest inside one another. Nested route paths build upon
            parent route paths, and nested route elements render inside
            parent route elements. See the note about <Outlet> below. */}
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Toolbar socket={webSocket} setter={setSessionData}/>} />
          <Route path="about" element={<About />} />
          {/* <Route path="dashboard" element={<Dashboard />} /> */}

          {/* Using path="*"" means "match anything", so this route
                acts like a catch-all for URLs that we don't have explicit
                routes for. */}
          <Route path="*" element={<NoMatch />} />
        </Route>
      </Routes>
    </div>
  );
}

// function Layout() {
//   return (
//     <div>
//       {/* A "layout route" is a good place to put markup you want to
//           share across all the pages on your site, like navigation. */}
//       <nav>
//         <ul>
//           <li>
//             <Link to="/">Home</Link>
//           </li>
//           <li>
//             <Link to="/about">About</Link>
//           </li>
//           <li>
//             <Link to="/dashboard">Dashboard</Link>
//           </li>
//           <li>
//             <Link to="/nothing-here">Nothing Here</Link>
//           </li>
//         </ul>
//       </nav>

//       <hr />

//       {/* An <Outlet> renders whatever child route is currently active,
//           so you can think about this <Outlet> as a placeholder for
//           the child routes we defined above. */}
//       <Outlet />
//     </div>
//   );
// }

function Home() {
  return (
    <div>
      <h2>Home</h2>
    </div>
  );
}

function About() {
  return (
    <div>
      <h2>About</h2>
      This is about stuff
    </div>
  );
}

// function Dashboard() {
//   return (
//     <div>
//       <h2>Dashboard</h2>
//     </div>
//   );
// }

function NoMatch() {
  return (
    <div>
      <h2>Nothing to see here!</h2>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}
