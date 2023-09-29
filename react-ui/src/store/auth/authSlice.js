import {createSlice} from "@reduxjs/toolkit";


const initialState = {
    logged: false,
    id: null,
    username: null
}

export const authSlice = createSlice({
    name: 'auth',
    initialState: initialState,
    reducers: {
        signup: (state, action) => {
            const {id, username} = action.payload
            state.logged = true
            state.id = id
            state.username = username
            return state
        },
        login: (state, action) => {
            const {id, username} = action.payload
            state.logged = true
            state.id = id
            state.username = username
            return state
        },
        logout: (state, action) => {
            state.logged = false
            state.userId = null
            state.userName = null
            return state
        }
    }
})

export const {actions, reducer} = authSlice