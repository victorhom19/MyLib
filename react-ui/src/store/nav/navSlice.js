const {createSlice} = require("@reduxjs/toolkit");


export const NavModes = {
    BOOKS: 'BOOKS',
    BOOK: 'BOOK',
    GENRES: 'GENRES',
    AUTHORS: 'AUTHORS',
    COMPILATIONS: 'COMPILATIONS',
    LOGIN: 'LOGIN',
    REGISTER: 'REGISTER'

}

const navSlice = createSlice({
    name: 'nav',
    initialState: {
        mode: NavModes.BOOKS,
        id: null
    },
    reducers: {
        setNavMode: (state, action) => {
            state = action.payload
            return state
        }
    }
})

export const {actions, reducer} = navSlice