import time

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from config import DB_USER, DB_PASS, DB_HOST, DB_HOST_PORT, DB_NAME
from models.models import User, Book

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_HOST_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def clear_user(name='Лиза'):
    with Session(engine) as session:
        stmt = select(User).where(User.name == name)
        user = (session.execute(stmt)).scalars().first()
        if user:
            session.delete(user)
            session.commit()


def clear_book(title='Новая книга'):
    with Session(engine) as session:
        stmt = select(Book).where(Book.title == title)
        book = (session.execute(stmt)).scalars().first()
        if book:
            session.delete(book)
            session.commit()


def scroll_down(driver):
    SCROLL_PAUSE_TIME = 0.5

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def scroll_up(driver):
    SCROLL_PAUSE_TIME = 0.5

    time.sleep(SCROLL_PAUSE_TIME)
    driver.execute_script("scroll(0, 0);")
