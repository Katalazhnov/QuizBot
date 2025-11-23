from aiogram import Router, types, F
from aiogram.filters import Command

from database.connection import update_quiz_index, get_quiz_index
from quiz.data import quiz_data
from keyboards.inline import generate_quiz_keyboard

router = Router()

# Импортируем словарь для сброса
from handlers.common import user_scores


@router.message(F.text == "Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Сбрасываем временные данные при начале нового квиза
    user_id = message.from_user.id
    if user_id in user_scores:
        del user_scores[user_id]

    await message.answer("Давайте начнем квиз!")
    await new_quiz(message)


async def new_quiz(message):
    user_id = message.from_user.id
    await update_quiz_index(user_id, 0)
    await get_question(message, user_id)


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    question_data = quiz_data[current_question_index]

    kb = generate_quiz_keyboard(question_data['options'], question_data['correct_option'])
    await message.answer(question_data['question'], reply_markup=kb)