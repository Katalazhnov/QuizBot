from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать в квиз!",
        reply_markup=get_main_keyboard()
    )