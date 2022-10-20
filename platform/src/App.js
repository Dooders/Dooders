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
import cubejs from '@cubejs-client/core';
import { CubeProvider } from '@cubejs-client/react';

const cubejsApi = cubejs(
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2NjUzNTY2ODksImV4cCI6MTY2NTQ0MzA4OX0.pXe8XjU80esG34OmcisRenU_02z8RNv2TmFBu0KbIJg',
  { apiUrl: 'http://192.168.1.220:4000/cubejs-api/v1' }
);

export default function App() {

  return (
    
    <Router>
      <CubeProvider cubejsApi={cubejsApi}>
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
      </CubeProvider>
    </Router>
    
  );
}
