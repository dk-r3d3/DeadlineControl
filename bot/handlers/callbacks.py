from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.database.database import Database
from bot.form import Form
from bot.handlers.support import date_validation, menu
from bot.keyboards import cancel, menu_period, main_menu_keyboard
from bot.handlers.deadline import DeadLine

router_callbacks = Router()
db = Database()


@router_callbacks.callback_query(F.data == "add_deadline")
async def add_deadline(cb: CallbackQuery, state: FSMContext):
    """Добавить событие"""
    await cb.answer("Создание события... (добавить эмодзи")
    await cb.message.answer("Введи название события (эмодзи)", reply_markup=cancel())
    await state.set_state(Form.waiting_deadline_name)


@router_callbacks.message(Form.waiting_deadline_name)
async def process_add_deadline_name(message: Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer("Введите дату события (ДД.ММ.ГГГГ):", reply_markup=cancel())
    await state.set_state(Form.waiting_deadline_datetime)


@router_callbacks.message(Form.waiting_deadline_datetime)
async def process_add_deadline_date(message: Message, state: FSMContext):
    try:
        if date_validation(message.text):
            await state.update_data(event_date=message.text)
            await message.answer("Введите описание события:", reply_markup=cancel())
            await state.set_state(Form.waiting_deadline_description)
        else:
            await message.answer("Ты ввел дату, которая уже в прошлом. Пробуй еще раз.")
            await state.set_state(Form.waiting_deadline_datetime)
    except Exception as e:
        await message.answer("Введите дату в соответствии с образцом - (ДД.ММ.ГГГГ)")
        await state.set_state(Form.waiting_deadline_datetime)


@router_callbacks.message(Form.waiting_deadline_description)
async def process_add_deadline_description(message: Message, state: FSMContext):
    await state.update_data(event_description=message.text)
    await message.answer("Выберите частоту уведомлений:", reply_markup=menu_period())
    await state.set_state(Form.waiting_deadline_period)


@router_callbacks.callback_query(Form.waiting_deadline_period)
async def process_add_deadline_period(cb: CallbackQuery, state: FSMContext):
    user_id = cb.from_user.id
    user_data = await state.get_data()
    deadline = DeadLine(
        event_name=user_data["event_name"],
        event_date=user_data["event_date"],
        description=user_data["event_description"],
        period=cb.data
    )
    # Сохраняем в БД
    db.add_event(user_id, deadline.event_name, deadline.event_date, deadline.description, deadline.period)
    await cb.message.answer("Событие добавлено!")

    events = db.get_events(user_id)
    await cb.message.answer(f"Сохраненные события:\n{menu(events)}\n"
                            f"\nВведи дату, укажи событие и задай частоту оповещений(обратный отсчет).\n",
                            reply_markup=main_menu_keyboard())
    await state.clear()


@router_callbacks.callback_query(F.data == "delete_deadline")
async def delete_deadline(cb: CallbackQuery, state: FSMContext):
    """Удалить событие"""
    await cb.message.answer("Введи название события, которое хочешь удалить", reply_markup=cancel())
    await state.set_state(Form.waiting_name_from_delete)


@router_callbacks.message(Form.waiting_name_from_delete)
async def process_delete_deadline(message: Message, state: FSMContext):
    user_id = message.from_user.id
    event = message.text

    if db.delete_event(user_id, event):
        await message.answer("Событие удалено!")
    else:
        await message.answer("Данного события не существует, попробуй еще раз")

    events = db.get_events(user_id)
    await message.answer(f"Сохраненные события:\n{menu(events)}\n"
                         f"\nВведи дату, укажи событие и задай частоту оповещений(обратный отсчет).\n",
                         reply_markup=main_menu_keyboard())
    await state.clear()
