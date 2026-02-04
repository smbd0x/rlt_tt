import asyncio
from aiogram import Bot, Dispatcher
from config import Config
from db.base import init_db
from handlers.main import router


async def main():
    await init_db()

    bot = Bot(Config.BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
