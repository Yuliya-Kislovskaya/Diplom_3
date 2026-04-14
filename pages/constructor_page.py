import allure
import time
from selenium.webdriver.common.action_chains import ActionChains
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
        source = self.browser.find_element(*INGREDIENT_BUN)
        target = self.browser.find_element(*CONSTRUCTOR_BASKET)
        
        # Симуляция Drag-n-Drop через JS для стабильности в Firefox/Chrome
        js_script = """
        var source = arguments[0];
        var target = arguments[1];
        var dataTransfer = new DataTransfer();
        source.dispatchEvent(new DragEvent('dragstart', {bubbles: true, dataTransfer: dataTransfer}));
        target.dispatchEvent(new DragEvent('drop', {bubbles: true, dataTransfer: dataTransfer}));
        source.dispatchEvent(new DragEvent('dragend', {bubbles: true, dataTransfer: dataTransfer}));
        """
        self.browser.execute_script(js_script, source, target)
        
        # Ждем, пока на ингредиенте появится счетчик (подтверждение, что бургер не пуст)
        self.explicit_wait.until(EC.visibility_of_element_located(COUNT_INGREDIENT))

    @allure.step('Получение значения счетчика ингредиента')
    def get_count_value(self):
        return self.get_text_of_element(COUNT_INGREDIENT)

    @allure.step('Оформление заказа и получение его номера')
    def create_order_and_get_number(self):
        # Ожидаем физическую доступность кнопки оформления
        self._wait_until_element_not_obscured(ARRANGE_ORDER_BUTTON)
        self.js_click(ARRANGE_ORDER_BUTTON)
        
        # Ожидание смены "9999" на реальный номер
        self.explicit_wait.until(
            lambda driver: driver.find_element(*MODAL_ORDER_ID).text.strip().isdigit() and 
                           driver.find_element(*MODAL_ORDER_ID).text.strip() not in ["9999", "0", ""]
        )
        
        order_num = self.get_text_of_element(MODAL_ORDER_ID)
        
        # Закрываем модалку через проверку перекрытия
        self._wait_until_element_not_obscured(CLOSE_MODAL_BUTTON)
        self.js_click(CLOSE_MODAL_BUTTON)
        
        self.explicit_wait.until(EC.invisibility_of_element_located(MODAL_ORDER_ID))
        
        return order_num

    def _is_element_not_obscured(self, element):
        """Проверка, что элемент не перекрыт другим слоем в центре"""
        return self.browser.execute_script(
            """
            const elem = arguments[0];
            if (!elem) return false;
            const rect = elem.getBoundingClientRect();
            if (rect.width === 0 || rect.height === 0) return false;
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            const topElem = document.elementFromPoint(x, y);
            return topElem === elem || (elem && elem.contains(topElem));
            """,
            element,
        )

    def _wait_until_element_not_obscured(self, locator, timeout=15):
        """Ожидание, пока элемент станет доступен для клика (не перекрыт)"""
        def condition(driver):
            element = driver.find_element(*locator)
            return element if self._is_element_not_obscured(element) else False
        return self.explicit_wait.until(condition)
