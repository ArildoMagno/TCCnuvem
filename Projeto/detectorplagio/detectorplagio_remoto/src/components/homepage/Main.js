import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import {Redirect} from 'react-router-dom';
import LoadingSpin from "react-loading-spin";
import {Alert} from "@mui/material";
import axios from "axios";

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
        this.inputReference = React.createRef();

    }

    fileUploadAction = () => {
        this.inputReference.current.click();
    }


    handleClick = async (event) => {
        event.preventDefault();
        this.cleanFiles()

        try {
            const newArr = event.target.files;

            await Promise.all(newArr).then((values) => {
                console.log("values:", values);
                const data = new FormData()
                for (let i = 0; i < values.length; i++) {
                    let locale = "file"
                    data.append(locale, values[i])
                }
                return data
            }).then((values_data) => {
                let validate = this.validate_files(newArr)
                if (validate) {
                    this.calculateSimilarity(values_data)
                }
            });
        } catch (e) {
            console.error(e);
        }
    };

    showResultPage(result) {
        this.setState({
            is_result_page_visible: true,
            result_calc: result
        });
    }

    validate_files(files) {
        let validate = true

        if (files.length <= 1) {
            validate = false
        }

        return validate
    }

    cleanFiles() {
        // Local:
        // var location = "http://127.0.0.1:8000/api/clean-files"
        // Remoto:
        var location = "/api/clean-files"
        axios.post(location)
    }


    calculateSimilarity(data) {
        console.log("calcula similaridade")


        this.setState({
            loading: true,
            error_message_number_files: false,
            error_message_type_files: false,
            error_message_name_files: false
        })
        // Local:
        // var location = "http://127.0.0.1:8000/api/calculate-similarity"
        // Remoto:
        var location = "/api/calculate-similarity"
        axios.post(location, data, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then((response) => {
                    console.log("response:", response.data)
                    if (response.data !== "processing") {
                        this.setState({
                            loading: false,
                        });
                        this.showResultPage(response.data)
                    } else {
                        setTimeout(
                            () => this.calculateSimilarity(data),
                            20000
                        );

                    }

                }
            )
            .catch(error => {
                console.log(error)            // check if any error
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
                                onChange={this.handleClick}/>

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
