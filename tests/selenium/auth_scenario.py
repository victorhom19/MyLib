import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def run_auth_scenario(driver):
    driver.get('http://localhost:3000')

    # Проверка на существование кнопки Войти
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Войти"]'))
    )
    assert button is not None
    time.sleep(0.5)

    # Проверка на существование кнопки Регистрация
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Регистрация"]'))
    )
    assert button is not None
    button.click()
    time.sleep(0.5)

    inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    assert inputs is not None
    assert len(inputs) == 3
    time.sleep(0.5)

    # Проверка на существование кнопки Назад
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Назад"]'))
    )
    assert button is not None
    button.click()
    time.sleep(0.5)

    # Проверка на существование кнопки Регистрация
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Регистрация"]'))
    )
    assert button is not None
    button.click()
    time.sleep(0.5)

    inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'input'))
    )
    assert inputs is not None
    assert len(inputs) == 3
    name, email, password = inputs
    name.send_keys('Лиза')
    time.sleep(0.5)
    email.send_keys('admin@gmail.com')
    time.sleep(0.5)
    password.send_keys('1234')
    time.sleep(0.5)

    # Проверка на существование кнопки Зарегистрироваться
    register_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Зарегистрироваться"]'))
    )
    assert button is not None
    register_button.click()

    # Проверка на ошибку регистрации: пользователь с почтой admin@gmail.com уже зарегистрирован
    error_inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Error'))
    )
    assert error_inputs is not None and len(error_inputs) > 0

    time.sleep(0.5)
    email.send_keys('lisa@gmail.com')
    time.sleep(0.5)
    register_button.click()

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
    email.send_keys('lisa@gmail.com')
    time.sleep(0.5)
    password.send_keys('12345')

    continue_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Продолжить"]'))
    )
    assert continue_button is not None
    time.sleep(0.5)
    continue_button.click()

    error_inputs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'Error'))
    )
    assert error_inputs is not None and len(error_inputs) > 0

    time.sleep(0.5)
    email.send_keys('lisa@gmail.com')
    time.sleep(0.5)
    password.send_keys('1234')
    continue_button.click()
    time.sleep(2)

    user_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Лиза"]'))
    )
    assert user_button is not None
    time.sleep(0.5)

    user_button.click()
    time.sleep(0.5)
    user_button.click()

    time.sleep(0.5)
    user_button.click()

    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Выйти из аккаунта"]'))
    )

    time.sleep(1)
    logout_button.click()

    # Проверка на существование кнопки Войти
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Войти"]'))
    )
    assert button is not None
    time.sleep(0.5)

    # Проверка на существование кнопки Регистрация
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="Регистрация"]'))
    )
    assert button is not None
