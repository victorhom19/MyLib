import {useEffect, useState} from "react";
import 'src/styles/CollectionsPage.scss'
import deleteIcon from 'src/assets/images/red-cross.svg'

const BookElement = ({book, collection, collections, setCollections, hideAllTrigger, setHideAllTrigger, isCreatedCollection}) => {

    const [showPopup, setShowPopup] = useState(false)

    useEffect(() => {
        if (!hideAllTrigger || hideAllTrigger !== book.id) {
            setShowPopup(false)
        }
    }, [hideAllTrigger])


    const fetchRemoveFromCollection = async () => {
        await fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections/${collection.id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: collection.title,
                book_ids: collection.books.map(b => b.id).filter(id => id !== book.id)
            })
        })
        setCollections(prev => prev.map(c => ({...c, books: c.books.filter(b => b.id !== book.id)})))

    }


    const fetchAddToCollection = async (collection) => {
        await fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections/${collection.id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: collection.title,
                book_ids: [...collection.books.map(b => b.id), book.id]
            })
        })
        setCollections(prev => prev.map(c => c.id === collection.id ? {...c, books: [...c.books, book]} : c))
    }

    return (
        <div className={'BookElement ' + (showPopup ? 'Active' : '')} onClick={() => {
            setHideAllTrigger(book.id)
            setShowPopup(prev => !prev)
        }}>
            <div className={'Header'}>{book.title}</div>
            {showPopup ?
                <div className={'Popup ' + (isCreatedCollection ? 'CreatedCollection' : null)}>
                    {!isCreatedCollection ? <>
                        {collection.title !== 'Буду читать' ? <button onClick={async () => {
                            const toCollection = collections.filter(c => c.title === 'Буду читать')[0]
                            await fetchRemoveFromCollection()
                            await fetchAddToCollection(toCollection)
                        }}>В "Буду читать"</button> : null}
                        {collection.title !== 'Буду читать' ? <div className={'Separator'}/> : null}
                        {collection.title !== 'Читаю' ? <button onClick={async () => {
                            const toCollection = collections.filter(c => c.title === 'Читаю')[0]
                            await fetchRemoveFromCollection()
                            await fetchAddToCollection(toCollection)
                        }}>В "Читаю"</button> : null}
                        {collection.title !== 'Читаю' ? <div className={'Separator'}/> : null}
                        {collection.title !== 'Прочитано' ? <button onClick={async () => {
                            const toCollection = collections.filter(c => c.title === 'Прочитано')[0]
                            await fetchRemoveFromCollection()
                            await fetchAddToCollection(toCollection)
                        }}>В "Прочитано"</button> : null}
                        {collection.title !== 'Прочитано' ? <div className={'Separator'}/> : null}
                    </> : null}
                    <button onClick={fetchRemoveFromCollection}>{"Удалить"}</button>
                </div>
                : null
            }
        </div>
    )
}


const CreatedCollection = ({collection, hideAllTrigger, setHideAllTrigger, createdCollections, setCreatedCollections}) => {

    const [title, setTitle] = useState(collection.title)
    const [editableTitle, setEditableTitle] = useState(collection.title)

    const fetchChangeCollectionTitle = async () => {

        await fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections/${collection.id}`, {
            method: 'PUT',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: editableTitle,
                book_ids: collection.books.map(b => b.id)
            })
        })
    }

    const fetchDeleteCollection = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections/${collection.id}`, {
            method: 'DELETE',
            credentials: 'include',
        })
        .then(res => res.json())
        .then(deleted => {
            setCreatedCollections(prev => prev.filter(c => c.id !== deleted.id))
        })
    }

    return (
        <div className={'Collection'}>
            <div className={'Header Created'}>
                <input  value={editableTitle}
                       onChange={e => setEditableTitle(e.target.value)}
                       onKeyPress={async e => {
                           if (e.key === 'Enter') {
                               await fetchChangeCollectionTitle()
                               setTitle(editableTitle)
                           }
                       }}
                       onBlur={e => {
                           setEditableTitle(title)
                       }}
                />
                <button className={'DeleteCollectionButton'} onClick={fetchDeleteCollection}><img src={deleteIcon} /></button>
            </div>

            <div className={'Body'}>
                {collection.books.map(book =>
                    <BookElement
                        key={book.id}
                        book={book}
                        collection={collection}
                        hideAllTrigger={hideAllTrigger}
                        setHideAllTrigger={setHideAllTrigger}
                        collections={createdCollections}
                        setCollections={setCreatedCollections}
                        isCreatedCollection={true}
                    />
                )}
            </div>
        </div>
    )
}

const CollectionsPage = () => {

    const [baseCollections, setBaseCollections] = useState([])
    const [createdCollections, setCreatedCollections] = useState([])
    const [hideAllTrigger, setHideAllTrigger] = useState(null)


    useEffect(() => {
        fetchCollections()
    }, [])

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

    const fetchCreateCollection = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/collections`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: 'Моя подборка'
            })
        })
        .then(res => res.json())
        .then(collection => {
            setCreatedCollections(prev => [...prev, collection])
        })
    }

    const collectionsPerPage = 3
    const [totalPages, setTotalPages] = useState(0)
    const [currentPage, setCurrentPage] = useState(0);

    useEffect(() => {

        setTotalPages(Math.ceil(createdCollections.length / collectionsPerPage))
        setCurrentPage(0)
    }, [createdCollections])

    return <div className={"CollectionsPage"}>
        <div className={"Header"}>Мои подборки</div>
        <div className={"BaseCollections"}>
            <div className={"Header"}>Базовые подборки</div>
            <div className={"Body"}>
                {baseCollections.map(collection => <div className={'Collection'}>
                    <div className={'Header'}>{collection.title}</div>
                    <div className={'Body'}>
                        {collection.books.map(book =>
                            <BookElement
                                key={book.id}
                                book={book}
                                collection={collection}
                                hideAllTrigger={hideAllTrigger}
                                setHideAllTrigger={setHideAllTrigger}
                                collections={baseCollections}
                                setCollections={setBaseCollections}
                                isCreatedCollection={false}
                            />
                        )}
                    </div>
                </div>)}
            </div>
        </div>
        <div className={"CreatedCollections"}>
            <div className={"Header"}>
                Созданные подборки
            </div>
            <button onClick={fetchCreateCollection}>Создать новую подборку +</button>
            <div className={"Body"}>
                {createdCollections.slice(currentPage * 3, (currentPage + 1) * 3).map(collection => <CreatedCollection
                    key={collection.id}
                    collection={collection}
                    hideAllTrigger={hideAllTrigger}
                    setHideAllTrigger={setHideAllTrigger}
                    createdCollections={createdCollections}
                    setCreatedCollections={setCreatedCollections}
                />)}
            </div>
            {createdCollections && createdCollections.length > 0 ?
                <div className={"Pagination"}>
                    <button className={"Control"} onClick={() => setCurrentPage(prev => {
                        if (prev > 0) return prev - 1
                        else return prev
                    })}>{"<"}</button>
                    {Array.from(Array(totalPages).keys()).map(k =>
                        <button className={"Page " + (currentPage === k ? "Active" : null)}
                            onClick={() => setCurrentPage(k)}
                        >{k+1}</button>
                    )}
                    <button className={"Control"} onClick={() => setCurrentPage(prev => {
                        if (prev + 1 < totalPages) return prev + 1
                        else return prev
                    })}>{">"}</button>
                </div> : null
            }

        </div>
    </div>
}

export default CollectionsPage