import React from 'react';
import { Outlet } from "react-router-dom";
import Navbar from './components/Navbar/Navbar';

function Layout() {
    return (
        <div>
            {/* <Navbar/> */}
            <Outlet />
        </div>
    );
}

export default Layout;