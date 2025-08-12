import asyncio
import logging
from aiogram import Dispatcher

from bot.database.database import Database
from bot.handlers.callbacks import router_callbacks
from bot.handlers.commands import commands_router
from bot.handlers.sender import check_and_notify
from config import client, bot

"""ЗАМЕНИТЬ ТОКЕН БОТА"""

async def main():
    logging.basicConfig(level=logging.INFO)

    db = Database()
    dp = Dispatcher()

    dp.include_routers(commands_router, router_callbacks)

    asyncio.create_task(check_and_notify(bot))
    await client.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
