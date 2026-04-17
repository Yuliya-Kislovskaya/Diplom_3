from selenium.webdriver.common.by import By

# Навигация
CONSTRUCTOR_BUTTON = (By.XPATH, ".//p[text()='Конструктор']")

# Ингредиенты и Конструктор
INGREDIENT_BUN = (By.XPATH, ".//p[text()='Флюоресцентная булка R2-D3']")
INGREDIENT_LINK = (By.XPATH, ".//a[contains(@href, '61c0c5a71d1f82001bdaaa6d')]")
CONSTRUCTOR_BASKET = (By.XPATH, ".//ul[contains(@class, 'BurgerConstructor_basket')]")

# Кнопки
ARRANGE_ORDER_BUTTON = (By.XPATH, ".//button[text()='Оформить заказ']")

# Модальное окно ингредиента
MODAL_TITLE = (By.XPATH, ".//h2[contains(@class, 'Modal_modal__title')]")
CLOSE_MODAL_BUTTON = (By.XPATH, ".//section[contains(@class, 'Modal_modal_opened')]//button[contains(@class, 'Modal_modal__close')]")

# Модальное окно заказа и номер
MODAL_ORDER_ID = (By.XPATH, ".//h2[contains(@class, 'text_type_digits-large')]")
LOADING_ICON = (By.XPATH, ".//img[@alt='loading...']")

# Счётчик
COUNT_INGREDIENT = (By.XPATH, ".//p[contains(@class, 'counter_counter__num') and text()='2']")

# Лента заказов
ORDER_NUMBERS_IN_WORK = (By.XPATH, ".//ul[contains(@class, 'OrderFeed_orderListReady')]//li")





