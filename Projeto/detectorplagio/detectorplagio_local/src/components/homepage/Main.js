import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import {Redirect} from 'react-router-dom';

import {Alert} from "@mui/material";
import axios from "axios";

import Loading from "./Loading"

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
            percentage: 0,
        };

        this.calculate_similarity = this.calculate_similarity.bind(this);
        this.inputReference = React.createRef();

    }

    file_upload_action = () => {
        this.inputReference.current.click();
    }


    handle_click = async (event) => {
        event.preventDefault();
        this.clean_files()

        try {
            const newArr = event.target.files;

            await Promise.all(newArr).then((values) => {
                const data = new FormData()
                for (let i = 0; i < values.length; i++) {
                    let locale = "file"
                    data.append(locale, values[i])
                }
                return data
            }).then((values_data) => {
                let validate = this.validate_files(newArr)
                if (validate) {
                    this.calculate_similarity(values_data)
                }
            });
        } catch (e) {
            console.error(e);
        }
    };

    show_result_page(result) {
        this.setState({
            is_result_page_visible: true,
            result_calc: result
        });
    }

    validate_files(files) {
        let validate = true

        if (files.length <= 1) {
            validate = false
            this.setState({error_message_number_files: true})
        }

        for (let i = 0; i < files.length; i++) {
            if (i + 1 < files.length) {
                let file1 = files[i].name.split('.')
                let file2 = files[i + 1].name.split('.')
                let fileName1 = file1[0]
                let fileName2 = file2[0]
                let fileExt = file1[1]

                if (fileExt !== 'pdf' && fileExt !== 'txt' && fileExt !== 'docx') {
                    validate = false
                    this.setState({error_message_type_files: true});
                }

                if (fileName1 === fileName2) {
                    validate = false
                    this.setState({error_message_name_files: true});
                }
            }
        }

        return validate
    }

    clean_files() {
        // Local:
        let location = "http://127.0.0.1:8000/api/clean-files"
        // Remoto:
        // let location = "/api/clean-files"
        axios.post(location)
    }

    calculate_similarity(data) {

        this.setState({
            loading: true,
            error_message_number_files: false,
            error_message_type_files: false,
            error_message_name_files: false
        })
        // Local:
        let location = "http://127.0.0.1:8000/api/calculate-similarity"
        // Remoto:
        // let location = "/api/calculate-similarity"
        axios.post(location, data, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
            .then((response) => {
                    if (typeof response.data === 'object' && response.data !== null) {
                        this.setState({percentage: 100})

                        setTimeout(
                            () => this.show_result_page(response.data),
                            2000
                        );


                    } else {
                        this.setState({percentage: (response.data.toFixed(2) * 100)})

                        setTimeout(
                            () => this.calculate_similarity(data),
                            5000
                        );
                    }
                }
            )
            .catch(error => {
                console.log(error)
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
                                onChange={this.handle_click}/>


                            {this.state.loading ?
                                <div align={"center"}>
                                    <Loading percentage={this.state.percentage}/>
                                </div>
                                :
                                <Button
                                    onClick={this.file_upload_action}
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