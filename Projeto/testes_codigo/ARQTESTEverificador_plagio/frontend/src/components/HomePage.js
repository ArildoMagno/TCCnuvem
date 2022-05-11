import * as React from 'react';


import CssBaseline from '@mui/material/CssBaseline';


import {createTheme, ThemeProvider} from '@mui/material/styles';
import AppBarPage from "./homepage/AppBarPage";
import Main from "./homepage/Main";
import Footer from "./homepage/Footer";


const theme = createTheme();

export default function HomePage() {
    return (
        <div>
            <ThemeProvider theme={theme}>
                <CssBaseline/>
                <AppBarPage/>
                <Main/>
                <Footer/>
            </ThemeProvider>
        </div>
    );
}
