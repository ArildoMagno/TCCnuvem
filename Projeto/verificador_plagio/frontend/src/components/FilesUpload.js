import React, {Component} from "react";
import {Redirect} from "react-router-dom"

export default class FilesUpload extends Component {
    constructor(props) {
        super(props);

        this.state = {
            file: true,
            result_calc: Array,
            isResultPageVisible: false,
        };


        this.calculateSimilarity = this.calculateSimilarity.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);

    }

    handleChange(event) {
        this.setState({file: event.target.files})
    }

    async handleSubmit(e) {
        e.preventDefault()
        this.calculateSimilarity();
    }

    showResultPage(result) {
        this.setState({
            isResultPageVisible: true,
            result_calc: result
        });
    }

    calculateSimilarity() {
        // Send Files:
        var input = document.querySelector('input[type="file"]')
        var data = new FormData()

        for (let i = 0; i < input.files.length; i++) {
            data.append('file', input.files[i])
        }

        const requestOptions = {
            method: "POST",
            redirect: "follow",
            body: data,
        }

        fetch("/api/calculate-similarity", requestOptions)
            .then(response => response.json())
            .then((response) => {
                console.log(response)
                this.showResultPage(response)
            })
            .catch(err => console.log(err))
    }


    render() {
        return (
            <div className="container">
                <div className="row">
                    <form onSubmit={this.handleSubmit}>
                        <input type="file" id="file" multiple name="file" onChange={this.handleChange}/>
                        <button type="submit" className="btn btn-info"> Calcula</button>
                    </form>
                </div>
                {this.state.isResultPageVisible ?
                    <Redirect to={{
                        pathname: '/result',
                        state: this.state.result_calc
                    }}
                    />
                    : null}
            </div>
        );
    }
}
