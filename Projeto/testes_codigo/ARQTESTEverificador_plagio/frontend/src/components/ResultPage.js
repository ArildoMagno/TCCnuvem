import React, {Component} from "react";
import Grid from '@mui/material/Grid';

import Container from '@mui/material/Container';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import BarGraph from "./resultpage/BarGraph";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";

const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];

const theme = createTheme();

export default class ResultPage extends Component {
    constructor(props) {
        super(props);

    }

    helloWorld() {
        console.log("HelloWorld")
    }

    render() {
        return (

            <Container sx={{py: 8}} maxWidth="md">
                {/* End hero unit */}
                <Grid container spacing={4}>
                    {this.props.location.state.map((document, index) => (

                        //xs (for phones) sm (for tablets) md (for small laptops)
                        <Grid item xs={12} sm={6} md={8} lg={5} key={index} justifyContent={"center"}
                              style={{display: "flex", flexWrap: "wrap"}}>

                            <Grid item>
                                <Typography variant="h6" color="text.secondary" paragraph>
                                    Arquivo: {document.name_file_source}
                                </Typography>

                                <BarGraph datafiles={document.relation_files}/>
                            </Grid>


                            <Grid item xs={12} sm={12} md={12} lg={12}></Grid>


                            <Button
                                variant="contained"
                                style={{
                                    borderRadius: 8,
                                    backgroundColor: "#21b6ae",
                                    padding: "8px 22px",
                                    fontSize: "8px",
                                    margin: "0 auto"
                                }}
                                onClick={this.helloWorld}
                            >

                                Ver Detalhes
                            </Button>


                        </Grid>


                    ))}
                </Grid>
            </Container>


        );
    }
}


