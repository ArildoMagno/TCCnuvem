import React, {Component} from "react";
import Toolbar from "@mui/material/Toolbar";
import AppBar from '@mui/material/AppBar';
import Typography from "@mui/material/Typography";

export default class AppBarPageDefault extends Component {

    constructor(props) {
        super(props);

        this.state = {
            opacity_home: 0.7,
            opacity_example: 0.7,

        };

    }


    mouse_hover_color_home() {

        this.setState({opacity_home: 1})

    }

    mouse_leave_color_home() {

        this.setState({opacity_home: 0.7})

    }

    mouse_hover_color_example() {

        this.setState({opacity_example: 1})

    }

    mouse_leave_color_example() {

        this.setState({opacity_example: 0.7})

    }

    render() {
        return (
            <div>
                <AppBar position="relative" style={{background: '#92A8D1'}}>
                    <Toolbar>

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
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: '#FFFFF0',
                                textDecoration: 'none',
                                opacity: this.state.opacity_home
                            }}
                        >
                            HOME
                        </Typography>


                        <Typography
                            variant="h6"
                            noWrap
                            component="a"
                            href="/example"
                            onMouseEnter={() => this.mouse_hover_color_example()}
                            onMouseLeave={() => this.mouse_leave_color_example()}
                            sx={{
                                mr: 2,
                                display: {xs: 'none', md: 'flex'},
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: '#FFFFF0',
                                textDecoration: 'none',
                                opacity: this.state.opacity_example
                            }}
                        >
                            EXEMPLOS
                        </Typography>

                    </Toolbar>
                </AppBar>
            </div>

        );
    }
}
