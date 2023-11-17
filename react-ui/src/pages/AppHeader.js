import React, {useEffect, useState} from 'react'
import '../styles/AppHeader.scss'
import {useSelector} from "react-redux";
import {useActions} from "../hooks/useActions";
import {NavModes} from "../store/nav/navSlice";

const UserPopup = () => {

    const {logout} = useActions();

    const fetchLogout = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        })
        .then(() => logout())
    }

    return (
        <div className={"UserPopup"}>
            <button>Подборки книг</button>
            <button onClick={fetchLogout}>Выйти из аккаунта</button>
        </div>
    )
}

const AuthButtons = () => {
    const {logged, name} = useSelector(state => state.auth)
    const {setNavMode, login} = useActions();
    const [showPopup, setShowPopup] = useState(false)

    const fetchStatus = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/status`, {
            method: 'GET',
            credentials: 'include'
        })
        .then(res => res.json())
        .then(userInfo => {
            if (Object.keys(userInfo).length > 1) login(userInfo)
        })
    }

    useEffect(() => {
        fetchStatus()
    }, [])

    return (
        logged
            ? <>
                <button id={"user-button"} onClick={() => setShowPopup(!showPopup)}>{name}</button>
                {showPopup ? <UserPopup/> : null}
            </>
            : <>
                <button
                    id={"login-button"}
                    onClick={() => setNavMode({mode: NavModes.LOGIN, id: null})}>Войти
                </button>
                <button
                    id={"register-button"}
                    onClick={() => setNavMode({mode: NavModes.REGISTER, id: null})}>Регистрация
                </button>
            </>
    )
}

const AppHeader = () => {

    const navMode = useSelector(state => state.nav)
    const {setNavMode} = useActions()

    return (
        <div className={"AppHeader"}>
            <button
                className={navMode.mode === NavModes.BOOKS ? "Active" : null}
                onClick={() => setNavMode({mode: NavModes.BOOKS, id: null})}>Книги</button>
            <button
                className={navMode.mode === NavModes.AUTHORS ? "Active" : null}
                onClick={() => setNavMode({mode: NavModes.AUTHORS, id: null})}>Авторы</button>
            <button
                className={navMode.mode === NavModes.GENRES ? "Active" : null}
                onClick={() => setNavMode({mode: NavModes.GENRES, id: null})}>Жанры</button>
            <input placeholder={"Поиск книг"}/><></>
            <AuthButtons />
        </div>
    )

}

export default AppHeader