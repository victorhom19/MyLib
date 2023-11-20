import logo from 'src/assets/images/mylib-logo.svg'

import 'src/styles/RegisterPage.scss'
import {useActions} from "../hooks/useActions";
import {NavModes} from "../store/nav/navSlice";
import React, {useEffect, useState} from 'react'

const RegisterPage = () => {

    const {setNavMode, login} = useActions();

    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(false)
    const [success, setSuccess] = useState(false)

    const fetchRegister = async () => {
        return await fetch(`${process.env.REACT_APP_WEB_APP_URI}/auth/register`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(
                {
                      email: email,
                      password: password,
                      is_active: true,
                      is_superuser: false,
                      is_verified: false,
                      name: name,
                      role_id: 0
                }
            )
        })
    }


    const handleRegister = async () => {
        setLoading(true)
        setError(false)
        setSuccess(false)

        const res = await fetchRegister()

        switch (res.status) {
            case 201:
                setSuccess(true)
                setNavMode({mode: NavModes.BOOKS, id: null})
                break;
            case 400:
                setLoading(false)
                setError(true)
                break;
        }

    }

    useEffect(() => {
        if (error) {
            setEmail('')
        }
    }, [error])

    return (
        <div className={"RegisterPage"}>
            <h3>Вход</h3>
            <img src={logo} />
            <input
                placeholder={"Имя"}
                value={name}
                onChange={(e) => {setName(e.target.value)}}
            />
            <input
                className={error ? "Error" : null}
                placeholder={"Электронная почта"}
                value={email}
                onChange={(e) => {setEmail(e.target.value)}}
            />
            <input
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
                <button id={'continue-btn'} onClick={handleRegister}>Зарегистрироваться</button>
            </div>
        </div>
    )
}

export default RegisterPage