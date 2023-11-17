import logo from 'src/assets/images/mylib-logo.svg'

import 'src/styles/LoginPage.scss'
import {useActions} from "../hooks/useActions";
import {NavModes} from "../store/nav/navSlice";
import {useState} from "react";

const LoginPage = () => {

    const {setNavMode, login} = useActions();

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)

    const fetchLogin = async () => {
        return await fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/login`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${username}&password=${password}`
        })
    }

    const fetchStatus = async () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/status`, {
                method: 'GET',
                credentials: 'include'
            })
            .then(res => res.json())
            .then(login)
    }

    const handleLogin = async () => {
        setLoading(true)
        setError(false)
        setSuccess(false)


        const res = await fetchLogin()

        switch (res.status) {
            case 204:
                await fetchStatus()
                setSuccess(true)
                setNavMode({mode: NavModes.BOOKS, id: null})
                break;
            case 400:
                setLoading(false)
                setError(true)
                break;
        }

    }

    return (
        <div className={"LoginPage"}>
            <h3>Вход</h3>
            <img src={logo} />
            <input
                className={error ? "Error" : null}
                placeholder={"Электронная почта"}
                value={username}
                onChange={(e) => {setUsername(e.target.value)}}
            />
            <input
                className={error ? "Error" : null}
                placeholder={"Пароль"}
                type={'password'}
                value={password}
                onChange={(e) => {setPassword(e.target.value)}}
            />
            <div className={"ButtonBlock"}>
                <button
                    id={'back-btn'}
                    onClick={() => setNavMode({mode: NavModes.BOOKS, id: null})}
                >Назад</button>
                <button id={'continue-btn'} onClick={handleLogin}>Продолжить</button>
            </div>
        </div>
    )
}

export default LoginPage