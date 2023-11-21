import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.selenium.utils import scroll_down, scroll_up


def run_reviews_scenario(testcase_instance, driver):
    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 1ой книги
    book_cards[0].click()

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[text()="Происхождение"]'))
    )
    assert title is not None
    time.sleep(1)

    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на отсутствие секции с созданием собственного отзыва

    with testcase_instance.assertRaises(TimeoutException):
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'CreateReviewCard'))
        )

    scroll_up(driver)

    time.sleep(0.5)

    # Проверка на существование кнопки Войти
    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Войти"]'))
    )
    assert login_button is not None
    time.sleep(0.5)
    login_button.click()

    inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    assert len(inputs) == 2

    email, password = inputs
    email.send_keys('pavel@gmail.com')
    time.sleep(0.5)
    password.send_keys('pavel')

    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Продолжить"]'))
    )
    assert continue_button is not None
    time.sleep(0.5)
    continue_button.click()

    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 1ой книги
    book_cards[0].click()

    time.sleep(0.5)

    scroll_down(driver)

    # Проверка существования секции с созданием собственного отзыва

    create_review_card = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'CreateReviewCard'))
    )
    assert create_review_card is not None

    # Проверка существования звезд рейтинга
    stars = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Star'))
    )
    assert stars is not None
    assert len(stars) == 5

    # Выбор 4 звезды
    ac = ActionChains(driver)
    ac.move_to_element(stars[1]).perform()

    # Проверка существования секции с текстом
    textarea = WebDriverWait(create_review_card, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'textarea'))
    )
    assert textarea is not None

    # Заполнение отзыва
    textarea.send_keys("Самая разочаровывающая книга про профессора Лэнгдона. 90% текста читаешь в ожидании ответов на вопросы: «Откуда мы? И куда идем?» Подобно неведомому джину, эта информация должна до основания разрушить устои мировых религий. А в конце, вместо джина появляется дарвиновская обезьяна с теорией эволюции. И мега-супер-мощный футуристический компьютер доказывает, что живая клетка образовалась в «первичном бульоне» исключительно благодаря законам физики. Лучше бы вообще не читал. Жалко потраченного времени.")

    # Проверка существования кнопки отправки отзыва
    send_review_button = WebDriverWait(create_review_card, 2).until(
        EC.presence_of_element_located((By.TAG_NAME, 'button'))
    )
    time.sleep(0.5)
    send_review_button.click()
    time.sleep(0.5)

    # Проверка существования 3 отзывов
    reviews = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'ReviewCard'))
    )
    assert reviews is not None
    assert len(reviews) == 3

    # Развернуть и скрыть отзыв
    expand_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ReviewCard")]/button[text()="Развернуть"]'))
    )
    assert expand_button is not None
    expand_button.click()
    time.sleep(0.5)

    hide_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "ReviewCard")]/button[text()="Свернуть"]'))
    )
    assert hide_button is not None
    hide_button.click()
    time.sleep(0.5)

    # Удаление отзыва
    delete_button = WebDriverWait(reviews[0], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'DeleteReviewButton'))
    )
    assert delete_button is not None
    time.sleep(0.5)
    delete_button.click()

    time.sleep(0.5)

    # Проверка существования 2 отзывов (1 удален)
    reviews = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'ReviewCard'))
    )
    assert reviews is not None
    assert len(reviews) == 2

    time.sleep(0.5)
