import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.selenium.utils import scroll_down, scroll_up


def run_collections_scenario(driver):
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

    # Проверка на существование кнопки добавления в коллекции
    add_to_collection_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Добавить"]'))
    )
    assert add_to_collection_button is not None
    add_to_collection_button.click()
    time.sleep(0.5)
    add_to_collection_button.click()
    time.sleep(0.5)
    add_to_collection_button.click()
    time.sleep(0.5)

    # Проверка на существование кнопок коллекций (д.б. 3)
    collection_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collection_buttons is not None
    assert len(collection_buttons) == 3
    time.sleep(0.5)

    # Добавление книги в коллекцию "Буду читать"
    to_be_read_button, now_reading_button, read_button = collection_buttons
    to_be_read_button.click()

    time.sleep(0.5)

    # Возврат на главную страницу
    books_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Книги"]'))
    )
    books_button.click()
    time.sleep(0.5)

    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 2ой книги
    book_cards[1].click()

    # Проверка на существование кнопки добавления в коллекции
    add_to_collection_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Добавить"]'))
    )
    assert add_to_collection_button is not None
    add_to_collection_button.click()

    # Проверка на существование кнопок коллекций (д.б. 3)
    collection_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collection_buttons is not None
    assert len(collection_buttons) == 3
    time.sleep(0.5)

    # Добавление книги в коллекцию "Читаю"
    to_be_read_button, now_reading_button, read_button = collection_buttons
    now_reading_button.click()

    time.sleep(0.5)

    # Возврат на главную страницу
    books_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Книги"]'))
    )
    books_button.click()
    time.sleep(0.5)

    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 3ой книги
    book_cards[2].click()

    # Проверка на существование кнопки добавления в коллекции
    add_to_collection_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Добавить"]'))
    )
    assert add_to_collection_button is not None
    add_to_collection_button.click()

    # Проверка на существование кнопок коллекций (д.б. 3)
    collection_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collection_buttons is not None
    assert len(collection_buttons) == 3
    time.sleep(0.5)

    # Добавление книги в коллекцию "Прочитано"
    to_be_read_button, now_reading_button, read_button = collection_buttons
    read_button.click()

    time.sleep(0.5)

    # Возврат на главную страницу
    books_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Книги"]'))
    )
    books_button.click()
    time.sleep(0.5)

    # Переход на вкладку с коллекциями
    user_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Pavel"]'))
    )
    assert user_button is not None
    time.sleep(0.5)

    user_button.click()

    collections_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Подборки книг"]'))
    )

    time.sleep(0.5)
    collections_button.click()

    # Проверка на существование 3 базовых коллекций
    collections = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collections is not None
    assert len(collection_buttons) == 3

    # Выбор книги "Происхождение"
    origin_book = WebDriverWait(collections[0], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert origin_book is not None

    # Выбор книги "Ангелы и демоны"
    angels_and_demons_book = WebDriverWait(collections[1], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert angels_and_demons_book is not None

    # Выбор книги "Цифровая крепость"
    digital_fortress_book = WebDriverWait(collections[2], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert digital_fortress_book is not None

    time.sleep(0.5)
    origin_book.click()
    time.sleep(0.5)
    angels_and_demons_book.click()
    time.sleep(0.5)
    digital_fortress_book.click()
    time.sleep(0.5)
    origin_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Преренести книгу в "Читаю"
    buttons[0].click()

    time.sleep(0.5)

    # Выбор книги "Ангелы и демоны"
    angels_and_demons_book = WebDriverWait(collections[1], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert angels_and_demons_book is not None
    angels_and_demons_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Преренести книгу в "Прочитано"
    buttons[1].click()

    time.sleep(0.5)

    # Выбор книги "Происхождение"
    origin_book = WebDriverWait(collections[1], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert origin_book is not None
    origin_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Преренести книгу в "Прочитано"
    buttons[1].click()

    time.sleep(0.5)

    # Выбор книги "Цифровая крепость"
    digital_fortress_book = WebDriverWait(collections[2], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert digital_fortress_book is not None
    digital_fortress_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Удалить книгу из коллекции
    buttons[2].click()

    time.sleep(0.5)

    # Выбор книги "Ангелы и демоны"
    angels_and_demons_book = WebDriverWait(collections[2], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert angels_and_demons_book is not None
    angels_and_demons_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Удалить книгу из коллекции
    buttons[2].click()

    time.sleep(0.5)

    # Выбор книги "Происхождение"
    origin_book = WebDriverWait(collections[2], 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert origin_book is not None
    origin_book.click()

    # Выбор выпадающего списка
    popup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'Popup'))
    )
    assert popup is not None

    # Выбор кнопок выпадающего списка
    buttons = WebDriverWait(popup, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'button'))
    )
    assert buttons is not None
    assert len(buttons) == 3

    time.sleep(0.5)

    # Удалить книгу из коллекции
    buttons[2].click()

    time.sleep(0.5)

    # Выбор кнопки создания новой коллекции
    create_collection_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*/button[text()="Создать новую подборку +"]'))
    )
    assert create_collection_button is not None
    create_collection_button.click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка существования 4 коллекций (3 базовые + 1 созданная)
    collections = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collections is not None
    assert len(collections) == 4

    # Выбор созданной коллекции
    created_collection = collections[3]
    assert created_collection is not None

    # Выбор названия созданной коллекции
    created_collection_name_input = WebDriverWait(created_collection, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, 'input'))
    )
    assert created_collection_name_input is not None
    created_collection_name_input.send_keys(Keys.CONTROL, 'a')
    created_collection_name_input.send_keys(Keys.DELETE)
    created_collection_name_input.send_keys("Любимые книги", Keys.ENTER)

    time.sleep(0.5)
    scroll_up(driver)
    time.sleep(0.5)

    # Возврат на главную страницу
    books_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Книги"]'))
    )
    books_button.click()

    time.sleep(0.5)

    # Проверка на существование карточек с книгами
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Переход на страницу 1ой книги
    book_cards[0].click()

    # Проверка на существование кнопки добавления в коллекции
    add_to_collection_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Добавить"]'))
    )
    assert add_to_collection_button is not None
    add_to_collection_button.click()

    # Проверка на существование кнопок коллекций (д.б. 4 = 3 базовых + 1 созданная)
    collection_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collection_buttons is not None
    assert len(collection_buttons) == 4
    time.sleep(0.5)

    # Добавление книги в созданную коллекцию "Любимые книги"
    to_be_read_button, now_reading_button, read_button, favorite_books = collection_buttons
    favorite_books.click()

    time.sleep(0.5)

    # Переход на вкладку с коллекциями
    user_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Pavel"]'))
    )
    assert user_button is not None
    time.sleep(0.5)

    user_button.click()

    collections_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Подборки книг"]'))
    )

    time.sleep(0.5)
    collections_button.click()

    time.sleep(0.5)
    scroll_down(driver)
    time.sleep(0.5)

    # Проверка на существование книги в созданной коллекции
    book = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'BookElement'))
    )
    assert book is not None

    # Удаление созданной подборки
    delete_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'DeleteCollectionButton'))
    )
    assert delete_button is not None
    delete_button.click()
    time.sleep(0.5)

    # Проверка на отсутствие дополнительных подборок
    collections = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Collection'))
    )
    assert collections is not None
    assert len(collections) == 3

    time.sleep(0.5)