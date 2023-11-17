import {useEffect, useState} from "react";


const CollectionsPage = () => {

    const [baseCollections, setBaseCollections] = useState([])
    const [createdCollections, setCreatedCollections] = useState([])


    useEffect(() => {
        console.log('Base colections')
    }, [baseCollections, createdCollections])

    const fetchCollections = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections`, {
            method: 'GET',
            credentials: 'include'
        })
        .then(res => res.json())
        .then(collections => {
            setBaseCollections(collections.filter(
                collection => ['Читаю', 'Буду читать', 'Прочитано'].includes(collection.title)))
            setCreatedCollections(collections.filter(
                collection => !['Читаю', 'Буду читать', 'Прочитано'].includes(collection.title)))
        })
    }

    return <div className={"CollectionsPage"}>
        <div className={"Header"}>Мои подборки</div>
        <div className={"BaseCollections"}>
            <div className={"Header"}>Базовые подборки</div>
            <div className={"Body"}></div>
        </div>
        <div className={"CreatedCollections"}>
            <div className={"Header"}>
                Базовые подборки
                <button>Создать новую подборку</button>
            </div>
            <div className={"Body"}></div>
        </div>
    </div>
}

export default CollectionsPage