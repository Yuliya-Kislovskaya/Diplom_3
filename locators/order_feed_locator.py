from selenium.webdriver.common.by import By

# Кнопка перехода в Ленту (Header)
ORDER_FEED_BUTTON = (By.XPATH, ".//p[text()='Лента Заказов']")

# Элементы истории и карточки заказа
ORDER_CARD = (By.XPATH, ".//li[contains(@class, 'OrderHistory_listItem')]")
POPUP_ORDER_DETAILS = (By.XPATH, ".//div[contains(@class, 'Modal_orderBox')]")

# Счетчики (используем поиск по тексту заголовка и соседний элемент)
COMPLETED_ALL_TIME = (By.XPATH, ".//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'digits-large')]")
COMPLETED_TODAY = (By.XPATH, ".//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'digits-large')]")

# Раздел "В работе" (список номеров заказов)
# Замена CSS-селектор на надежный XPath, который ищет в колонке "В работе" (Ready/Pending)
# Замените в locators/order_feed_locator.py:
# Локатор именно для списка заказов в колонке "В работе"
ORDERS_IN_WORK_LIST = (By.XPATH, ".//p[text()='В работе:']/following-sibling::ul//li")



# Локатор для конкретного номера заказа (динамический, подставлять через f-строку в методе)
# Пример: f".//li[text()='0{order_number}']"

