import requests
from selenium import webdriver
import pytest
import sys
import os
from helpers import generate_user_data
from url import URL, CREATE_USER, DELETE_USER
from pages.constructor_page import ConstructorPage
from pages.order_feed_page import OrderFeedPage
from pages.authorizations_page import AuthorizationsPage
from pages.personal_account_page import PersonalAccountPage
from pages.password_recovery_page import PasswordRecoveryPage

# Добавляем путь к директории проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

@pytest.fixture(params=["chrome", "firefox"])
def browser(request):
    if request.param == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(options=chrome_options)
    elif request.param == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=firefox_options)
        driver.set_window_size(1920, 1080)
    else:
        raise TypeError("Driver is not found")
    
    driver.get(URL)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def create_and_delete_user():
    """
    Фикстура для создания и удаления пользователя.
    Здесь yield необходим, так как после теста выполняется удаление.
    """
    payload = generate_user_data()
    response = requests.post(URL + CREATE_USER, json=payload)
    
    if response.status_code != 200:
        pytest.fail(f"Ошибка при создании пользователя: {response.text}")
    
    response_data = response.json()
    yield response, payload
    
    token = response_data.get('accessToken')
    if token:
        requests.delete(URL + DELETE_USER, headers={'Authorization': token})

@pytest.fixture
def prepare_for_constructor(browser, create_and_delete_user):
    """Подготовка страниц для тестов конструктора"""
    response, payload = create_and_delete_user
    return response, payload['email'], payload['password'], AuthorizationsPage(browser), ConstructorPage(browser), OrderFeedPage(browser)

@pytest.fixture()
def prepare_for_order(browser, create_and_delete_user):
    """Подготовка страниц для тестов ленты заказов"""
    response, payload = create_and_delete_user
    return response, payload['email'], payload['password'], AuthorizationsPage(browser), OrderFeedPage(browser), PersonalAccountPage(browser), ConstructorPage(browser)

@pytest.fixture()
def prepare_for_recovery_password(browser):
    """Подготовка страницы восстановления пароля"""
    return PasswordRecoveryPage(browser)

@pytest.fixture()
def prepare_for_personal_account(browser, create_and_delete_user):
    """Подготовка страниц для личного кабинета"""
    response, payload = create_and_delete_user
    return response, payload['email'], payload['password'], PersonalAccountPage(browser), AuthorizationsPage(browser)

