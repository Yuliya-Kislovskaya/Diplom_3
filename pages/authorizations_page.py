import allure
from pages.base_page import BasePage
from url import URL 
from locators.authorizations_locator import EMAIL_INPUT, PASSWORD_INPUT, BUTTON_ENTER

class AuthorizationsPage(BasePage):

    @allure.step('Вводит почту в поле на странице авторизации')
    def send_keys_email_input(self, email):
        self.send_keys(EMAIL_INPUT, email)

    @allure.step('Вводит пароль в поле на странице авторизации')
    def send_keys_password_input(self, password):
        self.send_keys(PASSWORD_INPUT, password)

    @allure.step('Нажатие на кнопку "Войти"')
    def click_button_enter(self):
        # Используем js_click для обхода ElementClickInterceptedException
        self.js_click(BUTTON_ENTER)

    @allure.step('Авторизация пользователя')
    def login(self, email, password):
        self.open(f"{URL}login") 
        self.send_keys_email_input(email)
        self.send_keys_password_input(password)
        self.click_button_enter()
        # Ждем успешного редиректа на главную
        self.wait_for_url(URL)



