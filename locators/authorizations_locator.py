from selenium.webdriver.common.by import By

# Поле Email
EMAIL_INPUT = (By.NAME, "name")

# Поле Пароль
PASSWORD_INPUT = (By.NAME, "Пароль")

# Кнопка Войти
BUTTON_ENTER = (By.XPATH, ".//button[text()='Войти']")

# Ссылка "Восстановить пароль"
FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")

