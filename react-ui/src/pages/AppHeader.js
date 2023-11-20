import React, {useEffect, useState} from 'react'
import '../styles/AppHeader.scss'
import {useSelector} from "react-redux";
import {useActions} from "../hooks/useActions";
import {NavModes} from "../store/nav/navSlice";

const UserPopup = () => {

    const {setNavMode, logout} = useActions();

    const fetchLogout = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/logout`, {
            method: 'POST',
            credentials: 'include'
        })
        .then(() => logout())
    }

    return (
        <div className={"UserPopup"}>
            <button onClick={() => {
                setNavMode({id: null, mode: NavModes.COLLECTIONS})

            }}>Подборки книг</button>
            <button onClick={fetchLogout}>Выйти из аккаунта</button>
        </div>
    )
}

const AuthButtons = () => {
    const {logged, name} = useSelector(state => state.auth)
    const {setNavMode, login} = useActions();
    const [showPopup, setShowPopup] = useState(false)
    const navMode = useSelector(state => state.nav)

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

    useEffect(() => {
        setShowPopup(false)
    }, [navMode])

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

const SearchPopup = ({searchBooks, setSearch}) => {

    const {logged} = useSelector(state => state.auth)
    const {setNavMode} = useActions()

    return (
        <div className={'SearchPopup ' + (logged ? '' : 'Shifted')}>
            {searchBooks.map(b => <button key={b.id} className={'Book'} onClick={() => {
                setNavMode({mode: NavModes.BOOK, id: b.id})
                setSearch("")
            }}>
                {b.title} – {b.author.name} – {b.year}
            </button>)}
        </div>
    )
}

const AppHeader = () => {

    const navMode = useSelector(state => state.nav)
    const {setNavMode} = useActions()
    const [searchBooks, setSearchBooks] = useState([])
    const [search, setSearch] = useState("")
    const {logged, role} = useSelector(state => state.auth)

    const fetchBooks = (setCallback) => {
        if (search.length > 0) {
            fetch(`${process.env.REACT_APP_WEB_APP_URI}/books/list`, {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    search_query: search,
                    genre_ids: null,
                    year_from: null,
                    year_to: null,
                    author_ids: null,
                })
            })
            .then(res => res.json())
            .then(setCallback)
        } else {
            setCallback([])
        }

    }

    useEffect(() => {
        let timer = setTimeout(() => {
            fetchBooks(setSearchBooks)
        }, 500)
        return () => {
            clearTimeout(timer)
        }
    }, [search])

    return (
        <div className={"AppHeader"}>
            <button
                className={navMode.mode === NavModes.BOOKS ? "Active" : null}
                onClick={() => setNavMode({mode: NavModes.BOOKS, id: null})}>Книги</button>
            {logged && role.name === "ADMIN" ? <button
                className={navMode.mode === NavModes.CREATION ? "Active" : null}
                onClick={() => setNavMode({mode: NavModes.CREATION, id: null})}>Создание сущностей</button> : null}
            {/*<button*/}
            {/*    className={navMode.mode === NavModes.AUTHORS ? "Active" : null}*/}
            {/*    onClick={() => setNavMode({mode: NavModes.AUTHORS, id: null})}>Авторы</button>*/}
            {/*<button*/}
            {/*    className={navMode.mode === NavModes.GENRES ? "Active" : null}*/}
            {/*    onClick={() => setNavMode({mode: NavModes.GENRES, id: null})}>Жанры</button>*/}
            <input placeholder={"Поиск книг"}
                   value={search}
                   onChange={e => setSearch(e.target.value)}
                   onBlur={(e) => {
                       if (!e.relatedTarget || !e.relatedTarget.classList.contains("Book")) setSearch("")
                   }}/>
            {search.length > 0 ? <SearchPopup searchBooks={searchBooks} setSearch={setSearch}/> : null}
            <AuthButtons />
        </div>
    )

}

export default AppHeader