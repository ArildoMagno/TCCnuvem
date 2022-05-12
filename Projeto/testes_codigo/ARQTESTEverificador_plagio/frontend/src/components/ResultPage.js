import React, {Component} from "react";
import BarGraph from "./resultpage/BarGraph";
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Grid from '@mui/material/Grid';

import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import {createTheme, ThemeProvider} from '@mui/material/styles';

const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];

const theme = createTheme();

export default class ResultPage extends Component {
    constructor(props) {
        super(props);

    }


    render() {
        return (
            <div>
                <h1>Result Page:</h1>

                <div>
                    {this.props.location.state.resultatual.map((documento, index) =>
                        <div key={index}>
                            <b>Nome Primeiro Arquivo:</b> {documento.name_file1} <br/>
                            <b>Nome Segundo Arquivo:</b> {documento.name_file2} <br/>

                            <h4>Sentenças:</h4>
                            {documento.similar_sets_log1.map((documento_inside, index_documento_inside) =>
                                <div key={index_documento_inside}>
                                    <b> Grau de semelhança entre Sentença Doc1 com Sentença
                                        Doc2</b>: {documento_inside.percentage_doc1_doc2} <br/>
                                    <b>Grau de semelhança entre Sentença Doc2 com Sentença
                                        Doc1: </b> {documento_inside.percentage_doc2_doc1} <br/>

                                    <b>Conteúdo Sentença Doc1: </b> {documento_inside.sentence_doc1} <br/>
                                    <b>Conteúdo Sentenca Doc2: </b> {documento_inside.sentence_doc2} <br/>
                                    <br/>
                                    <br/>
                                    <br/>
                                </div>
                            )}


                            <h3>Porcentagem Plagio Entre os Documentos:</h3> <h2> {documento.percent_plagiarism}</h2>
                            <br/>
                        </div>
                    )}
                </div>

                {/*IDEIA DE COMO EXIBIR OS RESULTADOS, PAG DETALHES FICA DEPOIS*/}
                {/*<Container sx={{py: 8}} maxWidth="md">*/}
                {/*    /!* End hero unit *!/*/}
                {/*    <Grid container spacing={4}>*/}
                {/*        {this.props.location.state.map((documento, index) => (*/}

                {/*            //xs (for phones) sm (for tablets) md (for small laptops)*/}
                {/*            <Grid item key={index} xs={12} sm={6} md={8}>*/}
                {/*                <h3>Doc1 porcentagem de chance de plagio com outros documentos:</h3>*/}
                {/*                <BarGraph/>*/}
                {/*                <button>Exibir Detalhes</button>*/}

                {/*            </Grid>*/}


                {/*        ))}*/}
                {/*    </Grid>*/}
                {/*</Container>*/}


            </div>
        );
    }
}


