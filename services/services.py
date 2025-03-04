from datetime import datetime, timedelta
import database.requests as rq
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import services.services as serv
import config.config as config


# Нажатие на кнопку "Сегодня"
async def today_press_button():
    today_date = datetime.now() # получаем сегодняшнюю дату 
    now_day_month = today_date.strftime("%d.%m") # переводим дату в формат 01.12 - день месяц
    if now_day_month.startswith("0"): # если день начинается с "0" удаляем его, чтобы постоянно не прописывать его при изменение расписания
        now_day_month = now_day_month.removeprefix("0")
    schedule = (date for date in (await rq.get_schedule()).split("\n\n")) # разделяем расписание по двум переводам строки
    today_schedule = None
    for i in schedule: # пробегаем циклом по датам, если совпала с сегодняшней, то присваиваем расписание на день переменной "today_schedule"
        if i.strip().startswith(now_day_month):
            today_schedule = i
            break
    if today_schedule:
        schedule_html = today_schedule.split("\n", 1)
        schedule_html[0] = "<u><i><b>" + schedule_html[0].strip() + "</b></i></u>"
        today_schedule = "\n".join(schedule_html)
        return today_schedule
    else:
        return "На сегодня нет расписания!"


# Нажатие на кнопку "Завтра"
async def tommorow_press_button():
    today_date = datetime.now()
    tommorow_date = today_date + timedelta(days=1)
    stroka_tommorow_date = tommorow_date.strftime("%d.%m")
    if stroka_tommorow_date.startswith("0"): # если день начинается с "0" удаляем его, чтобы постоянно не прописывать его при изменение расписания
        stroka_tommorow_date = stroka_tommorow_date.removeprefix("0")
    schedule = (date for date in (await rq.get_schedule()).split("\n\n")) # разделяем расписание по двум переводам строки
    tommorow_schedule = None
    for i in schedule:
        if i.strip().startswith(stroka_tommorow_date):
            tommorow_schedule = i
            break
    if tommorow_schedule:
        schedule_html = tommorow_schedule.split("\n", 1)
        schedule_html[0] = "<u><i><b>" + schedule_html[0].strip() + "</b></i></u>"
        tommorow_schedule = "\n".join(schedule_html)
        return tommorow_schedule
    else:
        return "На завтра нет расписания!"
    

async def scheduler_tommorow_button(bot: Bot):
    users_scalars = await rq.newslatter()
    users = [user.tg_id for user in users_scalars]
    res = await tommorow_press_button()
    for user in users:
        try:
            await bot.send_message(user, text=f"<b>Расписание на завтра:</b>\n\n{res}")
        except TelegramBadRequest:
            continue


async def scheduler_today_button(bot: Bot):
    res = await today_press_button()
    
    if res == "На сегодня нет расписания!":
        pass

    elif len(res.split("\n", 1)) > 1:
        if res.split("\n", 1)[1].strip().lower() == "выходной":
            pass

    
        else:
            users_scalars = await rq.newslatter()
            users = [user.tg_id for user in users_scalars]
            for user in users:
                try:
                    await bot.send_message(user, text=f"<b>Расписание на сегодня:</b>\n\n{res}")
                except TelegramBadRequest:
                    continue


# добавляем к дате html разметку для расипсания на неделю
def add_html(lst_schedule: list) -> list:
    return [("<u><i><b>" + i.split("\n", 1)[0] + "</b></i></u>" + "\n" + i.split("\n", 1)[1]) for i in lst_schedule] # разбиваем расписание по датам и каждую дату разбиваем по переводу строки, конкатенируем к дате html разметку и конкатенируем к обратному виду