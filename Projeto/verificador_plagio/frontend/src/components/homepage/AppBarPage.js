import React, {Component} from "react";
import Toolbar from "@mui/material/Toolbar";
import FortIcon from '@mui/icons-material/Fort';
import Typography from "@mui/material/Typography";
import AppBar from '@mui/material/AppBar';



export default class AppBarPage extends Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <AppBar position="relative" style={{background: '#21b6ae'}}>
                <Toolbar>
                </Toolbar>
            </AppBar>
        );
    }
}
