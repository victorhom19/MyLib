import {combineReducers, configureStore} from "@reduxjs/toolkit";
import {reducer as authReducer}  from 'src/store/auth/authSlice.js'
import {reducer as navReducer}  from 'src/store/nav/navSlice.js'


const reducers = combineReducers({
    auth: authReducer,
    nav: navReducer
})

export const store = configureStore({
    reducer: reducers,
    devTools: true
})