import random
import string
import allure
import time

@allure.step('Генерация уникальных данных для пользователя')
def generate_user_data():
    # Добавляем метку текущего времени (секунды), чтобы избежать дублей
    timestamp = int(time.time())
    email = f"test-burger-{timestamp}{random.randint(1, 99)}@yandex.ru"
    
    # Генерация пароля
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    
    # Генерация имени
    name = f"StellarUser_{random.randint(1, 1000)}"
    
    return {
        "email": email,
        "password": password,
        "name": name
    }


