from selenium.webdriver.common.by import By

# Кнопка/ссылка для перехода на страницу восстановления
BUTTON_PASSWORD_RECOVERY = (By.LINK_TEXT, "Восстановить пароль")

# Поле ввода Email
EMAIL_INPUT_RECOVERY = (By.XPATH, ".//input[@name='name']")

# Кнопка "Восстановить"
BUTTON_RECOVERY = (By.XPATH, ".//button[text()='Восстановить']")

# Заголовок страницы (для проверок перехода)
TITLE_PASSWORD_RECOVERY = (By.XPATH, ".//h2[text()='Восстановление пароля']")

# Кнопка показать/скрыть пароль (глазик)
SHOW_HIDE_BUTTON = (By.XPATH, ".//div[contains(@class, 'input__icon')]")

# Поле пароля в активном состоянии (когда на него нажат фокус или изменен статус)
PASSWORD_FIELD_ACTIVE = (By.XPATH, ".//div[contains(@class, 'input_status_active')]//input")
