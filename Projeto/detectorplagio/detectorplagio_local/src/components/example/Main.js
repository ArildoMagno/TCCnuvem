import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import FeaturedPost from "./FeaturedPost";
import Typography from '@mui/material/Typography';
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";


//Local Imgs
import DocumentImg from './images/document_img.png';
import ExplainMethod from './images/exemplo_main_img.png';
import {Component} from "react";
import axios from "axios";
import {Redirect} from "react-router-dom";
import LoadingInExamplePage from "./LoadingInExamplePage";


const example01 = [
    {
        title: 'Documento01',
        type: 'txt',
        description:
            'Que interessante este assunto, irei estudar mais sobre.' +
            'Você sabe de algum lugar onde posso encontrar mais informações?',
        image: DocumentImg,
    },
    {
        title: 'Documento02',
        type: 'txt',
        description:
            'Que curioso este conteúdo, irei aprender mais sobre. Você sabe de algum lugar para achar mais informações?',
        image: DocumentImg,
    }
];

const example02 = [
    {
        title: 'Documento01',
        type: 'txt',
        description:
            'O processo de procura de um emprego pode ser muito estressante, mas não precisa ser.' +
            'Comece com um currículo bem escrito que tenha palavras-chave apropriadas para sua ocupação. ' +
            'Em seguida, realize uma busca de emprego direcionada para cargos que atendam às suas necessidades.',
        image: DocumentImg,
    },
    {
        title: 'Documento02',
        type: 'pdf',
        description:
            'Procurar um emprego pode ser muito estressante, mas não precisa ser. Comece\n' +
            'escrevendo um bom currículo com palavras-chave apropriadas para sua ocupação. Em\n' +
            'segundo lugar, direcione sua busca de emprego para cargos que correspondam às suas\n' +
            'necessidades.',
        image: DocumentImg,

    },
    {
        title: 'Documento03',
        type: 'docx',
        description:
            'Segundo uma pesquisa realizada pelo linkedin, a maioria de seus usuários estão insatisfeitos com seus empregos, entretanto' +
            'procurar um emprego pode ser muito estressante, mas não precisa ser.' +
            'Comece escrevendo um bom currículo com palavras-chave apropriadas para sua ocupação.' +
            'Em segundo lugar, direcione sua busca de emprego para cargos que correspondam às suas necessidades.' +
            'O que pode levar a pessoas a desistir do seu objetivo.',
        image: DocumentImg,

    },
    {
        title: 'Documento04',
        type: 'txt',
        description:
            'A busca por um emprego pode ser muito estressante. Comece com um currículo bem escrito.' +
            'E realize uma procura de ocupação direcionada para cargos que atendam a sua carência.',
        image: DocumentImg,

    }
];


const theme = createTheme();


const style_image = {
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    width: "50%"
}

export default class Main extends Component {
    constructor(props) {
        super(props);

        this.state = {
            result_calc: Array,
            is_result_page_visible: false,
            loading_example01: false,
            loading_example02: false,
            percentage_example01: 0,
            percentage_example02: 0,
        };

        this.example01_calculate = this.example01_calculate.bind(this);
        this.example02_calculate = this.example02_calculate.bind(this);

    }

    example01_calculate() {
        this.setState({
            loading_example01: true
        })

        this.clean_files()
        // Local:
        let location = "http://127.0.0.1:8000/api/example01"
        // Remoto:
        // let location = "/api/example01"
        axios.get(location)
            .then((response) => {
                    setTimeout(
                        () => this.setState({percentage_example01: 100}),
                        3000
                    );

                    setTimeout(
                        () => this.show_result_page(response.data),
                        5000
                    );
                }
            )
            .catch(error => {
                console.log(error)
            })


    }


    example02_calculate() {
        this.setState({
            loading_example02: true
        })

        this.clean_files()
        // Local:
        let location = "http://127.0.0.1:8000/api/example02"
        // Remoto:
        // let location = "/api/example02"
        axios.get(location)
            .then((response) => {
                    setTimeout(
                        () => this.setState({percentage_example02: 50}),
                        3000
                    );
                    setTimeout(
                        () => this.setState({percentage_example02: 100}),
                        4000
                    );

                    setTimeout(
                        () => this.show_result_page(response.data),
                        5000
                    );
                }
            )
            .catch(error => {
                console.log(error)
            })


    }

    show_result_page(result) {
        console.log("aqui que quebrou?2")
        this.setState({
            is_result_page_visible: true,
            result_calc: result
        });
    }

    clean_files() {
        // Local:
        let location = "http://127.0.0.1:8000/api/clean-files"
        // Remoto:
        // let location = "/api/clean-files"
        axios.post(location)
    }

    render() {

        return (
            <ThemeProvider theme={theme}>
                <CssBaseline/>
                <Container maxWidth="lg">

                    <div style={{paddingTop: "10vh", paddingBottom: "5vh"}}>


                        <div style={{paddingBottom: "15vh"}}>
                            <Card sx={{display: 'flex'}}>
                                <CardContent sx={{flex: 1}}>

                                    <Grid container>


                                        <Typography variant="h6" align="center" color="text.secondary" paragraph
                                                    textAlign={"justify"} paddingLeft={"13vh"} paddingRight={"13vh"}>
                                            O sistema recebe arquivos nos formatos (pdf,txt,docx)
                                            e extrai o texto dos arquivos.
                                            Uma vez com o texto extraído é realizado a etapa de segmentação
                                            onde o texto é dividido em várias sentenças.
                                            Análises sobre a similaridade das sentenças são feitas,
                                            por fim, gerando a similaridade entre os arquivos.
                                        </Typography>


                                    </Grid>

                                    <div>

                                        <img src={ExplainMethod} alt="Ilustração do Processo" style={style_image}/>

                                    </div>


                                </CardContent>
                            </Card>
                        </div>


                        <Card sx={{display: 'flex'}}>
                            <CardContent sx={{flex: 1}}>


                                <Grid item xs={12} md={6} style={{paddingBottom: "10vh"}}>

                                    <Card sx={{display: 'flex'}}>
                                        <CardContent sx={{flex: 1}}>
                                            <div>
                                                <Typography variant="h4" gutterBottom>
                                                    Exemplo 01
                                                </Typography>

                                                <div style={{paddingTop: "2vh", paddingBottom: "2vh"}}>
                                                    <Grid container spacing={4}>
                                                        {example01.map((post, index) => (
                                                            <FeaturedPost key={index} post={post}/>
                                                        ))}
                                                    </Grid>
                                                </div>

                                                <div style={{textAlign: "center", paddingTop: "5vh"}}>
                                                    <Typography variant="h6" gutterBottom>
                                                        Para executar sua análise basta clicar em analisar
                                                    </Typography>


                                                    {this.state.loading_example01 ?
                                                        <div align={"center"}>
                                                            <LoadingInExamplePage
                                                                percentage={this.state.percentage_example01}/>
                                                        </div>
                                                        :
                                                        <Button
                                                            onClick={this.example01_calculate}
                                                            variant="contained"
                                                            disabled={this.state.loading_example02}
                                                            style={{
                                                                borderRadius: 15,
                                                                backgroundColor: "#92A8D1",
                                                                padding: "12px 26px",
                                                                fontSize: "12px",
                                                                fontFamily: "Helvetica"
                                                            }}
                                                        > Analisar </Button>
                                                    }


                                                </div>

                                            </div>

                                        </CardContent>
                                    </Card>

                                </Grid>


                                <Grid item xs={12} md={6}>

                                    <Card sx={{display: 'flex'}}>
                                        <CardContent sx={{flex: 1}}>


                                            <Typography variant="h4" gutterBottom>
                                                Exemplo 02
                                            </Typography>


                                            <div style={{paddingTop: "2vh", paddingBottom: "2vh"}}>
                                                <Grid container spacing={4}>
                                                    {example02.map((post, index) => (
                                                        <FeaturedPost key={index} post={post}/>
                                                    ))}
                                                </Grid>
                                            </div>


                                            <div style={{textAlign: "center", paddingTop: "5vh"}}>
                                                <Typography variant="h6" gutterBottom>
                                                    Para executar sua análise basta clicar em analisar
                                                </Typography>

                                                {this.state.loading_example02 ?
                                                    <div align={"center"}>
                                                        <LoadingInExamplePage
                                                            percentage={this.state.percentage_example02}/>
                                                    </div>
                                                    :
                                                    <Button
                                                        onClick={this.example02_calculate}
                                                        variant="contained"
                                                        disabled={this.state.loading_example01}
                                                        style={{
                                                            borderRadius: 15,
                                                            backgroundColor: "#92A8D1",
                                                            padding: "12px 26px",
                                                            fontSize: "12px",
                                                            fontFamily: "Helvetica"
                                                        }}
                                                    > Analisar </Button>
                                                }


                                            </div>

                                        </CardContent>
                                    </Card>

                                </Grid>

                            </CardContent>
                        </Card>


                    </div>


                </Container>

                {this.state.is_result_page_visible ?

                    <Redirect push to={{
                        pathname: '/result',
                        state: this.state.result_calc
                    }}
                    />

                    : null}

            </ThemeProvider>
        );
    }
}