import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import config
from database.connection import init_db
from handlers.start import router as start_router
from handlers.quiz import router as quiz_router
from handlers.common import router as common_router
from handlers.stats import router as stats_router  # Добавляем новый роутер

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    # Инициализация базы данных
    await init_db()

    # Создание объектов бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(quiz_router)
    dp.include_router(common_router)
    dp.include_router(stats_router)  # Регистрируем роутер статистики

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())