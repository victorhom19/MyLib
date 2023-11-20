import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run_books_scenario(driver):
    driver.get('http://localhost:3000')

    # Проверка на существование карточек книг (д.б. 10 штук)
    book_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert book_cards is not None
    assert len(book_cards) == 10

    time.sleep(0.5)

    # Проверка на существование фильтра жанров, года издания, фильтра по авторам
    genre_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'GenreFilter'))
    )
    assert genre_filter is not None

    year_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'YearFilter'))
    )
    assert year_filter is not None

    author_filter = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'AuthorFilter'))
    )
    assert author_filter is not None

    time.sleep(1)

    # Нажатие на кнопки "Показать/Скрыть" для фильтра по жанрам
    genre_filter_expand_button = WebDriverWait(genre_filter, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Показать все"]'))
    )
    assert genre_filter_expand_button is not None
    time.sleep(0.5)
    genre_filter_expand_button.click()

    genre_filter_shrink_button = WebDriverWait(genre_filter, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Скрыть"]'))
    )
    assert genre_filter_shrink_button is not None
    time.sleep(0.5)
    genre_filter_shrink_button.click()

    time.sleep(1)

    # Нажатие на кнопки "Показать/Скрыть" для фильтра по авторам
    author_filter_expand_button = WebDriverWait(author_filter, 10).until(
        EC.presence_of_element_located((By.XPATH, 'button[text()="Показать все"]'))
    )
    assert author_filter_expand_button is not None
    time.sleep(0.5)
    author_filter_expand_button.click()

    author_filter_shrink_button = WebDriverWait(author_filter, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Скрыть"]'))
    )
    assert author_filter_shrink_button is not None
    time.sleep(0.5)
    author_filter_shrink_button.click()

    time.sleep(1)

    # Проверка количества кнопок фильтров по жанрам (д.б. 5)
    filter_buttons = WebDriverWait(genre_filter, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, 'div[@class="Element"]/button'))
    )
    assert filter_buttons is not None
    assert len(filter_buttons) == 5

    # Фильтр "Детектив"
    filter_buttons[0].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 3
    time.sleep(0.5)
    filter_buttons[0].click()
    time.sleep(1)

    # Фильтр "Триллер"
    filter_buttons[1].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 3
    time.sleep(0.5)
    filter_buttons[1].click()
    time.sleep(1)

    # Фильтр "Научная фантастика"
    filter_buttons[2].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 4
    time.sleep(0.5)
    filter_buttons[2].click()
    time.sleep(1)

    # Определение input'ов фильтрации по году издания
    year_inputs = WebDriverWait(year_filter, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    assert year_inputs is not None
    year_from_input, year_to_input = year_inputs

    # Фильтр "после 2000 года"
    year_from_input.send_keys('2000')
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 5
    time.sleep(1)
    year_from_input.send_keys(Keys.CONTROL, 'a')
    year_from_input.send_keys(Keys.DELETE)
    time.sleep(1)

    # Фильтр "до 2000 года"
    year_to_input.send_keys('2000')
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 8
    time.sleep(1)
    year_to_input.send_keys(Keys.CONTROL, 'a')
    year_to_input.send_keys(Keys.DELETE)
    time.sleep(1)

    # Фильтр "с 2000 по 2015 года"
    year_from_input.send_keys('2000')
    time.sleep(0.5)
    year_to_input.send_keys('2015')
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 2
    time.sleep(1)
    year_from_input.send_keys(Keys.CONTROL, 'a')
    year_from_input.send_keys(Keys.DELETE)
    year_to_input.send_keys(Keys.CONTROL, 'a')
    year_to_input.send_keys(Keys.DELETE)
    time.sleep(1)

    # Проверка количества кнопок фильтров по авторам (д.б. 5)
    filter_buttons = WebDriverWait(author_filter, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, 'div[@class="Element"]/button'))
    )
    assert filter_buttons is not None
    assert len(filter_buttons) == 5

    # Фильтр "Дэн Браун"
    filter_buttons[0].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 3
    time.sleep(0.5)
    filter_buttons[0].click()
    time.sleep(1)

    # Фильтр "Энди Вейер"
    filter_buttons[1].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 3
    time.sleep(0.5)
    filter_buttons[1].click()
    time.sleep(1)

    # Фильтр "Стивен Кинг"
    filter_buttons[2].click()
    time.sleep(1)

    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 3
    time.sleep(0.5)
    filter_buttons[2].click()
    time.sleep(1)

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

    # Проверка пагинации с помощью стрелок
    pagination_right_arrow.click()
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 2
    time.sleep(0.5)

    pagination_left_arrow.click()
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 10
    time.sleep(0.5)

    # Проверка пагинации с помощью кнопок
    pages[1].click()
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 2
    time.sleep(0.5)

    pages[0].click()
    time.sleep(0.5)
    filtered_books = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'BookCard'))
    )
    assert filtered_books is not None
    assert len(filtered_books) == 10
    time.sleep(0.5)

    # Проверка существования поля поиска книг
    book_search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="AppHeader"]/input'))
    )
    assert book_search_input is not None

    # Поиск "он"
    book_search_input.send_keys('он')
    time.sleep(1)
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[@class="Book"]'))
    )
    assert search_results is not None
    assert len(search_results) == 2

    time.sleep(0.5)
    book_search_input.send_keys(Keys.CONTROL, 'a')
    book_search_input.send_keys(Keys.DELETE)
    time.sleep(1)

    # Поиск
    book_search_input.send_keys('Происхождение')
    time.sleep(1)
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//button[@class="Book"]'))
    )
    assert search_results is not None
    assert len(search_results) == 1

    time.sleep(0.5)

    search_results[0].click()

    time.sleep(1)

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[text()="Происхождение"]'))
    )
    assert title is not None
    time.sleep(1)
