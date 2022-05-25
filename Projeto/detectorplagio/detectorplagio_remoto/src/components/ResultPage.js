import React, {Component} from "react";
import BarGraph from "./resultpage/BarGraph";
import AppBarPageBackButton from "./homepage/AppBarPageBackButton";
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import {createTheme} from '@mui/material/styles';
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";


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
        const requestOptions = {
            method: "POST",
            responseType: 'blob',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(result),
        }

        // Local:
        // var location = "http://127.0.0.1:8000/api/generate-pdf"// Remoto:
        // Remoto:
        var location = "/api/generate-pdf"
        fetch(location, requestOptions)
            .then(response => response.blob())
            .then(blob => URL.createObjectURL(blob))
            .then(uril => {
                var link = document.createElement("a");
                link.href = uril;
                link.download = "relatorio.zip";
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            });
    }


    render() {
        return (
            <div>
                <CssBaseline/>
                <AppBarPageBackButton/>

                <Container sx={{py: 8}} maxWidth="md">

                    <Grid container spacing={4}>
                        {this.props.location.state.map((document, index) => (

                            <Grid item xs={12} sm={6} md={8} lg={8} key={index} justifyContent={"center"}
                                  style={{display: "flex", flexWrap: "wrap"}}>

                                <Grid item>
                                    <Typography variant="h6" color="text.secondary" paragraph>
                                        Arquivo: {document.name_file_source}
                                    </Typography>

                                    <BarGraph datafiles={document.relation_files}/>
                                </Grid>

                                <Grid item xs={12} sm={12} md={12} lg={12}></Grid>
                            </Grid>
                        ))}

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


