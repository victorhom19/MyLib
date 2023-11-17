import {createSlice} from "@reduxjs/toolkit";

const Roles = {
    USER: "User",
    MODERATOR: "Moderator",
    ADMIN: "Admin"
}

const initialState = {
    logged: false,
    id: null,
    name: null,
    email: null,
    role: null
}

export const authSlice = createSlice({
    name: 'auth',
    initialState: initialState,
    reducers: {
        login: (state, action) => {
            const {id, name, email, role} = action.payload
            state.logged = true
            state.id = id
            state.name = name
            state.email = email
            state.role = role
            return state
        },
        logout: (state, action) => {
            state.logged = false
            state.id = null
            state.name = null
            state.email = null
            state.email = null
            return state
        }
    }
})

export const {actions, reducer} = authSlice