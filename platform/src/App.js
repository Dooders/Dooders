import * as React from "react";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import ResponsiveSideBar from "./components/ResponsiveSideBar";
import ExperimentMain from "./components/ExperimentMain";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Home } from "./Home";
import { About } from "./About";
import { NoMatch } from "./NoMatch";

export default function App() {
  return (
    <Router>
      <Box sx={{ display: "flex" }}>
        <CssBaseline />
        <ResponsiveAppBar />
        <ResponsiveSideBar />
        <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
          <br />
          <br />
          <br />
          <br />
          <Routes>
            <Route path="/" element={<ExperimentMain />} />
            <Route path="/about" element={<About />} />
            <Route path="/home" element={<Home />} />
            <Route element={<NoMatch />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
}
