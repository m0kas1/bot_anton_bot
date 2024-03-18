import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram import Router
from handlers import bot_messages
from utils.stateforms import StepsForm
import os
import dotenv

dotenv.load_dotenv()

dp = Dispatcher()
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    dp.message.register(bot_messages.get_start, Command(commands='form'))
    dp.message.register(bot_messages.get_FIO, StepsForm.GET_FIO)
    dp.message.register(bot_messages.get_CHEH, StepsForm.GET_CHEH)
    dp.message.register(bot_messages.get_PODRASDELENIE, StepsForm.GET_PODRASDELENIE)
    dp.message.register(bot_messages.get_ULUCHENIE, StepsForm.GET_ULUCHENIE)
    dp.message.register(bot_messages.get_PREDLOSHENIE, StepsForm.GET_PREDLOSHENIE)
    dp.message.register(bot_messages.get_PROBLEMA, StepsForm.GET_PROBLEMA)
    dp.message.register(bot_messages.get_PHOTO_1, StepsForm.GET_PHOTO_1)
    dp.message.register(bot_messages.get_RESHENIE, StepsForm.GET_RESHENIE)
    dp.message.register(bot_messages.get_PHOTO_2, StepsForm.GET_PHOTO_2)
    dp.message.register(bot_messages.get_VIBER, StepsForm.GET_vibor)
    dp.include_routers(
        bot_messages.router,
        # user_messages.router
    )
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
    await bot.delete_webhook(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())