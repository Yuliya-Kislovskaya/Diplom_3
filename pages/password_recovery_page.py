import allure
from pages.base_page import BasePage
from data import LOGIN
from locators.password_recovery_locator import (
    BUTTON_PASSWORD_RECOVERY, EMAIL_INPUT_RECOVERY, 
    BUTTON_RECOVERY, SHOW_HIDE_BUTTON, PASSWORD_FIELD_ACTIVE
)

class PasswordRecoveryPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    @allure.step('Нажимает на ссылку "Восстановить пароль"')
    def click_link_password_recovery(self):
        self.click_element(BUTTON_PASSWORD_RECOVERY)

    @allure.step('Вводит email для восстановления')
    def send_keys_email_recovery(self, email=LOGIN):
        self.send_keys(EMAIL_INPUT_RECOVERY, email)

    @allure.step('Нажимает на кнопку "Восстановить"')
    def click_button_recovery(self):
        self.click_element(BUTTON_RECOVERY)

    @allure.step('Нажимает на иконку "Показать/скрыть" пароль')
    def click_show_hide_icon(self):
        # Используем js_click, так как иконка может быть перекрыта краем инпута
        self.js_click(SHOW_HIDE_BUTTON)

    @allure.step('Проверяет активность поля пароля (наличие активного класса)')
    def is_password_field_active(self):
        # Ждем появления элемента с локатором PASSWORD_FIELD_ACTIVE 
        # (который содержит класс инпута в активном состоянии)
        return self.explicit_wait.until(
            lambda d: d.find_element(*PASSWORD_FIELD_ACTIVE).is_displayed()
        )



