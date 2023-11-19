import {useEffect, useState} from "react";


const DropList = ({elements, displayProperty, useProperty, setCallback}) => {

    const [selected, setSelected] = useState()
    const [showList, setShowList] = useState(false)

    useEffect(() => {
        setCallback(selected[useProperty])
    }, [selected])

    return (
        <div className={'DropList'}>
            <div className={'Header'} onClick={() => setShowList(prev => !prev)}>{selected[displayProperty]}</div>
            <div className={'Body'}>
                {elements.map(el => <div
                    key={el[useProperty]}
                    className={'ListItem ' + (selected[useProperty] === el[useProperty] ? 'Active' : '')}
                    onClick={() => {
                        setShowList(false)
                    }}>{el[displayProperty]}</div>)}
            </div>
        </div>
    )
}


export default DropList