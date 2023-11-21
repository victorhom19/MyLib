import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.selenium.utils import scroll_down, scroll_up


def run_roles_scenario(testcase_instance, driver):
    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 2ой книги
    book_cards[1].click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на отсутствие возможности удалять комментарии (нет ни одной кнопки)
    with testcase_instance.assertRaises(TimeoutException):
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'DeleteReviewButton'))
        )

    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Вход за пользователя Pavel (без особых прав)
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

    # Переход на страницу 2ой книги
    book_cards[1].click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на существование кнопки удаления собственного комментария
    delete_review_buttons = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'DeleteReviewButton'))
    )
    assert delete_review_buttons is not None
    assert len(delete_review_buttons) == 1

    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Выход из аккаунта
    user_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-button'))
    )
    assert user_button is not None
    time.sleep(0.5)
    user_button.click()

    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Выйти из аккаунта"]'))
    )
    time.sleep(0.5)
    logout_button.click()
    time.sleep(0.5)

    # Вход за пользователя Moderator (с правами на удаление комментариев)
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
    email.send_keys('moderator@gmail.com')
    time.sleep(0.5)
    password.send_keys('moderator')

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

    # Переход на страницу 2ой книги
    book_cards[1].click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на существование кнопки удаления любого комментария
    delete_review_buttons = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'DeleteReviewButton'))
    )
    assert delete_review_buttons is not None
    assert len(delete_review_buttons) == 2

    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Выход из аккаунта
    user_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'user-button'))
    )
    assert user_button is not None
    time.sleep(0.5)
    user_button.click()

    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Выйти из аккаунта"]'))
    )
    time.sleep(0.5)
    logout_button.click()
    time.sleep(0.5)

    # Вход за пользователя Admin (с правами на удаление комментариев)
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
    email.send_keys('admin@gmail.com')
    time.sleep(0.5)
    password.send_keys('admin')

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

    # Переход на страницу 2ой книги
    book_cards[1].click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на существование кнопки удаления любого комментария
    delete_review_buttons = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'DeleteReviewButton'))
    )
    assert delete_review_buttons is not None
    assert len(delete_review_buttons) == 2

    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Проверка существования кнопки создания новых сущностей у администратора
    create_new_entities = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Создание сущностей"]'))
    )
    assert create_new_entities is not None
    create_new_entities.click()
    time.sleep(0.5)

    # Проверка сущестовования кнопок переключения режимов создания (книги, авторы, жанры)
    book_creation_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Создание книг"]'))
    )
    assert book_creation_button is not None

    author_creation_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Создание авторов"]'))
    )
    assert author_creation_button is not None

    genre_creation_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Создание жанров"]'))
    )
    assert genre_creation_button is not None

    time.sleep(0.5)
    author_creation_button.click()
    time.sleep(0.5)
    genre_creation_button.click()
    time.sleep(0.5)
    book_creation_button.click()

    # Выбор управляющих элементов для создания новой книги
    book_title_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[1]/input'))
    )
    assert book_title_input is not None

    dan_brown_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[3]/div[1]/button'))
    )
    assert dan_brown_button is not None

    detective_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[5]/div[1]/button'))
    )
    assert detective_button is not None

    mystic_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[5]/div[4]/button'))
    )
    assert mystic_button is not None

    year_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[7]/input'))
    )
    assert year_input is not None

    annotation_textarea = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div[9]/textarea'))
    )
    assert annotation_textarea is not None

    book_title_input.send_keys("Новая книга")
    time.sleep(0.5)
    dan_brown_button.click()
    time.sleep(0.5)
    detective_button.click()
    time.sleep(0.5)
    mystic_button.click()
    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)
    year_input.send_keys('2023')
    time.sleep(0.5)
    annotation_textarea.send_keys("Аннотация к новой книге")

    # Создание книги
    create_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div/button'))
    )
    assert create_button is not None
    time.sleep(0.5)
    create_button.click()
    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Возврат на главную страницу
    books_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Книги"]'))
    )
    books_button.click()
    time.sleep(0.5)

    # Переход ко второй странице с книгами
    # Проверка существования элементов пагинации
    pagination_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Pagination'))
    )
    assert pagination_box is not None

    pagination_arrows = WebDriverWait(pagination_box, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Control'))
    )
    assert pagination_arrows is not None
    assert len(pagination_arrows) == 2
    pagination_left_arrow, pagination_right_arrow = pagination_arrows

    pages = WebDriverWait(pagination_box, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Page'))
    )
    assert pages is not None
    assert len(pagination_arrows) == 2

    pagination_right_arrow.click()
    time.sleep(0.5)

    # Проверка на существование карточек с книгами (должно быть 3)
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 3

    # Переход к созданной книге
    book_cards[2].click()
    time.sleep(0.5)
