from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_quiz_keyboard(answer_options, correct_option_index):
    builder = InlineKeyboardBuilder()
    correct_answer = answer_options[correct_option_index]

    for option in answer_options:
        builder.add(InlineKeyboardButton(
            text=option,
            callback_data="right_answer" if option == correct_answer else "wrong_answer"
        ))

    builder.adjust(1)
    return builder.as_markup()