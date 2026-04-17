import allure
from url import URL, RESET_PASSWORD, FORGOT_PASSWORD, LOGIN

class TestPasswordRecovery:

    @allure.title('Переход на страницу восстановления пароля по кнопке «Восстановить пароль»')
    def test_password_recovery_page(self, prepare_for_recovery_password):
        recovery_page = prepare_for_recovery_password
        with allure.step('Открываем страницу авторизации'):
            recovery_page.open(f'{URL}{LOGIN}')
        with allure.step('Нажимаем на кнопку "Восстановить пароль"'):
            recovery_page.click_link_password_recovery()
        with allure.step('Проверяем переход на страницу forgot-password'):
            recovery_page.wait_for_url(f'{URL}{FORGOT_PASSWORD}')
            assert recovery_page.get_current_url() == f'{URL}{FORGOT_PASSWORD}'

    @allure.title('Ввод почты и клик по кнопке «Восстановить»')
    def test_password_reset_email_submission(self, prepare_for_recovery_password):
        recovery_page = prepare_for_recovery_password
        with allure.step('Открываем страницу восстановления'):
            recovery_page.open(f'{URL}{FORGOT_PASSWORD}')
        with allure.step('Вводим почту'):
            recovery_page.send_keys_email_recovery()
        with allure.step('Нажимаем кнопку "Восстановить"'):
            recovery_page.click_button_recovery()
        with allure.step('Проверяем переход на страницу reset-password'):
            recovery_page.wait_for_url(f'{URL}{RESET_PASSWORD}')
            assert recovery_page.get_current_url() == f'{URL}{RESET_PASSWORD}'

    @allure.title('Клик по кнопке показать/скрыть пароль делает поле активным')
    def test_show_activates_password_field(self, prepare_for_recovery_password):
        recovery_page = prepare_for_recovery_password
        
        with allure.step('Проходим этап ввода email для доступа к reset-password'):
            recovery_page.open(f'{URL}{FORGOT_PASSWORD}')
            recovery_page.send_keys_email_recovery()
            recovery_page.click_button_recovery()
            recovery_page.wait_for_url(f'{URL}{RESET_PASSWORD}')

        with allure.step('Нажимаем на иконку "глазика" (показать/скрыть)'):
            recovery_page.click_show_hide_icon()

        with allure.step('Проверяем, что поле пароля стало активным'):
            assert recovery_page.is_password_field_active()






