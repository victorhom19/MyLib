import {useDispatch} from "react-redux";
import {useMemo} from "react";
import bindActionCreators from "react-redux/es/utils/bindActionCreators";
import {actions as authActions} from 'src/store/auth/authSlice.js'
import {actions as navActions} from 'src/store/nav/navSlice.js'

const rootActions = {
    ...authActions,
    ...navActions
}

export const useActions = () => {
    const dispatch = useDispatch()

    return useMemo(() => bindActionCreators(rootActions, dispatch), [dispatch])
}