from aiogram import Router, types, F
from database.connection import update_quiz_index, get_quiz_index, save_quiz_result
from quiz.data import quiz_data
from keyboards.inline import generate_quiz_keyboard

router = Router()

# Добавим словарь для отслеживания правильных ответов
user_scores = {}


@router.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id

    # Увеличиваем счетчик правильных ответов
    if user_id not in user_scores:
        user_scores[user_id] = 0
    user_scores[user_id] += 1

    current_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_index]
    correct_answer = question_data['options'][question_data['correct_option']]

    await callback.message.edit_text(
        f"❓ {question_data['question']}\n\n"
        f"✅ Вы ответили правильно: {correct_answer}"
    )
    await callback.answer()

    next_index = current_index + 1

    if next_index < len(quiz_data):
        await update_quiz_index(user_id, next_index)
        question_data = quiz_data[next_index]
        kb = generate_quiz_keyboard(question_data['options'], question_data['correct_option'])
        await callback.message.answer(question_data['question'], reply_markup=kb)
    else:
        # Сохраняем результат при завершении квиза
        score = user_scores.get(user_id, 0)
        total_questions = len(quiz_data)
        username = callback.from_user.username or callback.from_user.first_name

        await save_quiz_result(user_id, username, score, total_questions)

        # Удаляем временные данные
        if user_id in user_scores:
            del user_scores[user_id]

        await callback.message.answer(
            f"🎉 Поздравляем! Вы завершили квиз!\n"
            f"📊 Ваш результат: {score}/{total_questions} правильных ответов\n\n"
            f"Для просмотра статистики используйте команду /stats"
        )


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    current_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_index]
    correct_answer = question_data['options'][question_data['correct_option']]

    await callback.message.edit_text(
        f"❓ {question_data['question']}\n\n"
        f"❌ Неправильно. Правильный ответ: {correct_answer}"
    )
    await callback.answer()

    next_index = current_index + 1

    if next_index < len(quiz_data):
        await update_quiz_index(user_id, next_index)
        question_data = quiz_data[next_index]
        kb = generate_quiz_keyboard(question_data['options'], question_data['correct_option'])
        await callback.message.answer(question_data['question'], reply_markup=kb)
    else:
        # Сохраняем результат при завершении квиза
        score = user_scores.get(user_id, 0)
        total_questions = len(quiz_data)
        username = callback.from_user.username or callback.from_user.first_name

        await save_quiz_result(user_id, username, score, total_questions)

        # Удаляем временные данные
        if user_id in user_scores:
            del user_scores[user_id]

        await callback.message.answer(
            f"🎉 Вы завершили квиз!\n"
            f"📊 Ваш результат: {score}/{total_questions} правильных ответов\n\n"
            f"Для просмотра статистики используйте команду /stats"
        )