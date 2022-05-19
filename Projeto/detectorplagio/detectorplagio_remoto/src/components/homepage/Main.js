import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import {Redirect} from 'react-router-dom';
import LoadingSpin from "react-loading-spin";

export default class Main extends Component {
    constructor(props) {
        super(props);


        this.state = {
            file: true,
            result_calc: Array,
            isResultPageVisible: false,
            fileUploadState: "",
            loading: false
        };

        this.calculateSimilarity = this.calculateSimilarity.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.inputReference = React.createRef();

    }

    fileUploadAction = () => {
        this.inputReference.current.click();
    }

    fileUploadInputChange = (e) => {
        this.setState({fileUploadState: e.target.files, loading: true}, () => {
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
            console.log("FileUploadState posi", i, "con:", this.state.fileUploadState[i])
            data.append('file', this.state.fileUploadState[i])
        }

        const requestOptions = {
            method: "POST",
            redirect: "follow",
            body: data,
        }
        // CALL LOCAL
        fetch("http://127.0.0.1:8000/api/calculate-similarity", requestOptions)
            .then(response => response.json())
            .then((response) => {
                this.setState({
                    loading: false,
                });
                this.showResultPage(response)
            })
            .catch(err => {
                console.log(err)
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
                            Verificador de Plágio
                        </Typography>


                        <Typography variant="h5" align="center" color="text.secondary" paragraph>
                            Detectamos o plágio até mesmo quando há troca
                            das palavras por sinônimos.
                        </Typography>
                        <br/>
                        <Typography variant="h6" align="center" color="text.secondary" paragraph>
                            Envie os arquivos que deseja analisar.
                        </Typography>

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

                    <Redirect to={{
                        pathname: '/result',
                        state: this.state.result_calc
                    }}
                    />
                    : null}

            </main>

        );
    }
}
