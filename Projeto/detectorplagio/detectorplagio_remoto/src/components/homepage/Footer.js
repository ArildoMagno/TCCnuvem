import React, {Component} from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";


function Copyright() {
    return (
        <Typography variant="body2" color="text.secondary" align="center">
            {'Copyright © '}
            <Link color="inherit" href="https://mui.com/">
               https://github.com/ArildoMagno
            </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}


export default class Footer extends Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (


            <Box sx={{bgcolor: 'background.paper', p: 10}} component="footer">

                <Typography
                    variant="subtitle1"
                    align="center"
                    color="text.secondary"
                    component="p"
                >
                    Todos direitos reservados
                </Typography>
                <Copyright/>
            </Box>


        );
    }
}
