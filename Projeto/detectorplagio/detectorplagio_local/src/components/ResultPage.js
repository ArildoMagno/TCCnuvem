import React, {Component} from "react";
import AppBarPageDefault from "./navbar/AppBarPageDefault";
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import {createTheme} from '@mui/material/styles';
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import axios from "axios";
import Graph from "./resultpage/Graph";


createTheme();


export default class ResultPage extends Component {
    constructor(props) {
        super(props);


        this.state = {
            result_sentences: Array,
            document_name: "",
            is_details_page_visible: false,
        };
        this.on_button_click = this.on_button_click.bind(this);
        this.generate_pdf = this.generate_pdf.bind(this);
        this.handle_submit = this.handle_submit.bind(this);
    }


    on_button_click(result, name) {
        this.setState({
            result_sentences: result,
            document_name: name,
            is_details_page_visible: true,
        });
    }

    async handle_submit() {
        this.generate_pdf(this.props.location.state);
    }

    generate_pdf(result) {

        // Local:
        let location = "http://127.0.0.1:8000/api/generate-pdf"// Remoto:
        // Remoto:
        // let location = "/api/generate-pdf"
        axios({
            url: location, //your url
            method: 'POST',
            responseType: 'blob',// important
            data: result,
        }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'relatorio.zip'); //or any other extension
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        });
    }


    render() {
        return (
            <div>
                <CssBaseline/>
                <AppBarPageDefault/>

                <Container sx={{py: 8}} maxWidth="md">

                    <Grid container spacing={4}>

                        <Graph datafiles={this.props.location.state}/>


                        <Grid item xs={12} sm={12} md={12} lg={12}></Grid>
                        <Grid item xs={12} sm={12} md={12} lg={12}></Grid>


                        <Button
                            variant="contained"
                            style={{
                                borderRadius: 35,
                                backgroundColor: "#92A8D1",
                                padding: "18px 36px",
                                fontSize: "22px",
                                margin: "0 auto",
                                fontFamily: "Helvetica"
                            }}

                            onClick={() => this.handle_submit()}
                        >
                            Gerar Relatorio
                        </Button>

                    </Grid>
                </Container>
            </div>

        )
            ;
    }
}


