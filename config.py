import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    DB_NAME: str = 'quiz_bot.db'

config = Config()