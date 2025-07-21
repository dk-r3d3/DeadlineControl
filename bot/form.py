from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):  # класс для хранения состояний
    waiting_deadline_name = State()
    waiting_deadline_description = State()
    waiting_deadline_datetime = State()
    waiting_deadline_period = State()
    waiting_name_from_delete = State()
