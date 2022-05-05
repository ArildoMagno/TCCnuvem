import React, {Component} from "react";
import FilesUpload from "./FilesUpload";
import ResultPage from "./ResultPage";

import {
    BrowserRouter as Router,
    Switch,
    Route,
} from "react-router-dom";

export default class HomePage extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/" component={FilesUpload}/>
                    <Route path="/result" component={ResultPage}/>
                </Switch>
            </Router>
        );
    }
}
