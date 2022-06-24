import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import {createTheme, ThemeProvider} from '@mui/material/styles';
import Main from "./homepage/Main";
import AppBarPageDefault from "./navbar/AppBarPageDefault";


const theme = createTheme();

export default function HomePage() {
    return (
        <div>
            <ThemeProvider theme={theme}>
                <CssBaseline/>
                <AppBarPageDefault/>
                <Main/>

            </ThemeProvider>
        </div>
    );
}