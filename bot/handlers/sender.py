import asyncio
from datetime import timedelta
from bot.database.database import Database
from bot.handlers.support import display_period, period_remain
from bot.keyboards import main_menu_keyboard
from aiogram import Bot

PERIOD_MAP = {
    "everyday": timedelta(days=1),
    "weekly": timedelta(weeks=1),
    "monthly": timedelta(days=30),
    "on_the_date": None,
}

db = Database()


async def send_notification(bot: Bot, user_id: int, event):
    """Отправляемое уведомление"""
    event_name, event_date, description, event_at, period = event
    text = (
        f"\u23F0 Напоминание о событии!\n"
        f"<b>Название:</b> {event_name}\n"
        f"<b>Дата:</b> {event_date}\n"
        f"<b>Описание:</b> {description}\n"
        f"<b>Период:</b> {period_remain(period)}\n"
        f"<b>Осталось:</b> {display_period(period, event_date)}"
    )
    await bot.send_message(user_id, text, reply_markup=main_menu_keyboard(), parse_mode="HTML")


async def check_and_notify(bot: Bot, interval_sec: int = 3600):  # заменить на 3600
    while True:
        users = db.conn.execute("SELECT user_id FROM users").fetchall()
        # now = datetime.now()

        for (user_id,) in users:
            events = db.get_events(user_id)
            print(events)
            for event in events:
                await send_notification(bot, user_id, event)
        await asyncio.sleep(interval_sec)
