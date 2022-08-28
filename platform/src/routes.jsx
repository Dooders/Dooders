import React from "react";
import {BrowserRouter, Route, Switch} from "react-router-dom";
import Authentication from "./components/Authentication";
import Home from "./components/Home";

function Routes() {
    return (
        <BrowserRouter>
            <Switch>
                <Route path="/" exact component={Home}/>
                <Route path="/settings" component={Authentication}/>

                {/* <Route component={NotFound}/> */}
            </Switch>
        </BrowserRouter>
    )
}

export default Routes;