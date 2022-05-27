import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import {Redirect} from 'react-router-dom';
import LoadingSpin from "react-loading-spin";
import {Alert} from "@mui/material";

export default class Main extends Component {
    constructor(props) {
        super(props);


        this.state = {
            file: true,
            result_calc: Array,
            isResultPageVisible: false,
            fileUploadState: "",
            loading: false,
            errorMessage: false,
        };

        this.calculateSimilarity = this.calculateSimilarity.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.inputReference = React.createRef();

    }

    fileUploadAction = () => {
        this.inputReference.current.click();
    }

    fileUploadInputChange = (e) => {
        if (e.target.files.length <= 1) {
            this.setState({errorMessage: true});
            return
        }

        this.setState({fileUploadState: e.target.files, errorMessage: false, loading: true}, () => {
            this.handleSubmit(e)
        });
    }

    async handleSubmit(event) {
        event.preventDefault()
        this.calculateSimilarity();
    }

    showResultPage(result) {
        this.setState({
            isResultPageVisible: true,
            result_calc: result
        });
    }

    calculateSimilarity() {
        var data = new FormData()
        for (let i = 0; i < this.state.fileUploadState.length; i++) {
            data.append('file', this.state.fileUploadState[i])
        }

        const requestOptions = {
            method: "POST",
            redirect: "follow",
            body: data,
        }

        // Local:
        // var location = "http://127.0.0.1:8000/api/calculate-similarity"
        // Remoto:
        var location = "/api/calculate-similarity"
        fetch(location, requestOptions)
            .then(response => response.json())
            .then((response) => {
                this.setState({
                    loading: false,
                });
                this.showResultPage(response)
            })
            .catch(error => {
                console.log(error)
                this.setState({
                    loading: false,
                });
            })
    }

    render() {


        return (

            <main>
                {/* Hero unit */}
                <Box
                    sx={{
                        bgcolor: 'background.paper',
                        pt: 8,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h1"
                            variant="h2"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Detector de Plágio
                        </Typography>


                        <Typography variant="h5" align="center" color="text.secondary" paragraph>
                            Detectamos o plágio até mesmo quando há troca
                            das palavras por sinônimos.
                        </Typography>
                        <br/>
                        <Typography variant="h6" align="center" color="text.secondary" paragraph>
                            Envie os arquivos que deseja analisar.
                        </Typography>

                        {this.state.errorMessage && <Alert severity="error">Envie mais de um arquivo!</Alert>}

                        <Stack
                            sx={{pt: 4}}
                            direction="row"
                            spacing={1}
                            justifyContent="center"
                        >


                            <input
                                type="file"
                                id="file"
                                name="file"
                                multiple
                                hidden
                                ref={this.inputReference}
                                onChange={this.fileUploadInputChange}/>

                            {this.state.loading ? <LoadingSpin primaryColor="#92A8D1"/>
                                :
                                <Button
                                    onClick={this.fileUploadAction}
                                    variant="contained"
                                    style={{
                                        borderRadius: 35,
                                        backgroundColor: "#92A8D1",
                                        padding: "18px 36px",
                                        fontSize: "18px"
                                    }}
                                > Enviar Arquivos </Button>
                            }


                        </Stack>


                    </Container>
                </Box>


                {this.state.isResultPageVisible ?
                    <Redirect push to={{
                        pathname: '/result',
                        state: this.state.result_calc
                    }}
                    />
                    : null}

            </main>

        );
    }
}
