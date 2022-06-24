import React, {Component} from "react";


import {
    CircularProgressbar,
} from "react-circular-progressbar";
import "react-circular-progressbar/dist/styles.css";


export default class Loading extends Component {
    render() {

        return (
            <Example>
                <CircularProgressbar value={this.props.percentage} text={`${this.props.percentage}%`}/>
            </Example>

        );
    }
}

function Example(props) {
    return (
        <div>
            <div style={{width: "25%"}}>{props.children}</div>
            <p>{props.description}</p>
        </div>


    );
}
