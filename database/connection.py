import aiosqlite
from config import config
from datetime import datetime


async def init_db():
    """Инициализация базы данных"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        # Таблица для состояния квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state 
                          (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')

        # Таблица для результатов квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           user_id INTEGER,
                           username TEXT,
                           score INTEGER,
                           total_questions INTEGER,
                           completed_at TIMESTAMP)''')
        await db.commit()


async def update_quiz_index(user_id, index):
    """Обновление индекса вопроса для пользователя"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)',
                         (user_id, index))
        await db.commit()


async def get_quiz_index(user_id):
    """Получение индекса вопроса для пользователя"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            return results[0] if results is not None else 0


async def save_quiz_result(user_id, username, score, total_questions):
    """Сохранение результата прохождения квиза"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        await db.execute('''INSERT INTO quiz_results 
                          (user_id, username, score, total_questions, completed_at) 
                          VALUES (?, ?, ?, ?, ?)''',
                         (user_id, username, score, total_questions, datetime.now()))
        await db.commit()


async def get_user_stats(user_id):
    """Получение статистики пользователя"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        # Последний результат
        async with db.execute('''SELECT score, total_questions, completed_at 
                               FROM quiz_results 
                               WHERE user_id = ? 
                               ORDER BY completed_at DESC LIMIT 1''', (user_id,)) as cursor:
            last_result = await cursor.fetchone()

        # Лучший результат
        async with db.execute('''SELECT MAX(score) 
                               FROM quiz_results 
                               WHERE user_id = ?''', (user_id,)) as cursor:
            best_score = await cursor.fetchone()

        # Количество пройденных квизов
        async with db.execute('''SELECT COUNT(*) 
                               FROM quiz_results 
                               WHERE user_id = ?''', (user_id,)) as cursor:
            quiz_count = await cursor.fetchone()

        return {
            'last_result': last_result,
            'best_score': best_score[0] if best_score and best_score[0] is not None else 0,
            'quiz_count': quiz_count[0] if quiz_count else 0
        }


async def get_global_stats():
    """Получение глобальной статистики"""
    async with aiosqlite.connect(config.DB_NAME) as db:
        # Топ-10 игроков по лучшему результату
        async with db.execute('''SELECT username, MAX(score) as best_score 
                               FROM quiz_results 
                               GROUP BY user_id 
                               ORDER BY best_score DESC 
                               LIMIT 10''') as cursor:
            top_players = await cursor.fetchall()

        # Общее количество пройденных квизов
        async with db.execute('SELECT COUNT(*) FROM quiz_results') as cursor:
            total_quizzes = await cursor.fetchone()

        return {
            'top_players': top_players,
            'total_quizzes': total_quizzes[0] if total_quizzes else 0
        }