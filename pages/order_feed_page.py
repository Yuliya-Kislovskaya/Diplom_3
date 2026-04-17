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
        return [order.text.strip().replace('#', '') for order in orders]

    @allure.step('Возвращает количество заказов за все время')
    def get_completed_all_time(self):
        self.explicit_wait.until(lambda _: self.get_text_of_element(COMPLETED_ALL_TIME).strip().isdigit())
        return self.get_text_of_element(COMPLETED_ALL_TIME)

    @allure.step('Возвращает количество заказов за сегодня')
    def get_completed_today(self):
        self.explicit_wait.until(lambda _: self.get_text_of_element(COMPLETED_TODAY).strip().isdigit())
        return self.get_text_of_element(COMPLETED_TODAY)

    @allure.step('Ожидает обновления счетчика')
    def wait_for_counter_to_change(self, counter_type, old_value):
        locator = COMPLETED_ALL_TIME if counter_type == 'all' else COMPLETED_TODAY
        self.explicit_wait.until(EC.visibility_of_element_located(locator))
        
        def condition(_):
            current_value = self.get_text_of_element(locator).strip()
            return current_value != str(old_value) and current_value.isdigit()
            
        return self.explicit_wait.until(condition)

    @allure.step('Получает список номеров заказов в разделе "В работе"')
    def get_at_work_orders(self):
        try:
            def condition(_):
                # Используем поиск через внутренний метод браузера
                work_orders = self.browser.find_elements(*ORDERS_IN_WORK_LIST)
                return any(el.text.strip().replace('#', '').isdigit() for el in work_orders)

            self.explicit_wait.until(condition)
            orders = self.find_elements(ORDERS_IN_WORK_LIST)
            return [order.text.strip().replace('#', '') for order in orders]
        except Exception:
            return []

    @allure.step('Ожидание появления номера заказа {order_number} в разделе "В работе"')
    def wait_for_order_in_work_section(self, order_number):
        """Метод инкапсулирует ожидание и обновление страницы для стабильности"""
        expected_number = order_number.lstrip('0')

        def check_order_in_list(_):
            orders = self.get_at_work_orders()
            return any(expected_number == num.lstrip('0') for num in orders)

        try:
            # Первая попытка ожидания
            return self.explicit_wait.until(check_order_in_list)
        except Exception:
            # Если не появился (проблема WebSocket в Firefox) — рефреш и повтор
            with allure.step('Обновление страницы для синхронизации WebSocket'):
                self.browser.refresh()
            return self.explicit_wait.until(check_order_in_list)

    @allure.step('Нажимает на карточку заказа в списке')
    def click_order_card(self):
        self.explicit_wait.until(EC.element_to_be_clickable(ORDER_CARD))
        self.js_click(ORDER_CARD)

    @allure.step('Проверяет наличие всплывающего окна с деталями')
    def is_popup_displayed(self):
        return self.explicit_wait.until(EC.visibility_of_element_located(POPUP_ORDER_DETAILS)).is_displayed()

