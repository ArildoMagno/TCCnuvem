import React, {Component} from "react";
import FilesForm from "./FilesForm";

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
                    <Route exact path="/" component={FilesForm}/>
                </Switch>
            </Router>
        );
    }
}
