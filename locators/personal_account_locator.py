from selenium.webdriver.common.by import By

# Кнопка перехода в Личный Кабинет (в хедере)
BUTTON_PERSONAL_ACCOUNT = (By.XPATH, ".//p[text()='Личный Кабинет']")

# Ссылка на Историю заказов в боковом меню
ORDER_HISTORY_LINK = (By.XPATH, ".//a[@href='/account/order-history']")

# Кнопка Выход
BUTTON_EXIT = (By.XPATH, ".//button[text()='Выход']")

# Заголовок страницы Вход (для проверки успешного логаута)
TITLE_AUTHORIZATION = (By.XPATH, ".//h2[text()='Вход']")

# Номера заказов в истории (универсальный локатор для всех карточек)
ORDER_HISTORY_ITEM_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")
