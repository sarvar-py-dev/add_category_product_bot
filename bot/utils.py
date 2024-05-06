from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.config import database
from aiogram import Router
import requests
from aiogram.types import Message

utils_router = Router()


# make url if you want get any photos url

def make_url(message: Message):
    with open('for_url.jpg', 'rb') as f:
        response = requests.post('https://telegra.ph/upload', files={'file': f})
        data = response.json()
        url = "https://telegra.ph" + data[0].get('src').replace(r"\\", '')
    return url


def reply_categories():
    rkb = ReplyKeyboardBuilder()
    for category in database['category'].keys():
        rkb.add(KeyboardButton(text=category))
    rkb.adjust(3, repeat=True)
    return rkb
