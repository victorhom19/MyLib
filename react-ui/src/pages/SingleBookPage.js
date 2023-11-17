import {useEffect, useRef, useState} from "react";
import {useSelector} from "react-redux";
import RatingIcon from "../assets/images/star.svg";
import EmptyRatingIcon from "../assets/images/star-empty.svg";
import UserIcon from "../assets/images/user-icon.svg"
import 'src/styles/SingleBookPage.scss'


const RatingBar = ({rating, setRating}) => {

    return (
        <div className={"RatingBar"}>
            {Array.from(new Array(5).keys()).map(x =>
                <div className={"Star"} onMouseEnter={() => {
                    setRating(x+1)
                }}>
                    <img src={rating >= x+1 ? RatingIcon : EmptyRatingIcon}/>
                </div>
            )}
        </div>
    )
}

const CreateReviewCard = ({book, setUpdateTrigger}) => {

    const auth = useSelector(state => state.auth)
    const [rating, setRating] = useState(3)
    const [text, setText] = useState("")

    const fetchCreateReview = async () => {
        await fetch(`${process.env.REACT_APP_WEB_APP_URI}/reviews/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                book_id: book.id,
                rating: rating,
                text: text
            })
        })
        setText("")
        setRating(3)
        setUpdateTrigger(prev => prev + 1)
    }


    return (
        <div className={"CreateReviewCard"}>
            <div className={"Header"}>
                <img src={UserIcon}/>
                <div className={"User"}>{auth.name}</div>
                <RatingBar rating={rating} setRating={setRating}/>
            </div>
            <div className={"Body"}>
                <textarea placeholder={"Текст отзыва..."} value={text} onChange={e => setText(e.target.value)}/>
            </div>
            <button onClick={fetchCreateReview}>Оставить отзыв</button>
        </div>
    )
}

const ReviewCard = ({review}) => {

    const [expanded, setExpanded] = useState(false)
    const [clamped, setClamped] = useState(false)

    const ref = useRef()

    useEffect(() => {
        setClamped(expanded || ref.current.scrollHeight > ref.current.clientHeight)
    }, [expanded])

    useEffect(() => {
        setClamped(expanded || ref.current.scrollHeight > ref.current.clientHeight)
    }, [])

    return (
        <div className={"ReviewCard"}>
            <div className={"Header"}>
                <img src={UserIcon}/>
                <div className={"UserDate"}>
                    <div className={"User"}>{review.user.name}</div>
                    <div className={"Date"}>{new Date(Date.parse(review.created)).toLocaleDateString("en-US")}</div>
                </div>
                <div className={"Rating"}>
                    <img src={RatingIcon}/>
                    {review.rating}
                </div>
            </div>
            <div className={"Body"}>
                <div ref={ref} className={"TextWrapper " + (expanded ? "Expanded" : null)}>{review.text}</div>
            </div>
            {clamped ? <button
                onClick={() => setExpanded(prev => !prev)}>{expanded ? "Свернуть" : "Развернуть"}</button> : null}
        </div>
    )
}


const ReviewsBlock = ({book, setUpdateTrigger}) => {

    const auth = useSelector(state => state.auth)

    return (
        <div className={"ReviewsBlock"}>
            <div className={"Header"}>Отзывы</div>
            <div className={"Body"}>
                {book.reviews.map(review => <ReviewCard review={review} />)}
                {auth.id ? <CreateReviewCard book={book} setUpdateTrigger={setUpdateTrigger}/> : null}
            </div>
        </div>
    )
}

const AnnotationBlock = ({text}) => {

    const [expanded, setExpanded] = useState(false)

    return (
        <div className={"AnnotationBlock"}>
            <div className={"Header"}>Аннотация</div>
            <div className={"Body"}>
                <div className={"TextWrapper " + (expanded ? "Expanded" : null)}>{text}</div>
            </div>
            <button onClick={() => setExpanded(prev => !prev)}>{expanded ? "Свернуть" : "Развернуть"}</button>
        </div>
    )
}

const SingleBookPage = () => {

    const [book, setBook] = useState()
    const navMode = useSelector(state => state.nav)
    const [updateTrigger, setUpdateTrigger] = useState(0)


    const fetchBook = (setCallback) => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/books/${navMode.id}`, {
            method: 'GET',
            credentials: 'include'
        })
        .then(res => res.json())
        .then(setCallback)
    }

    useEffect(() => {
        fetchBook(setBook)
    }, [updateTrigger])


    return (
        book ? <div className={"SingleBookPage"}>
            <div className={"Header"}>
                <div className={"Title"}>{book.title}</div>
                <div className={"AuthorYear"}>{book.author.name} – {book.year}</div>
                <div className={"Rating"}>
                    <img src={RatingIcon}/>
                    {book.rating}
                </div>
                <div className={"Image"}></div>
            </div>
            <AnnotationBlock text={book.annotation}/>
            <ReviewsBlock book={book} setUpdateTrigger={setUpdateTrigger}/>
        </div> : null
    )
}

export default SingleBookPage