import React, {Component} from "react";
import {render} from "react-dom";
import Links from "./Links";

export default class App extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Links/>
        );
    }
}

const appDiv = document.getElementById("app");
render(<App/>, appDiv);
