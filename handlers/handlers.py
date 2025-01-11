from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
import database.requests as rq
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, StateFilter
import logging
from keyboards.keyboards import create_inline_keyboard, create_reply_keyboard, head_reply_keyboard
from config.config import load_config
from fsm.fsm import AdminChangeSchedule
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import services.services as serv

handler_router = Router()

logger = logging.getLogger(__name__)


# обработка команды /start
@handler_router.message(CommandStart())
async def process_press_start_command(message: Message, scheduler: AsyncIOScheduler, bot: Bot):
    await rq.set_user(tg_id=message.from_user.id, full_name=f"{message.from_user.first_name} {message.from_user.last_name}")
    await message.answer(f"Приветствую {message.from_user.first_name}!\nЭто официальный бот <b>ФК Камаз!!</b>\n\n"
                         f"Я отправлю тебе расписание! Выбери, чтобы ты хотел посмотреть...",
                         reply_markup=head_reply_keyboard)
    if str(message.from_user.id) in load_config().admins.ids:
        try:
            await rq.get_schedule()
        except AttributeError:
            await rq.set_schedule()
    scheduler.add_job(bot.send_message, "cron", hour=21,
                      args=(message.chat.id, f"<b>Расписание на завтра:</b>\n\n{await serv.tommorow_press_button()}"))


# обработка команды /change_schedule для админов и переход в состояние AdminChangeSchedule.wait_schedule
@handler_router.message(Command("change_schedule"))
async def change_schedule_admin_command_press(message: Message, state: FSMContext):
    config = load_config()
    admins_list = config.admins.ids
    if str(message.from_user.id) in admins_list:
        await message.answer("Введите новое расписание...",
                             reply_markup=create_inline_keyboard(1, cancel="Отмена"))
        await state.set_state(AdminChangeSchedule.wait_schedule)


# Ловим состояние и кнопку колбэк дату отмена - cancel
@handler_router.callback_query(F.data == "cancel", StateFilter(AdminChangeSchedule.wait_schedule))
async def process_cancell_inline_button_press_changed_schedule(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("Редактирование расписания отменено")


# Ловим состояние AdminChangeSchedule.wait_schedule и обновляем расписание через сообщение
@handler_router.message(StateFilter(AdminChangeSchedule.wait_schedule))
async def change_schedule_process(message: Message, state: FSMContext):
    await rq.update_schedule(schedule=message.text)
    await message.answer("Расписание изменено!")
    await state.clear()



# Обработка команды /help
@handler_router.message(Command("help"))
async def process_help_command_press(message: Message):
    if str(message.from_user.id) in load_config().admins.ids:
        await message.answer(text="Для изменения расписания воспользуйтесь командой /change_schedule",
                             reply_markup=head_reply_keyboard)
    else:    
        await message.answer(text="Бот помогает ориентироваться в расписание, нажми кнопку на клавиатуре внизу...",
                            reply_markup=head_reply_keyboard)
    

# Ловим кнопку "Расписание на неделю" и выводим "full_schedule" через requests
@handler_router.message(F.text == "📝 Расписание на неделю")
async def process_schedule_week_button_press(message: Message):
    await message.answer(text=f"<b>Расписание на неделю:</b>\n\n{await rq.get_schedule()}")


# Обработка кнопки "Сегодня" 
@handler_router.message(F.text == "🔖 Сегодня")
async def process_button_today_press(message: Message):
    await message.answer(text=f"<b>Расписание на сегодня:</b>\n{await serv.today_press_button()}")


# Обработка кнопки "Завтра"
@handler_router.message(F.text == "🔜 Завтра")
async def process_button_press_tommorow(message: Message):
    await message.answer(text=f"<b>Расписание на завтра:</b>\n{await serv.tommorow_press_button()}")


# для инлайн кнопок разделить расписание по \n\n и потом разделить каждый элемент по первому пробелу и записать в кнопки 
@handler_router.message(F.text == "📅 Расписание по датам")
async def process_button_schedule_dates_press(message: Message):
    schedule = str(await rq.get_schedule())
    dates = [i.strip().split("\n", 1)[0].strip() for i in schedule.split("\n\n")]
    await message.answer(text="Выберите дату...",
                         reply_markup=create_inline_keyboard(3, *dates))
    

# отлавливаем колбэк на дату
@handler_router.callback_query(F.data.replace(".", '').isdigit())
async def process_callback_button_date_press(calback: CallbackQuery):
    schedule = await rq.get_schedule() # получаем расписание
    await calback.message.edit_text(text=[i for i in schedule.split("\n\n") if i.strip().startswith(calback.data)][0]) # нулевой индекс из найденных дней по дате
    await calback.answer()