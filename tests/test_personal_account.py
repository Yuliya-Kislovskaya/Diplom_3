import allure
import pytest
from url import URL, LOGIN, HISTORY

class TestPersonalAccount:

    @allure.title('Переход по клику на «Личный кабинет»')
    def test_personal_cabinet_navigation(self, prepare_for_personal_account): # Убран browser
        _, _, _, personal_account, _ = prepare_for_personal_account
        with allure.step('Открываем главную страницу'):
            personal_account.open()
        with allure.step('Нажимаем на кнопку "Личный кабинет"'):
            personal_account.click_personal_account()
        with allure.step('Проверяем, что открылась страница авторизации (для неавторизованного)'):
            personal_account.wait_for_url(f'{URL}{LOGIN}')
            assert personal_account.get_current_url() == f'{URL}{LOGIN}'

    @allure.title('Переход в раздел «История заказов»')
    def test_navigate_to_order_history(self, prepare_for_personal_account):
        _, email, password, personal_account, auth = prepare_for_personal_account
        with allure.step('Авторизация пользователя'):
            auth.login(email, password)
        with allure.step('Переход в Личный кабинет'):
            personal_account.click_personal_account()
        with allure.step('Переход в "История заказов"'):
            personal_account.click_button_history()
        with allure.step('Проверяем переход в Историю'):
            personal_account.wait_for_url(f'{URL}{HISTORY}')
            assert personal_account.get_current_url() == f'{URL}{HISTORY}'

    @allure.title('Выход из аккаунта')
    def test_logout_your_account(self, prepare_for_personal_account):
        _, email, password, personal_account, auth = prepare_for_personal_account
        with allure.step('Авторизация и переход в профиль'):
            auth.login(email, password)
            personal_account.click_personal_account()
        with allure.step('Нажимаем кнопку "Выход"'):
            personal_account.click_button_exit()
        with allure.step('Проверяем редирект на страницу входа'):
            personal_account.wait_for_url(f'{URL}{LOGIN}')
            assert personal_account.get_current_url() == f'{URL}{LOGIN}'
