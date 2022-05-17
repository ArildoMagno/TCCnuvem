import React, {Component} from "react";
import Grid from '@mui/material/Grid';

import Container from '@mui/material/Container';
import {createTheme} from '@mui/material/styles';
import BarGraph from "./resultpage/BarGraph";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import {Redirect} from "react-router-dom";
import DetailsResult from "./resultpage/DetailsResult";
import CssBaseline from "@mui/material/CssBaseline";
import AppBarPageBackButton from "./homepage/AppBarPageBackButton";

createTheme();

export default class ResultPage extends Component {
    constructor(props) {
        super(props);


        this.state = {
            result_sentences: Array,
            document_name: "",
            isDetailsPageVisible: false,
        };
        this._onButtonClick = this._onButtonClick.bind(this);

    }


    _onButtonClick(result, name) {
        this.setState({
            result_sentences: result,
            document_name: name,
            isDetailsPageVisible: true,
        });
    }


    render() {
        return (
            <div>
                <CssBaseline/>
                <AppBarPageBackButton/>

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
                                        backgroundColor: "#92A8D1",
                                        padding: "8px 22px",
                                        fontSize: "8px",
                                        margin: "0 auto"
                                    }}
                                    onClick={() => this._onButtonClick(document.relation_files, document.name_file_source)}
                                >

                                    Ver Detalhes
                                </Button>


                            </Grid>


                        ))}
                    </Grid>

                    {this.state.isDetailsPageVisible ?
                        <Redirect to={{
                            pathname: '/details',
                            state: {
                                sentences: this.state.result_sentences,
                                document_name: this.state.document_name
                            }
                        }}
                        />
                        : null}


                </Container>
            </div>

        );
    }
}


