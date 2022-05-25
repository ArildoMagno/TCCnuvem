import React, {Component} from "react";
import ResultPage from "./components/ResultPage";
import HomePage from "./components/HomePage";
import history from "./history_locale";

import {
    Router,
    Switch,
    Route,
} from "react-router-dom";

export default class Links extends Component {
    render() {
        return (
            <Router history={history}>
                <Switch>
                    <Route exact path="/" component={HomePage}/>
                    <Route path="/result" component={ResultPage}/>
                </Switch>
            </Router>
        );
    }
}
