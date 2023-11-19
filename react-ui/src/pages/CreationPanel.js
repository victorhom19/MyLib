import 'src/styles/CreationPanel.scss'
import SingleChoiceList from "../components/SingleChoiceList";
import MultipleChoiceList from "../components/MultipleChoiceList";

const {useState} = require("react");


const CreationMode = {
    BOOKS: 0,
    AUTHORS: 1,
    GENRES: 2
}

const annotationPlaceholder = 'Роберт Лэнгдон прибывает в музей Гуггенхайма в Бильбао по приглашению друга и бывшего студента Эдмонда Кирша. Миллиардер и компьютерный гуру, он известен своими удивительными открытиями и предсказаниями. И этим вечером Кирш собирается "перевернуть все современные научные представления о мире", дав ответ на два главных вопроса, волнующих человечество на протяжении всей истории:\n' +
    'Откуда мы?\n' +
    'Что нас ждет?\n' +
    'Однако прежде чем Эдмонд успевает сделать заявление, роскошный прием превращается в хаос. Лэнгдону и директору музея, красавице Амбре Видаль, чудом удается бежать.\n' +
    'Теперь их путь лежит в Барселону, где Кирш оставил для своего учителя закодированный ключ к тайне, способной потрясти сами основы представлений человечества о себе. Тайне, которая была веками похоронена во тьме забвения. Тайне, которой, возможно, лучше бы никогда не увидеть света, - по крайней мере, так считают те, кто преследует Лэнгдона и Видаль и готов на все, чтобы помешать им раскрыть истину.\n' +
    '\n' +
    'Об авторе\n' +
    'Дэн Браун - известнейший американский писатель, названный одним из 100 самых влиятельных людей мира по версии журнала "Time". Его книги переведены на 56 языков, а их суммарный тираж составил более 200 миллионов экземпляров.\n' +
    '\n' +
    'Мировую славу Дэну Брауну принесла серия романов о профессоре-криптологе Роберте Лэнгдоне, лучшем в мире специалисте по разгадке кодов, шифров и символов. "Код да Винчи", "Ангелы и демоны", "Инферно" - все эти книги стали бестселлерами №1, а также легли в основу одноименных фильмов, главную роль в которых исполнил неподражаемый Том Хэнкс.\n' +
    'Подробнее: https://www.labirint.ru/books/622401/'

const CreateGenreTemplate = ({setMessage}) => {

    const [genreName, setGenreName] = useState('')

    const fetchCreateGenre = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/genres/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: genreName
            })
        })
        .then(res => res.json())
        .then(genre => setMessage(`Создан жанр "${genre.name}"`))
    }

    return (
        <div className={'CreateGenreTemplate'}>
            <div className={'Header'}>Создать новый жанр</div>
            <div className={'Body'}>
                <div className={'Field'}>
                    <div className={'Label'}>Название жанра: </div>
                    <input placeholder={'Научная фантастика'}
                           value={genreName}
                           onChange={e => setGenreName(e.target.value)}
                    />
                </div>
            </div>
            <button onClick={fetchCreateGenre}>Создать</button>
        </div>
    )
}


const CreateAuthorTemplate = ({setMessage}) => {

    const [authorName, setAuthorName] = useState('')
    const [aboutAuthor, setAboutAuthor] = useState('')

    const fetchCreateAuthor = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/authors/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: authorName,
                about: aboutAuthor
            })
        })
        .then(res => res.json())
        .then(author => setMessage(`Создан автор "${author.name}"`))
    }

    return (
        <div className={'CreateAuthorTemplate'}>
            <div className={'Header'}>Создать нового автора</div>
            <div className={'Body'}>
                <div className={'Field'}>
                    <div className={'Label'}>Имя автора: </div>
                    <input placeholder={'Дэн Браун'}
                           value={authorName}
                           onChange={e => setAuthorName(e.target.value)}
                    />
                </div>
                <div className={'FieldV'}>
                    <div className={'Label'}>Информация об авторе: </div>
                    <textarea placeholder={'Об авторе'}
                           value={aboutAuthor}
                           onChange={e => setAboutAuthor(e.target.value)}
                    />
                </div>
            </div>
            <button onClick={fetchCreateAuthor}>Создать</button>
        </div>
    )
}


const CreateBookTemplate = ({setMessage}) => {

    const [title, setTitle] = useState('')
    const [authorId, setAuthorId] = useState('')
    const [genreIds, setGenreIds] = useState('')
    const [year, setYear] = useState('')
    const [annotation, setAnnotation] = useState('')

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

    const fetchCreateBook = () => {
        fetch(`${process.env.REACT_APP_WEB_APP_URI}/books/`, {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title,
                author_id: authorId,
                genre_ids: genreIds,
                year: year,
                annotation: annotation
            })
        })
        .then(res => res.json())
        .then(book => setMessage(`Создана книга "${book.title}"`))
    }

    return (
        <div className={'CreateBookTemplate'}>
            <div className={'Header'}>Создать новую книгу</div>
            <div className={'Body'}>
                <div className={'Field'}>
                    <div className={'Label'}>Название книги: </div>
                    <input placeholder={'Происхождение'}
                           value={title}
                           onChange={e => setTitle(e.target.value)}
                    />
                </div>
                <div className={'Separator'} />
                <SingleChoiceList
                    title={"Автор"}
                    getElementsCallback={fetchAuthors}
                    hiddenLimit={5}
                    titleProperty={'name'}
                    selectProperty={'id'}
                    selected={authorId}
                    setSelected={setAuthorId}
                />
                <div className={'Separator'} />
                <MultipleChoiceList
                    title={"Жанр"}
                    getElementsCallback={fetchGenres}
                    hiddenLimit={5}
                    titleProperty={'name'}
                    selectProperty={'id'}
                    setSelected={setGenreIds}
                />
                <div className={'Separator'} />
                <div className={'Field'}>
                    <div className={'Label'}>Год издания: </div>
                    <input placeholder={'2017'}
                           value={year}
                           onChange={e => setYear(e.target.value)}
                    />
                </div>
                <div className={'Separator'} />
                <div className={'FieldV'}>
                    <div className={'Label'}>Аннотация: </div>
                    <textarea placeholder={annotationPlaceholder}
                           value={annotation}
                           onChange={e => setAnnotation(e.target.value)}
                    />
                </div>
            </div>
            <button onClick={fetchCreateBook}>Создать</button>
        </div>
    )
}


const CreationPanel = () => {

    const [message, setMessage] = useState(null)
    const [mode, setMode] = useState(CreationMode.BOOKS)

    return (
        <div className={'CreationPanel '}>
            <div className={'Header'}>
                <button
                    className={mode === CreationMode.BOOKS ? 'Active' : ''}
                    onClick={() => setMode(CreationMode.BOOKS)}>
                    {"Создание книг"}
                </button>
                <button
                    className={mode === CreationMode.AUTHORS ? 'Active' : ''}
                    onClick={() => setMode(CreationMode.AUTHORS)}>
                    {"Создание авторов"}
                </button>
                <button
                    className={mode === CreationMode.GENRES ? 'Active' : ''}
                    onClick={() => setMode(CreationMode.GENRES)}>
                    {"Создание жанров"}
                </button>
            </div>
            <div className={'Body'}>
                {mode === CreationMode.BOOKS ? <CreateBookTemplate setMessage={setMessage} /> : null}
                {mode === CreationMode.AUTHORS ? <CreateAuthorTemplate setMessage={setMessage} /> : null}
                {mode === CreationMode.GENRES ? <CreateGenreTemplate setMessage={setMessage} /> : null}
            </div>
            {message ? <div className={'DisplayMessage'}>{message}</div> : null}
        </div>
    )
}


export default CreationPanel