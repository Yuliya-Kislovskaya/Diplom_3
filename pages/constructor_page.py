import allure
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.constructor_locator import (
    INGREDIENT_LINK, INGREDIENT_BUN, ARRANGE_ORDER_BUTTON, MODAL_TITLE,
    CLOSE_MODAL_BUTTON, CONSTRUCTOR_BASKET,
    COUNT_INGREDIENT, MODAL_ORDER_ID, CONSTRUCTOR_BUTTON
)

class ConstructorPage(BasePage):

    @allure.step('Нажатие на ингредиент')
    def click_on_ingredient(self):
        self.scroll_to_element(INGREDIENT_LINK)
        self.js_click(INGREDIENT_LINK)

    @allure.step('Получение текста из модального окна ингредиента')
    def get_modal_ingredient_text(self):
        return self.get_text_of_element(MODAL_TITLE)

    @allure.step('Закрытие модального окна ингредиента')
    def click_close_modal_ingredient(self):
        self.js_click(CLOSE_MODAL_BUTTON)

    @allure.step('Проверка, что модальное окно закрылось')
    def check_modal_closed(self):
        return self.explicit_wait.until(EC.invisibility_of_element_located(MODAL_TITLE))

    @allure.step('Переход в Конструктор по кнопке')
    def click_constructor_button(self):
        self.js_click(CONSTRUCTOR_BUTTON)

    @allure.step('Добавление ингредиента в заказ (Drag-n-Drop через JS)')
    def add_ingredient_to_burger(self):
        self.scroll_to_element(INGREDIENT_BUN)
        source = self.find(INGREDIENT_BUN)
        target = self.find(CONSTRUCTOR_BASKET)
        
        js_script = """
        var source = arguments[0];
        var target = arguments[1];
        var dataTransfer = new DataTransfer();
        source.dispatchEvent(new DragEvent('dragstart', {bubbles: true, dataTransfer: dataTransfer}));
        target.dispatchEvent(new DragEvent('drop', {bubbles: true, dataTransfer: dataTransfer}));
        source.dispatchEvent(new DragEvent('dragend', {bubbles: true, dataTransfer: dataTransfer}));
        """
        self.browser.execute_script(js_script, source, target)
        
        # Ждем, пока на ингредиенте появится счетчик
        self.explicit_wait.until(EC.visibility_of_element_located(COUNT_INGREDIENT))

    @allure.step('Получение значения счетчика ингредиента')
    def get_count_value(self):
        return self.get_text_of_element(COUNT_INGREDIENT)

    @allure.step('Оформление заказа и получение его номера')
    def create_order_and_get_number(self):
        self.wait_until_element_not_obscured(ARRANGE_ORDER_BUTTON)
        self.js_click(ARRANGE_ORDER_BUTTON)
        
        self.wait_for_order_number(MODAL_ORDER_ID)
        
        order_num = self.get_text_of_element(MODAL_ORDER_ID)
        
        # Закрываем модалку, ожидая её доступности через базовый метод
        self.wait_until_element_not_obscured(CLOSE_MODAL_BUTTON)
        self.js_click(CLOSE_MODAL_BUTTON)
        
        self.explicit_wait.until(EC.invisibility_of_element_located(MODAL_ORDER_ID))
        
        return order_num

