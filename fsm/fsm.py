from aiogram.fsm.state import State, StatesGroup


class AdminChangeSchedule(StatesGroup):
    wait_schedule = State()