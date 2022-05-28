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
            is_result_page_visible: false,
            file_upload_state: "",
            loading: false,
            error_message_number_files: false,
            error_message_type_files: false,
            error_message_name_files: false,
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
            this.setState({error_message_number_files: true});
            return
        }

        for (let i = 0; i < e.target.files.length; i++) {
            if (i + 1 < e.target.files.length) {
                var file1 = e.target.files[i].name.split('.')
                var file2 = e.target.files[i + 1].name.split('.')
                var fileName1 = file1[0]
                var fileName2 = file2[0]
                var fileExt = file1[1]

                //Not Accept Types
                if (fileExt !== 'pdf' && fileExt !== 'txt' && fileExt !== 'docx') {
                    this.setState({error_message_type_files: true});
                    return
                }

                //Same Name
                if (fileName1 === fileName2) {
                    this.setState({error_message_name_files: true});
                    return
                }
            }
        }

        this.setState({
            file_upload_state: e.target.files, error_message_number_files: false,
            error_message_type_files: false, error_message_name_files: false, loading: true
        }, () => {
            this.handleSubmit(e)
        });
    }

    async handleSubmit(event) {
        event.preventDefault()
        this.calculateSimilarity();
    }

    showResultPage(result) {
        this.setState({
            is_result_page_visible: true,
            result_calc: result
        });
    }

    calculateSimilarity() {
        var data = new FormData()
        for (let i = 0; i < this.state.file_upload_state.length; i++) {
            data.append('file', this.state.file_upload_state[i])
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


                        {this.state.error_message_number_files &&
                            <Alert severity="error">Envie mais de um arquivo!</Alert>}
                        {this.state.error_message_type_files &&
                            <Alert severity="error">Tipos de arquivos aceitos: txt, pdf, docx!</Alert>}
                        {this.state.error_message_name_files &&
                            <Alert severity="error">Envie arquivos com nomes distintos!</Alert>}

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


                {this.state.is_result_page_visible ?
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
