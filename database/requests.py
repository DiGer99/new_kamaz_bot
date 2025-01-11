from database.models import async_session
from database.models import User, Schedule
from sqlalchemy import select, update


# декоратор открывающий сессию для каждого запроса
def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner
    

# заводим юзера в таблицу
@connection
async def set_user(session, tg_id, full_name):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, name=full_name))
        await session.commit()


# меняем тру на фолс и наоборот для наопминаний
@connection
async def change_schedule_remind(session, tg_id):
    user = await session.scalar(select(User).where(User.tg_id == tg_id))
    user_remind = user.bool_remind
    await session.execute(update(User).where(User.tg_id == tg_id).values(bool_remind=not user_remind))
    await session.commit()


# добавляем расписание при старте команды
@connection
async def set_schedule(session):
    schedule = await session.scalar(select(Schedule).where(Schedule.id == 1))
    if not schedule:
        session.add(Schedule(full_schedule="Расписание"))
        await session.commit()


# обновляем расписание 
@connection
async def update_schedule(session, schedule):
    await session.execute(update(Schedule).where(Schedule.id == 1).values(full_schedule=schedule))
    await session.commit()



# выводим расписание 
@connection
async def get_schedule(session):
    schedule_row = await session.scalar(select(Schedule).where(Schedule.id == 1))
    return schedule_row.full_schedule

    