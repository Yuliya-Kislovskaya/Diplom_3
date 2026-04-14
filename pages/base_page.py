import allure
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from locators.personal_account_locator import BUTTON_PERSONAL_ACCOUNT
from url import URL
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, browser):
        self.browser = browser
        self.actions = ActionChains(self.browser)
        # Увеличила ожидание до 40 для тяжелых страниц в Firefox
        self.explicit_wait = WebDriverWait(self.browser, 40) 

    @allure.step('Получение текущего URL')
    def get_current_url(self):
        return self.browser.current_url

    @allure.step('Явное ожидание кликабельности элемента')
    def wait_element_clickable(self, locator):
        return self.explicit_wait.until(EC.element_to_be_clickable(locator))

    @allure.step('Общий метод для поиска элемента')
    def find(self, locator):
        self.explicit_wait.until(EC.visibility_of_element_located(locator))
        return self.browser.find_element(*locator)

    @allure.step('Поиск списка элементов')
    def find_elements(self, locator):
        self.explicit_wait.until(EC.visibility_of_any_elements_located(locator))
        return self.browser.find_elements(*locator)

    @allure.step('Прокрутка до элемента')
    def scroll_to_element(self, locator):
        element = self.find(locator)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step('Общий метод для клика по элементу')
    def click_element(self, locator):
        self.scroll_to_element(locator)
        try:
            self.wait_element_clickable(locator).click()
        except Exception:
            self.js_click(locator)

    @allure.step('Клик через JavaScript')
    def js_click(self, locator):
        element = self.find(locator)
        self.browser.execute_script("arguments[0].click();", element)

    @allure.step('Общий метод для ввода данных')
    def send_keys(self, locator, text):
        element = self.find(locator)
        element.send_keys(text)

    @allure.step('Открывает страницу')
    def open(self, url=None):
        target_url = url if url else URL
        self.browser.get(target_url)

    @allure.step('Ждет загрузки URL')
    def wait_for_url(self, url):
        self.explicit_wait.until(EC.url_to_be(url))

    @allure.step('Получение текста элемента')
    def get_text_of_element(self, locator):
        return self.find(locator).text

    @allure.step('Нажимает на кнопку "Личный кабинет"')
    def click_personal_account(self):
        self.js_click(BUTTON_PERSONAL_ACCOUNT)
        
    @allure.step('Перетаскивание элемента (Drag and Drop)')
    def drag_and_drop(self, source_locator, target_locator):
        source = self.find(source_locator)
        target = self.find(target_locator)
        self.actions.click_and_hold(source).pause(0.5).move_to_element(target).release().perform()

    # --- Новые методы для стабильности в Firefox ---

    def _is_element_not_obscured(self, element):
        """Проверяет через JS, что элемент является верхним в данной точке (не перекрыт)"""
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

    @allure.step('Ожидание, пока элемент перестанет быть перекрыт другими объектами')
    def wait_until_element_not_obscured(self, locator):
        """Ждет, пока центр элемента станет доступен для взаимодействия"""
        def condition(driver):
            element = driver.find_element(*locator)
            return element if self._is_element_not_obscured(element) else False
        
        return self.explicit_wait.until(condition)




