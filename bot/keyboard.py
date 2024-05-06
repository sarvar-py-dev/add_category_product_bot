from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardBuilder

admin_panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Product qoshish'), KeyboardButton(text='Category qoshish')]],
    resize_keyboard=True)

user_panel_keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Produktlarni korish')]],
    resize_keyboard=True)
