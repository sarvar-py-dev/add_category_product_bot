from aiogram import Router, F
from aiogram.types import InlineKeyboardButton, URLInputFile, Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder

from redis_dict import RedisDict

pagination_router = Router()

database = RedisDict('products')

product_db: list = database['products']


def make_inline_button(product):
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text='⬅', callback_data=str(int(product_db.index(product)) - 1)),
        InlineKeyboardButton(text=f"{product_db.index(product) + 1}/{len(product_db)}",
                             callback_data=f"current_{product_db.index(product)}"),
        InlineKeyboardButton(text='➡', callback_data=str(int(product_db.index(product)) + 1))
    )
    return ikb.as_markup()


@pagination_router.message(F.text == 'Produktlarni korish')
async def pagination_start(message: Message):
    if product_db:
        product = product_db[0]
        text = f"<b>{product['name']}</b>\n\n{product['description']}"
        img = product['image']
        await message.answer_photo(img, caption=text, reply_markup=make_inline_button(product))
    else:
        await message.answer('There are no products in database')


@pagination_router.callback_query(F.data.func(lambda data: data.isdigit() or data.startswith('current_')))
async def start(callback: CallbackQuery):
    if callback.data.startswith('current_'):
        current_product_id = callback.data.split('_')[-1]
        text = current_product_id
        await callback.answer(str(int(text) + 1), show_alert=True)

    elif callback.data.isdigit():
        if int(callback.data) < 0 or len(product_db) <= int(callback.data):
            await callback.answer('Limit', show_alert=True)

        else:
            product = product_db[int(callback.data)]
            text = f"<b>{product['name']}</b>\n\n{product['description']}"
            img = product['image']
            media = InputMediaPhoto(media=img, caption=text)
            await callback.message.edit_media(media, reply_markup=make_inline_button(product))
