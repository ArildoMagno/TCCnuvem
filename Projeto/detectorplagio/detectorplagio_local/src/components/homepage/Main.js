import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import {Redirect} from 'react-router-dom';

import {Alert, Menu, MenuItem} from "@mui/material";
import axios from "axios";

import Loading from "./Loading"
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@material-ui/core/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import AppBar from "@mui/material/AppBar";
import ExplainMethod from "../example/images/exemplo_main_img.png";


const style_image = {
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    width: "30%",
    paddingTop: "5vh",
    paddingBottom: "5vh",
}

export default class Main extends Component {
    constructor(props) {
        super(props);

        this.state = {
            // navbar:
            opacity_home: 1,
            opacity_example: 1,

            anchorEl: null,
            anchorOriginVertical: 'bottom',
            anchorOriginHorizontal: 'right',
            transformOriginVertical: 'top',
            transformOriginHorizontal: 'right',
            anchorReference: 'anchorEl',

            // main:
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
        // main:
        this.calculate_similarity = this.calculate_similarity.bind(this);
        this.inputReference = React.createRef();

        // navbar:
        this.handleMenu = this.handleMenu.bind(this);
        this.handleClose = this.handleClose.bind(this);

    }

    // navbar:
    mouse_hover_color_home() {

        this.setState({opacity_home: 0.7})

    }

    mouse_leave_color_home() {

        this.setState({opacity_home: 1})

    }

    mouse_hover_color_example() {

        this.setState({opacity_example: 0.7})

    }

    mouse_leave_color_example() {

        this.setState({opacity_example: 1})

    }

    handleMenu = event => {
        this.setState({anchorEl: event.currentTarget});
    };


    handleClose = () => {
        this.setState({anchorEl: null});
    };

    // main:

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
        const {anchorEl} = this.state;
        const open = Boolean(anchorEl);


        return (

            <main>
                {/*NAVBAR*/}
                <AppBar position="static" style={{background: '#75C3DC'}}>

                    <Toolbar disableGutters style={{paddingLeft: "5vw", paddingRight: "5vw"}}>
                        <Box sx={{flexGrow: 1, display: {xs: 'flex', md: 'none'}}}>
                            <IconButton
                                aria-owns={open ? 'menu-appbar' : null}
                                onClick={this.handleMenu}
                            >
                                <MenuIcon/>
                            </IconButton>

                            <Menu
                                id="menu-appbar"
                                anchorEl={anchorEl}
                                anchorOrigin={{vertical: "bottom", horizontal: "center"}}
                                transformOrigin={{vertical: "top", horizontal: "center"}}
                                open={open}
                                onClose={this.handleClose}
                            >

                                <MenuItem
                                    href="/"
                                    component="a"
                                    style={{width: "100%"}}
                                    onClick={this.handleClose}
                                > home </MenuItem> <br/>

                                <MenuItem
                                    href="/examples"
                                    component="a"
                                    style={{width: "100%"}}
                                    onClick={this.handleClose}
                                > exemplos </MenuItem> <br/>

                            </Menu>

                        </Box>


                        <Typography
                            variant="h6"
                            noWrap
                            component="a"
                            href="/"
                            onMouseEnter={() => this.mouse_hover_color_home()}
                            onMouseLeave={() => this.mouse_leave_color_home()}
                            sx={{
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'roboto',
                                color: 'white',
                                textDecoration: 'none',
                                opacity: this.state.opacity_home,

                            }}
                        >
                            Home
                        </Typography>


                        <Typography
                            variant="h6"
                            noWrap
                            component="a"
                            href="/examples"
                            onMouseEnter={() => this.mouse_hover_color_example()}
                            onMouseLeave={() => this.mouse_leave_color_example()}
                            sx={{
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'roboto',
                                color: 'white',
                                textDecoration: 'none',
                                opacity: this.state.opacity_example,
                                flexGrow: 1
                            }}
                        >
                            Exemplos
                        </Typography>


                        <Typography
                            variant="h6"
                            noWrap
                            component="a"
                            href="#/"
                            onClick={this.file_upload_action}
                            sx={{
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                color: 'white',
                                textDecoration: 'none',
                                padding: 1.5,
                                backgroundColor: "black",
                                borderRadius: '2vw'
                            }}
                        >
                            Analisar Arquivos
                        </Typography>


                    </Toolbar>

                </AppBar>

                <Container style={{paddingTop: "2vh"}}>
                    {this.state.error_message_number_files &&


                        <Alert severity="warning">Envie mais de um arquivo!</Alert>
                    }

                    {this.state.error_message_type_files &&
                        <Alert severity="error">Tipos de arquivos aceitos: txt, pdf, docx!</Alert>}
                    {this.state.error_message_name_files &&
                        <Alert severity="error">Envie arquivos com nomes distintos!</Alert>}

                </Container>


                {this.state.loading ?
                    <div align={"center"}>
                        <Loading percentage={this.state.percentage}/>
                    </div>
                    :


                    <Box
                        sx={{
                            bgcolor: 'background.paper',
                            pt: 8,
                            pb: 6,
                        }}
                    >


                        <Container>


                            <Typography
                                component="h1"
                                variant="h2"
                                align="center"
                                color="text.primary"
                                gutterBottom
                                sx={{

                                    fontFamily: 'chivo',

                                }}
                            >
                                Detector de Plágio
                            </Typography>


                            <Typography
                                variant="h6"
                                align="center"
                                color="text.secondary"
                                sx={{

                                    fontFamily: 'lato',

                                }}
                            >
                                Detectamos o plágio até mesmo quando há troca
                                das palavras por sinônimos.
                            </Typography>

                            <div>

                                <img src={ExplainMethod} alt="Ilustração do Processo" style={style_image}/>

                            </div>


                            <Typography
                                component="h4"
                                variant="h5"
                                align="center"
                                color="text.primary"
                                gutterBottom
                                sx={{

                                    fontFamily: 'chivo',

                                }}
                            >
                                Clique em <b>Analisar Arquivos</b> para enviar seus documentos.
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
                                    onChange={this.handle_click}/>

                            </Stack>


                        </Container>
                    </Box>
                }


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
