import { useParams } from 'react-router';

import './styles/global.scss'
import AppHeader from "./pages/AppHeader";
import {useSelector} from "react-redux";
import {NavModes} from "./store/nav/navSlice";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import BooksPage from "./pages/BooksPage";
import SingleBookPage from "./pages/SingleBookPage";


const _switchPart = (navMode) => {
    switch (navMode.mode) {
        case NavModes.LOGIN:
            return (
                <LoginPage />
            )
        case NavModes.REGISTER:
            return (
                <RegisterPage />
            )
        case NavModes.BOOKS:
            return (
                <>
                    <AppHeader />
                    <BooksPage />
                </>
            )
        case NavModes.BOOK:
            return (
                <>
                    <AppHeader />
                    <SingleBookPage />
                </>
            )
    }
}

function App() {

    const navMode = useSelector(state => state.nav)
    return (
        <div className="App">
            {_switchPart(navMode)}
        </div>
    );
}

export default App;
