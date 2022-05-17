import React, {Component} from "react";
import Toolbar from "@mui/material/Toolbar";
import AppBar from '@mui/material/AppBar';
import Button from "@mui/material/Button";
import {useHistory} from "react-router-dom";
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import Box from '@mui/material/Box';
import IconButton from "@material-ui/core/IconButton";

const AppBarPageBackButton = () => {


    const history = useHistory();

    return (
        <div>

            <AppBar position="relative" style={{background: '#92A8D1'}}>
                <Toolbar>



                    <IconButton onClick={() => history.goBack()}>
                        <ArrowBackIcon/>
                    </IconButton>


                </Toolbar>
            </AppBar>
        </div>

    );
}
export default AppBarPageBackButton;