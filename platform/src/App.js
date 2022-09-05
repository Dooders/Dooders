import * as React from "react";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import ResponsiveSideBar from "./components/ResponsiveSideBar";
import ExperimentMain from "./components/ExperimentMain";

export default function App() {
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <ResponsiveAppBar />
      <ResponsiveSideBar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <br />
        <br />
        <br />
        <ExperimentMain />
      </Box>
    </Box>
  );
}
