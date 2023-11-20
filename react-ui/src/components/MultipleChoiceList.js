import {useEffect, useState} from "react";
import 'src/styles/MultipleChoiceList.scss'

const Element = ({elementObj, titleProperty, selectProperty, setSelected}) => {

    const [elementSelected, setElementSelected] = useState(false)

    return (
        <div className={"Element"}>
            {elementObj[titleProperty]}
            <button onClick={() => {
                if (elementSelected) {
                    setSelected(prev => prev.filter(el => el !== elementObj[selectProperty]))
                } else {
                    setSelected(prev => [...prev, elementObj[selectProperty]])
                }
                setElementSelected(prev => !prev)
            }}>{elementSelected ? <div className={"Marker"} /> : null}</button>
        </div>
    )
}

const MultipleChoiceList = (
    {id,
    title,
    getElementsCallback,
    hiddenLimit,
    titleProperty,
    selectProperty,
    setSelected}) => {

    const [elements, setElements] = useState([])
    const [expanded, setExpanded] = useState(false)

    useEffect(() => {
        getElementsCallback(setElements)
    }, [])


    return (
        <div className={"MultipleChoiceList"} id={id}>
            <h3>{title}</h3>
            {expanded
                ? elements.map(el => <Element elementObj={el} titleProperty={titleProperty}
                                              selectProperty={selectProperty} setSelected={setSelected} />)
                : elements.slice(0, hiddenLimit).map(el => <Element elementObj={el} titleProperty={titleProperty}
                                              selectProperty={selectProperty} setSelected={setSelected} />)
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

export default MultipleChoiceList