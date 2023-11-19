const {createSlice} = require("@reduxjs/toolkit");


export const NavModes = {
    BOOKS: 'BOOKS',
    BOOK: 'BOOK',
    GENRES: 'GENRES',
    AUTHORS: 'AUTHORS',
    COLLECTIONS: 'COLLECTIONS',
    LOGIN: 'LOGIN',
    REGISTER: 'REGISTER',
    CREATION: 'CREATION'

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