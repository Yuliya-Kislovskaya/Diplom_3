import allure
from data import DEFAULT_ORDER_NUMBER, INGREDIENT_DETAILS, COUNT_INGREDIENT
from url import LOGIN, URL, FEED

class TestToConstructor:

    @allure.title('Переход по клику на «Лента заказов»')
    def test_navigate_to_order_feed(self, browser, prepare_for_constructor):
        _, _, _, _, constructor, order_feed_page = prepare_for_constructor
        with allure.step('Открываем главную страницу'):
            constructor.open()
        with allure.step('Нажимаем кнопку "Лента заказов"'):
            order_feed_page.click_order_feed_button()
        with allure.step('Проверяем переход на страницу "Лента заказов"'):
            constructor.wait_for_url(f'{URL}{FEED}')
            assert constructor.get_current_url() == f'{URL}{FEED}'

    @allure.title('Если кликнуть на ингредиент, появится всплывающее окно с деталями')
    def test_click_ingredient_displays_popup_with_details(self, browser, prepare_for_constructor):
        _, _, _, _, constructor, _ = prepare_for_constructor
        with allure.step('Открываем страницу с конструктором'):
            constructor.open()
        with allure.step('Нажимаем на ингредиент'):
            constructor.click_on_ingredient()
        with allure.step('Проверяем заголовок модального окна'):
            assert constructor.get_modal_ingredient_text() == INGREDIENT_DETAILS

    @allure.title('Всплывающее окно закрывается кликом по крестику')
    def test_ingredient_popup_close(self, browser, prepare_for_constructor):
        _, _, _, _, constructor, _ = prepare_for_constructor
        with allure.step('Открываем страницу с конструктором'):
            constructor.open()
        with allure.step('Нажимаем на ингредиент и закрываем его'):
            constructor.click_on_ingredient()
            constructor.click_close_modal_ingredient()
        with allure.step('Проверяем, что окно закрылось (невидимо)'):
            assert constructor.check_modal_closed()

    @allure.title('При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается')
    def test_counter_increments_when_ingredient_added(self, browser, prepare_for_constructor):
        _, _, _, _, constructor, _ = prepare_for_constructor
        with allure.step('Открываем страницу с конструктором'):
            constructor.open()
        with allure.step('Перетаскиваем ингредиент в корзину'):
            constructor.add_ingredient_to_burger()
        with allure.step('Проверяем значение счетчика'):
            assert constructor.get_count_value() == COUNT_INGREDIENT

    @allure.title('Залогиненный пользователь может оформить заказ')
    def test_user_can_place_order(self, browser, prepare_for_constructor):
        _, email, password, auth, constructor, _ = prepare_for_constructor
        with allure.step('Авторизация пользователя'):
            auth.login(email, password)
        with allure.step('Добавляем ингредиент и оформляем заказ'):
            constructor.add_ingredient_to_burger()
            order_number = constructor.create_order_and_get_number()
        with allure.step('Проверяем, что номер заказа получен и он не дефолтный'):
             assert order_number != DEFAULT_ORDER_NUMBER
