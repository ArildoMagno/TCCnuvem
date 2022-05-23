import React, {Component} from "react";
import Typography from "@mui/material/Typography";
import CssBaseline from "@mui/material/CssBaseline";
import AppBarPageBackButton from "../homepage/AppBarPageBackButton";
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';

export default class DetailsResult extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div>
                <CssBaseline/>
                <AppBarPageBackButton/>


                <Container sx={{py: 8}} maxWidth="md">

                    <Typography variant="h2" align="center" color="text.secondary" paragraph>
                        <b>Detalhes</b>
                    </Typography>

                    {/* End hero unit */}
                    <Grid container spacing={4}>
                        {this.props.location.state.sentences.map((document, index) => (
                            <div key={index}>

                                <br/> <br/><br/>
                                <Typography variant="h5" color="text.secondary" paragraph>
                                    <b>Similaridade das sentenças em relação aos
                                        documentos {this.props.location.state.document_name} e {document.name_file_dest} :</b>
                                </Typography>


                                {document.similar_set_dest_source.map((document_inside, index_inside) => (
                                    <div key={index_inside}>

                                        <Typography variant="h6" color="text.secondary" paragraph>
                                            Sentença {index_inside}:
                                        </Typography>

                                        <Typography variant="h7" color="text.secondary" paragraph>
                                            <b> Documento {document.name_file_dest}:</b> {document_inside.sentence_doc1}
                                            <br/>
                                            <b>Documento {this.props.location.state.document_name}:</b> {document_inside.sentence_doc2}
                                        </Typography>


                                    </div>
                                ))}


                            </div>
                        ))}
                    </Grid>
                </Container>
            </div>
        );
    }
}

