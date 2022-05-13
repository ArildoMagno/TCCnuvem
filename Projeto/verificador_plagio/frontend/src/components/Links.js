import React, {Component} from "react";
import FilesUpload from "./FilesUpload";
import ResultPage from "./ResultPage";
import HomePage from "./HomePage";
import DetailsResult from "./resultpage/DetailsResult";

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
                    <Route path="/details" component={DetailsResult}/>
                </Switch>
            </Router>
        );
    }
}
