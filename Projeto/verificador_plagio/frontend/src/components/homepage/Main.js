import React, {Component} from "react";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import SendIcon from '@mui/icons-material/Send';

const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];

export default class Main extends Component {
    constructor(props) {
        super(props);
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
                            <Button
                                variant="contained"
                                style={{
                                    borderRadius: 35,
                                    backgroundColor: "#21b6ae",
                                    padding: "18px 36px",
                                    fontSize: "18px"
                                }}
                            >

                                Enviar Arquivos
                            </Button>

                        </Stack>


                    </Container>
                </Box>


            </main>

        );
    }
}
