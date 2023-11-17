import {useEffect, useState} from "react";
import 'src/styles/BooksPage.scss'
import MultipleChoiceList from "../components/MultipleChoiceList";
import RangeSelection from "../components/RangeSelection";
import RatingIcon from "src/assets/images/star.svg"
import ReviewIcon from "src/assets/images/reviews.svg"
import {useActions} from "../hooks/useActions";
import {NavModes} from "../store/nav/navSlice";


const FilterSection = ({setSelectedGenres, setSelectedAuthors, setYearFrom, setYearTo}) => {

    const fetchGenres = (setCallback) => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/genres/`, {
            method: 'GET',
            credentials: 'include'
        })
        .then(res => res.json())
        .then(setCallback)
    }

    const fetchAuthors = (setCallback) => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/authors/`, {
            method: 'GET',
            credentials: 'include'
        })
        .then(res => res.json())
        .then(setCallback)
    }

    return (
        <div className={"FilterSection"}>
            <MultipleChoiceList
                title={"Жанр"}
                getElementsCallback={fetchGenres}
                hiddenLimit={5}
                titleProperty={'name'}
                selectProperty={'id'}
                setSelected={setSelectedGenres}
            />
            <RangeSelection
                title={"Год"}
                setFrom={setYearFrom}
                setTo={setYearTo}
            />
            <MultipleChoiceList
                title={"Автор"}
                getElementsCallback={fetchAuthors}
                hiddenLimit={5}
                titleProperty={'name'}
                selectProperty={'id'}
                setSelected={setSelectedAuthors}
            />
        </div>
    )
}


const SideBar = ({setFilters}) => {

    const [selectedGenres, setSelectedGenres] = useState([])
    const [selectedAuthors, setSelectedAuthors] = useState([])
    const [yearFrom, setYearFrom] = useState("")
    const [yearTo, setYearTo] = useState("")

    useEffect(() => {
        const filterState = {
            search_query: null,
            genre_ids: selectedGenres.length > 0 ? selectedGenres : null,
            year_from: yearFrom.length > 0 ? parseInt(yearFrom) : null,
            year_to: yearTo.length > 0 ? parseInt(yearTo) : null,
            author_ids: selectedAuthors.length > 0 ? selectedAuthors : null,
        }
        setFilters(filterState)
    }, [selectedGenres, selectedAuthors, yearFrom, yearTo])

    return (
        <div className={"SideBar"}>
            <FilterSection
                setSelectedGenres={setSelectedGenres}
                setSelectedAuthors={setSelectedAuthors}
                setYearFrom={setYearFrom}
                setYearTo={setYearTo}
            />
        </div>
    )
}

const BookCard = ({book}) => {

    const genresLimit = 3
    const hiddenGenresCount = book.genres.length - genresLimit
    const {setNavMode} = useActions()

    return (
        <div className={"BookCard"} onClick={() => {
            setNavMode({mode: NavModes.BOOK, id: book.id})
        }}>
            <div className={"Header"}>
                <div className={"Rating"}>
                    <img src={RatingIcon}/>
                    {book.rating}
                </div>
                <div className={"Reviews"}>
                    <img src={ReviewIcon}/>
                    {book.reviews_count}
                </div>
            </div>
            <div className={"Image"}>dsfsdf</div>
            <div className={"About"}>
                <div className={"Title"}>{book.title}</div>
                <div className={"AuthorYear"}>{book.author.name} – {book.year}</div>
            </div>
            <div className={"Genres"}>
                {book.genres.slice(0, genresLimit).map(genre => <div className={"Genre"}>{genre.name}</div>)}
                {hiddenGenresCount > 0 ? <div className={"Genre"}>+{hiddenGenresCount}</div> : null}
            </div>
        </div>
    )
}

const BooksList = ({books, booksPerRow, rowsPerPage}) => {

    const booksPerPage = rowsPerPage * booksPerRow
    const totalPages = Math.ceil(books.length / booksPerPage)

    const [currentPage, setCurrentPage] = useState(0);

    useEffect(() => {
        setCurrentPage(0)
    }, [books])


    return (
        <div className={"BooksList"}>
            <div className={"BookCardContainer"}>
                {books.slice(currentPage * booksPerPage, (currentPage + 1) * booksPerPage).map(book => <BookCard book={book} />)}
            </div>
            <div className={"Pagination"}>
                <button className={"Control"} onClick={() => setCurrentPage(prev => {
                    if (prev > 0) return prev - 1
                    else return prev
                })}>{"<"}</button>
                {Array.from(Array(totalPages).keys()).map(k =>
                    <button className={"Page " + (currentPage === k ? "Active" : null)}>{k+1}</button>
                )}
                <button className={"Control"} onClick={() => setCurrentPage(prev => {
                    if (prev + 1 < totalPages) return prev + 1
                    else return prev
                })}>{">"}</button>
            </div>
        </div>
    )
}

const BooksPage = () => {

    const [filters, setFilters] = useState({
        search_query: null,
        genre_ids: null,
        year_from: null,
        year_to: null,
        author_ids: null,
    })

    const [books, setBooks] = useState([])

    const fetchBooks = (setCallback) => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/books/list`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        })
        .then(res => res.json())
        .then(setCallback)
    }

    useEffect(() => {
        let timer = setTimeout(() => {
            fetchBooks(setBooks)
        }, 200)
        return () => {
            clearTimeout(timer)
        }
    }, [filters])


    return (
        <div className={"BooksPage"}>
            <SideBar setFilters={setFilters}/>
            <BooksList books={books} booksPerRow={5} rowsPerPage={2}/>
        </div>
    )

}

export default BooksPage