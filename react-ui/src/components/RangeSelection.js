import {useState} from "react";
import 'src/styles/RangeSelection.scss'

const RangeSelection = ({id, title, setFrom, setTo}) => {


    const [_from, _setFrom] = useState("")
    const [_to, _setTo] = useState("")

    return (
        <div className={"RangeSelection"} id={id}>
            <h3>{title}</h3>
            <div className={"RangeBody"}>
                <input value={_from} onChange={e => {
                    if (!isNaN(e.target.value)) {
                        setFrom(e.target.value)
                        _setFrom(e.target.value)
                    }
                }}/>
                –
                <input value={_to} onChange={e => {
                    if (!isNaN(e.target.value)) {
                        setTo(e.target.value)
                        _setTo(e.target.value)
                    }

                }}/>
            </div>
        </div>
    )
}

export default RangeSelection