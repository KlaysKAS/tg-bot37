import os
from dotenv import load_dotenv, find_dotenv
from database import DB

load_dotenv(find_dotenv())  # Загрузка переменных окружения

db = DB(os.environ.get('DATABASE_URL'))  # Экземпляр
