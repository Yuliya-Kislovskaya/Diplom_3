import allure
from pages.base_page import BasePage
from selenium.webdriver.support import expected_conditions as EC
from locators.order_feed_locator import (
    ORDER_FEED_BUTTON, ORDER_CARD, POPUP_ORDER_DETAILS, 
    COMPLETED_ALL_TIME, COMPLETED_TODAY, ORDERS_IN_WORK_LIST
)

class OrderFeedPage(BasePage):
    def __init__(self, browser):
        super().__init__(browser)

    @allure.step('Нажимает на кнопку "Лента заказов"')
    def click_order_feed_button(self):
        self.js_click(ORDER_FEED_BUTTON)

    @allure.step('Возвращает список номеров всех заказов в ленте')
    def get_all_order_numbers(self):
        self.explicit_wait.until(EC.visibility_of_any_elements_located(ORDER_CARD))
        orders = self.find_elements(ORDER_CARD)
        # Извлекаем текст и чистим от символа #, чтобы остались только цифры
        return [order.text.strip().replace('#', '') for order in orders]

    @allure.step('Возвращает количество заказов за все время')
    def get_completed_all_time(self):
        self.explicit_wait.until(lambda d: d.find_element(*COMPLETED_ALL_TIME).text.strip().isdigit())
        return self.get_text_of_element(COMPLETED_ALL_TIME)

    @allure.step('Возвращает количество заказов за сегодня')
    def get_completed_today(self):
        self.explicit_wait.until(lambda d: d.find_element(*COMPLETED_TODAY).text.strip().isdigit())
        return self.get_text_of_element(COMPLETED_TODAY)

    @allure.step('Ожидает обновления счетчика')
    def wait_for_counter_to_change(self, counter_type, old_value):
        locator = COMPLETED_ALL_TIME if counter_type == 'all' else COMPLETED_TODAY
        self.explicit_wait.until(EC.visibility_of_element_located(locator))
        
        return self.explicit_wait.until(
            lambda d: d.find_element(*locator).text.strip() != str(old_value) and 
                      d.find_element(*locator).text.strip().isdigit()
        )

    @allure.step('Получает список номеров заказов в разделе "В работе"')
    def get_at_work_orders(self):
        try:
            # Ожидаем, пока в разделе появится хотя бы один цифровой номер заказа
            self.explicit_wait.until(
                lambda driver: any(el.text.strip().replace('#', '').isdigit() 
                                   for el in driver.find_elements(*ORDERS_IN_WORK_LIST))
            )
            orders = self.find_elements(ORDERS_IN_WORK_LIST)
            # Возвращаем список очищенных номеров
            return [order.text.strip().replace('#', '') for order in orders]
        except Exception:
            # Если за таймаут заказы не появились, возвращаем пустой список
            return []

    @allure.step('Нажимает на карточку заказа в списке')
    def click_order_card(self):
        self.explicit_wait.until(EC.element_to_be_clickable(ORDER_CARD))
        self.js_click(ORDER_CARD)

    @allure.step('Проверяет наличие всплывающего окна с деталями')
    def is_popup_displayed(self):
        return self.explicit_wait.until(EC.visibility_of_element_located(POPUP_ORDER_DETAILS)).is_displayed()
