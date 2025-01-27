from aiogram.fsm.state import State, StatesGroup


class AdminChangeSchedule(StatesGroup):
    wait_schedule = State()

class AdminNewsLetter(StatesGroup):
    wait_newsletter = State()