from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from llm.parser import parse_text_to_command
from db.queries import run_query

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Привет! Отправь мне текстовое сообщение с запросом')


@router.message(F.text)
async def message_handler(message: Message):
    user_text = message.text

    try:
        command = await parse_text_to_command(user_text)
        result = await run_query(command)
        print(f"Получен результат для команды {command}: {result}")
        await message.answer(str(result))

    except Exception as e:
        await message.answer(f"Ошибка: {e}")
