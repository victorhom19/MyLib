import {useEffect, useState} from "react";
import 'src/styles/SingleChoiceList.scss'

const Element = ({elementObj, titleProperty, selectProperty, selected, setSelected}) => {

    return (
        <div className={"Element"}>
            {elementObj[titleProperty]}
            <button onClick={() => {
                if (selected && selected === elementObj[selectProperty]) {
                    setSelected(null)
                } else {
                    setSelected(elementObj[selectProperty])
                }
            }}>{selected && selected === elementObj[selectProperty] ? <div className={"Marker"} /> : null}</button>
        </div>
    )
}

const SingleChoiceList = (
    {title,
    getElementsCallback,
    hiddenLimit,
    titleProperty,
    selectProperty,
    selected,
    setSelected}) => {

    const [elements, setElements] = useState([])
    const [expanded, setExpanded] = useState(false)

    useEffect(() => {
        getElementsCallback(setElements)
    }, [])


    return (
        <div className={"SingleChoiceList"}>
            <h3>{title}</h3>
            {expanded
                ? elements.map(el => <Element elementObj={el} titleProperty={titleProperty}
                                              selectProperty={selectProperty} setSelected={setSelected}
                                              selected={selected}/>)
                : elements.slice(0, hiddenLimit).map(el => <Element elementObj={el} titleProperty={titleProperty}
                                              selectProperty={selectProperty} setSelected={setSelected}
                                              selected={selected}/>)
            }
            {
                hiddenLimit < elements.length
                    ? <button onClick={() => setExpanded(prev => !prev)}>
                        {expanded ? "Скрыть" : "Показать все"}
                    </button> : null
            }
        </div>
    )
}

export default SingleChoiceList