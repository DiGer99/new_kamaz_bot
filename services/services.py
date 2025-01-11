from datetime import datetime, timedelta
import database.requests as rq


# Нажатие на кнопку "Сегодня"
async def today_press_button():
    today_date = datetime.now() # получаем сегодняшнюю дату 
    now_day_month = today_date.strftime("%d.%m") # переводим дату в формат 01.12 - день месяц
    if now_day_month.startswith("0"): # если день начинается с "0" удаляем его, чтобы постоянно не прописывать его при изменение расписания
        now_day_month.removeprefix("0")
    schedule = str(await rq.get_schedule()).split("\n\n") # разделяем расписание по двум переводам строки
    today_schedule = None
    for i in schedule: # пробегаем циклом по датам, если совпала с сегодняшней, то присваиваем расписание на день переменной "today_schedule"
        if i.strip().startswith(now_day_month):
            today_schedule = i
            break
    if today_schedule:
        return today_schedule
    else:
        return "На сегодня нет расписания!"


# Нажатие на кнопку "Завтра"
async def tommorow_press_button():
    today_date = datetime.now()
    tommorow_date = today_date + timedelta(days=1)
    stroka_tommorow_date = tommorow_date.strftime("%d.%m")
    if stroka_tommorow_date.startswith("0"): # если день начинается с "0" удаляем его, чтобы постоянно не прописывать его при изменение расписания
        stroka_tommorow_date.removeprefix("0")
    schedule = str(await rq.get_schedule()).split("\n\n") # разделяем расписание по двум переводам строки
    tommorow_schedule = None
    for i in schedule:
        if i.strip().startswith(stroka_tommorow_date):
            tommorow_schedule = i
            break
    if tommorow_schedule:
        return tommorow_schedule
    else:
        return "На завтра нет расписания!"