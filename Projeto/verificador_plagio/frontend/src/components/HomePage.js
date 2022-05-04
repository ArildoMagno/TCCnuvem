import React, {Component} from "react";


import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect,
} from "react-router-dom";

export default class HomePage extends Component {
    constructor(props) {
        super(props);

        this.state = {
            files: true,
        };

    }

    handleRoomButtonPressed() {
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                files: this.state.files,
            }),
        };//Talvez isso na hora de redireiconar no meu site, eu ja jogo para o resultado
        fetch("/api/send-files", requestOptions)
            .then((response) => response.json());
    }

    renderHomePage() {
        return (
            <div>
                <h1>HOMEPAGE</h1>
                <h3>o plagio bblabla</h3>

                <Button
                    color="primary"
                    variant="contained"
                    onClick={this.handleRoomButtonPressed}>
                    Enviar Arquivos
                </Button>
            </div>
        );
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/" render={this.renderHomePage}></Route>
                </Switch>
            </Router>
        );
    }
}
