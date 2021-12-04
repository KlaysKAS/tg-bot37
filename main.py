import os
from dotenv import load_dotenv, find_dotenv
from database import DB

load_dotenv(find_dotenv())  # Загрузка переменных окружения
# token = os.environ.get('API_TOKEN')

db = DB(os.environ.get('DATABASE_URL'))  # Экземпляр
