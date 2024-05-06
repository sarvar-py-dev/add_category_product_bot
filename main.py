import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, ReplyKeyboardRemove
from bot.config import TOKEN, database
from bot.routers import start_router

bot = Bot(token=TOKEN)


async def on_startup(dispatcher: Dispatcher):
    if not (database.get('category')):
        database['category'] = {}
    if not database.get('products'):
        database['products'] = []
    command_list = [
        BotCommand(command='/start', description="Botni boshlash"),
        BotCommand(command='/view_products', description="Faqat admin uchun")
    ]
    await bot.set_my_commands(command_list)


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.include_routers(start_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    rkb = ReplyKeyboardRemove()
