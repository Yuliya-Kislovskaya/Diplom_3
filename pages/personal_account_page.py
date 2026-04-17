import allure
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from locators.personal_account_locator import (
    BUTTON_EXIT, ORDER_HISTORY_LINK, ORDER_HISTORY_ITEM_NUMBER
)

class PersonalAccountPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    @allure.step('Нажимает на кнопку "Выход"')
    def click_button_exit(self):
        # Используем js_click для стабильного выхода
        self.js_click(BUTTON_EXIT)

    @allure.step('Нажимает на кнопку "История заказов"')
    def click_button_history(self):
        # Используем js_click для перехода в историю
        self.js_click(ORDER_HISTORY_LINK)

    @allure.step('Возвращает номер последнего заказа в ЛК')
    def get_order_history_item(self):
        self.explicit_wait.until(EC.presence_of_element_located(ORDER_HISTORY_ITEM_NUMBER))
        return self.get_text_of_element(ORDER_HISTORY_ITEM_NUMBER)


