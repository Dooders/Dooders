
// import React from 'react';
// import ReactDOM from 'react-dom';
// import './index.css';
// import App from './App';
// import reportWebVitals from './reportWebVitals';
// import {
//   BrowserRouter,
//   Routes,
//   Route
// } from "react-router-dom";
// import Authentication from './pages/Authentication/Authentication';
// import MachineLearning from './pages/MachineLearning/MachineLearning';
// import Hosting from './pages/Hosting/Hosting';
// import Functions from './pages/Functions/Functions';
// import Database from './pages/Database/Database';
// import Storage from './pages/Storage/Storage';

// ReactDOM.render(
//     <BrowserRouter>
//     <Routes>
//       <Route path="/" element={<App />}>
//         <Route path="authentication" element={<Authentication />} />
//         <Route path="database" element={<Database />} />
//         <Route path="functions" element={<Functions />} />
//         <Route path="hosting" element={<Hosting />} />
//         <Route path="machine-learning" element={<MachineLearning />} />
//         <Route path="storage" element={<Storage />} />
//       </Route>
//     </Routes>
//   </BrowserRouter>,
//   document.getElementById('root')
// );

// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();


import * as React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import "./index.css";
import App from "./App";
// import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(
  document.getElementById("root")
);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);