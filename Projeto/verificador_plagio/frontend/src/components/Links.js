import React, {Component} from "react";
import FilesUpload from "./FilesUpload";
import ResultPage from "./ResultPage";
import HomePage from "./HomePage";
import ResultPageGrafico from "./resultpage/BarGraph";

import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";

export default class Links extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/" component={FilesUpload}/>
                    <Route path="/result" component={ResultPage}/>
                    <Route path="/homepage" component={HomePage}/>
                    <Route path="/grafico" component={ResultPageGrafico}/>
                </Switch>
            </Router>
        );
    }
}
