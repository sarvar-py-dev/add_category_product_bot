from aiogram import Router

from bot.handlers import main_router
from bot.utils import utils_router
from bot.pagination import pagination_router

start_router = Router()

start_router.include_routers(
    main_router,
    utils_router,
    pagination_router,
)
