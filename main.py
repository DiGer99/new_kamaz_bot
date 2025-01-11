from aiogram import Dispatcher, Bot
from database.models import db_main
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
from config.config import load_config, Config
import logging
from handlers.handlers import handler_router
from  apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares.middleware import SchedulerMiddleware

loger = logging.getLogger(__name__)


async def main():
    await db_main()
    logging.basicConfig(level=logging.DEBUG,
                        format="[%(asctime)s] #%(levelname)-8s %(filename)s "
                        "%(lineno)d - %(message)s")
    config: Config = load_config()
    
    loger.debug("Bot on.")
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()
    
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_routers(handler_router)
    dp.update.middleware(SchedulerMiddleware(scheduler=scheduler))
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    


if __name__ == "__main__":
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot off.")