# файл config.py, где будем хранить и загружать переменные окружения в память приложения:

# Токен ненастоящий :) Подставьте свой
#token = '5416667430:AAGiAixxU1UTyKFJNiDQhYrD0IWp2WyONuw'



# file: config.py
from os import environ
from dotenv import load_dotenv

# Загрузка значений переменных окружения
load_dotenv()

API_ID = environ.get('API_ID')
API_HASH = environ.get('API_HASH')
SESSION_STRING = environ.get('SESSION_STRING')
TARGET_CHANNEL = environ.get('TARGET_CHANNEL')
SOURCE_CHANNEL = environ.get('SOURCE_CHANNEL')
DATABASE_URL = environ.get('DATABASE_URL')
