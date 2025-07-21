from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.database import Database
from bot.handlers.support import period_remain
from bot.keyboards import main_menu_keyboard
from bot.logs import logger

commands_router = Router()
db = Database()


@commands_router.message(Command("start"))
async def start(message: Message):
    """
    Приветствие и отображение клавиатуры.
    Добавление пользователя в базу
    """
    user_id = message.from_user.id
    username = message.from_user.username
    db.add_user(user_id, username)
    logger.info(f"User {username} добавлен в БД")

    try:
        events = db.get_events(user_id)
        events_text = "\n\n".join(
            f"Название: {e[0]}\nДата: {e[1]}\nОписание: {e[2]}\nСоздано: {period_remain(e[3])}\nПериод: {e[4]}"
            for e in events
        )
    except Exception as e:
        events_text = None
        logger.info(f"Ошибка при получении 'get_events': {e}")

    await message.answer(
        f"Привет!\n\n"
        f"Данный бот предназначен для отслеживания важных событий/дедлайнов.\n"
        f"Сохраненные события:\n{events_text}\n"
        f"\nВведи дату, укажи событие и задай частоту оповещений(обратный отсчет).\n",
        reply_markup=main_menu_keyboard(),
        parse_mode="HTML"
    )


@commands_router.message(Command("help"))
async def help_command(message: Message):
    """
    Краткая справка по использованию бота.
    """
    await message.answer(
        "Я бот для сохранения событий"
    )
