import allure
import pytest
from selenium.webdriver.support.wait import WebDriverWait

class TestOrderFeed:

    @allure.title('При создании нового заказа счётчик «Выполнено за всё время» увеличивается')
    def test_total_orders_counter_increases(self, browser, prepare_for_order):
        _, email, password, auth, feed_page, _, constructor = prepare_for_order

        with allure.step('Авторизация и получение начального значения счетчика'):
            auth.login(email, password)
            feed_page.click_order_feed_button()
            initial_count = int(feed_page.get_completed_all_time())

        with allure.step('Создание нового заказа'):
            constructor.click_constructor_button()
            constructor.add_ingredient_to_burger()
            constructor.create_order_and_get_number()

        with allure.step('Проверка увеличения счетчика "Выполнено за все время"'):
            feed_page.click_order_feed_button()
            # Обновление страницы помогает Firefox подтянуть актуальный стейт WebSocket
            browser.refresh()
            feed_page.wait_for_counter_to_change('all', initial_count)
            new_count = int(feed_page.get_completed_all_time())
            assert new_count > initial_count

    @allure.title('При создании нового заказа счётчик «Выполнено за сегодня» увеличивается')
    def test_today_orders_counter_increases(self, browser, prepare_for_order):
        _, email, password, auth, feed_page, _, constructor = prepare_for_order

        with allure.step('Авторизация и получение начального значения счетчика "За сегодня"'):
            auth.login(email, password)
            feed_page.click_order_feed_button()
            initial_count = int(feed_page.get_completed_today())

        with allure.step('Создание нового заказа'):
            constructor.click_constructor_button()
            constructor.add_ingredient_to_burger()
            constructor.create_order_and_get_number()

        with allure.step('Проверка увеличения счетчика "Выполнено за сегодня"'):
            feed_page.click_order_feed_button()
            browser.refresh()
            feed_page.wait_for_counter_to_change('today', initial_count)
            new_count = int(feed_page.get_completed_today())
            assert new_count > initial_count

    @allure.title('После оформления заказа его номер появляется в разделе «В работе»')
    def test_order_appears_in_work_section(self, browser, prepare_for_order):
        _, email, password, auth, feed_page, _, constructor = prepare_for_order

        with allure.step('Авторизация и оформление заказа'):
            auth.login(email, password)
            constructor.add_ingredient_to_burger()
            order_number = constructor.create_order_and_get_number()

        with allure.step('Переход в ленту и поиск номера в разделе "В работе"'):
            feed_page.click_order_feed_button()
            
            # Очищаем созданный номер от ведущих нулей для сравнения
            expected_number = order_number.lstrip('0')

            def check_order_in_list(driver):
                orders = feed_page.get_at_work_orders()
                if not orders:
                    return False
                # Очищаем от нулей каждый номер из списка ленты и ищем совпадение
                return any(expected_number == num.lstrip('0') for num in orders)

            try:
                # Первичная попытка дождаться появления номера
                WebDriverWait(browser, 20).until(check_order_in_list)
            except Exception:
                # Если не появился — рефрешим страницу (костыль для Firefox) и ждем еще раз
                browser.refresh()
                WebDriverWait(browser, 20).until(check_order_in_list)

        # Финальная проверка
        assert check_order_in_list(browser), f"Заказ {expected_number} не найден в разделе 'В работе'"


