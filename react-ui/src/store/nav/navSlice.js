const {createSlice} = require("@reduxjs/toolkit");


export const NavModes = {
    BOOKS: 'BOOKS',
    GENRES: 'GENRES',
    AUTHORS: 'AUTHORS',
    COMPILATIONS: 'COMPILATIONS'

}

const navSlice = createSlice({
    name: 'nav',
    initialState: NavModes.BOOKS,
    reducers: {
        setNavMode: (state, action) => {
            state = action.payload
            return state
        }
    }
})

export const {actions, reducer} = navSlice