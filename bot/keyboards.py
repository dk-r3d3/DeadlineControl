from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить событие", callback_data="add_deadline")],
            [InlineKeyboardButton(text="Удалить событие", callback_data="delete_deadline")],
            [InlineKeyboardButton(text="Помощь", callback_data="help")],
        ]
    )
    return keyboard


def menu_period():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Ежедневно", callback_data="everyday")],
            [InlineKeyboardButton(text="Еженедельно", callback_data="weekly")],
            [InlineKeyboardButton(text="Ежемесячно", callback_data="monthly")],
            [InlineKeyboardButton(text="В день события", callback_data="on_the_date")],
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
        ]
    )
    return keyboard


def cancel():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Отмена", callback_data="cancel")],
        ]
    )
    return keyboard
