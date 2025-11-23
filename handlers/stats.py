from aiogram import Router, types, F
from aiogram.filters import Command
from database.connection import get_user_stats, get_global_stats

router = Router()


@router.message(Command("stats"))
@router.message(F.text == "📊 Статистика")
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id

    # Получаем статистику пользователя
    user_stats = await get_user_stats(user_id)

    stats_text = "📊 Ваша статистика\n\n"

    if user_stats['last_result']:
        score, total, completed_at = user_stats['last_result']
        stats_text += f"📝 Последний результат: {score}/{total}\n"
        stats_text += f"🏆 Лучший результат: {user_stats['best_score']}/{total}\n"
        stats_text += f"🎯 Пройдено квизов: {user_stats['quiz_count']}\n"
    else:
        stats_text += "Вы еще не проходили квиз! Начните с команды /quiz\n"

    await message.answer(stats_text)


@router.message(Command("leaderboard"))
@router.message(F.text == "🏆 Таблица лидеров")
async def cmd_leaderboard(message: types.Message):
    # Получаем глобальную статистику
    global_stats = await get_global_stats()

    leaderboard_text = "🏆 Таблица лидеров\n\n"

    if global_stats['top_players']:
        for i, (username, score) in enumerate(global_stats['top_players'], 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            leaderboard_text += f"{medal} {username}: {score} баллов\n"
    else:
        leaderboard_text += "Пока никто не прошел квиз!\n"

    leaderboard_text += f"\n📈 Всего пройдено квизов: {global_stats['total_quizzes']}"

    await message.answer(leaderboard_text)