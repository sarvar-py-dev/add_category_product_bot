from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, \
    CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from uuid import uuid4

import bot.keyboard as kb
from bot.config import ADMIN_LIST, database
from bot.utils import reply_categories

main_router = Router()

save_product = {}


class FormState(StatesGroup):
    category = State()
    product_name = State()
    product_price = State()
    product_quantity = State()
    product_image = State()
    product_description = State()
    product_category = State()
    product_view = State()
    product_inline = State()
    product_delete = State()


@main_router.message(F.from_user.id.in_(ADMIN_LIST), Command(commands='view_products'))
async def products_for_admin(message: Message, state: FSMContext):
    if database['category']:
        rkb = reply_categories()
        await state.set_state(FormState.product_view)
        await message.answer('Categorylar: ', reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_view)
async def products_for_admin(message: Message, state: FSMContext):
    products_for_view = database['products']
    if message.text in database['category']:
        ikb = InlineKeyboardBuilder()
        for product in products_for_view:
            if product['category'] == message.text:
                ikb.add(InlineKeyboardButton(text=product['name'], callback_data=product['id']))
        if ikb:
            ikb.adjust(3, repeat=True)
            ikb.row(InlineKeyboardButton(text='❌', callback_data='x'),
                    InlineKeyboardButton(text='Search 🔍', callback_data='search'))
            await message.answer('Productlar: ', reply_markup=ikb.as_markup())
            await state.set_state(FormState.product_inline)
        else:
            await message.answer('Bu category ichida productlar yoq')
    else:
        await message.answer('Category topilmadi')


@main_router.callback_query(F.from_user.id.in_(ADMIN_LIST), FormState.product_inline)
async def product(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'x' or callback.data == 'search':
        await callback.message.delete()
        await callback.message.answer('tanlang', reply_markup=kb.admin_panel_keyboard)
    else:
        db_product: dict = [product_ for product_ in database['products'] if product_['id'] == callback.data][0]
        msg = f'Name: <b>{db_product["name"]}</b>\nPrice: {db_product["price"]}\nQuantity: {db_product["quantity"]}\nDescription: {db_product["description"]}\nCategory: {db_product["category"]}'
        await callback.message.delete()
        ikb = InlineKeyboardBuilder()
        ikb.row(InlineKeyboardButton(text='Delete product', callback_data=db_product['id']),
                InlineKeyboardButton(text='No', callback_data='no'))
        await callback.message.answer_photo(db_product['image'], caption=msg, parse_mode=ParseMode.HTML,
                                            reply_markup=ikb.as_markup())
        await state.set_state(FormState.product_delete)


@main_router.callback_query(F.from_user.id.in_(ADMIN_LIST), FormState.product_delete)
async def delete_product(callback: CallbackQuery):
    if callback.data.startswith('no'):
        await callback.message.edit_reply_markup()
        await callback.message.answer('tanlang', reply_markup=kb.admin_panel_keyboard)
        return
    product_ = [i for i in database['products'] if i['id'] == callback.data][0]
    del_prod = database['products']
    del_cate = database['category'][product_['category']]

    del_cate.remove(product_['id'])
    del_prod.remove(product_)

    database['products'] = del_prod
    database['category'][product_['category']] = del_cate
    await callback.message.delete()
    await callback.message.answer('Product deleted', reply_markup=kb.admin_panel_keyboard)


@main_router.message((F.from_user.id.in_(ADMIN_LIST)) & (F.text == 'Category qoshish'))
async def add_category(message: Message, state: FSMContext):
    await state.set_state(FormState.category)
    await message.answer('Category nomini kiriting', reply_markup=ReplyKeyboardRemove())


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.category)
async def add_category(message: Message, state: FSMContext):
    category = database['category']
    category[message.text] = []
    database['category'] = category
    await state.clear()
    await message.answer('Category qoshildi', reply_markup=kb.admin_panel_keyboard())


@main_router.message((F.from_user.id.in_(ADMIN_LIST)) & (F.text == 'Product qoshish'))
async def add_product(message: Message, state: FSMContext):
    save_product = {}
    if not database['category']:
        await message.answer('Avval category qoshing')
        return
    await state.set_state(FormState.product_name)
    await message.answer('Product nomini kiriting', reply_markup=ReplyKeyboardRemove())


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_name)
async def add_product(message: Message, state: FSMContext):
    save_product['name'] = message.text
    await state.set_state(FormState.product_price)
    await message.answer('Product narxini kiriting: ')


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_price)
async def add_product(message: Message, state: FSMContext):
    save_product['price'] = message.text
    await state.set_state(FormState.product_quantity)
    await message.answer('Product sonini kiriting: ')


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_quantity)
async def add_product(message: Message, state: FSMContext):
    save_product['quantity'] = message.text
    await state.set_state(FormState.product_image)
    await message.answer('Product rasmini kiriting: ')


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_image)
async def add_product(message: Message, state: FSMContext):
    save_product['image'] = message.photo[0].file_id
    # products['image_for_users'] = make_url(message)
    await state.set_state(FormState.product_description)
    await message.answer('Product malumotini kiriting: ')


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_description)
async def add_product(message: Message, state: FSMContext):
    save_product['description'] = message.text
    rkb = reply_categories()
    await state.set_state(FormState.product_category)
    await message.answer('Category ni tanlang', reply_markup=rkb.as_markup(resize_keyboard=True))


@main_router.message(F.from_user.id.in_(ADMIN_LIST), FormState.product_category)
async def add_product(message: Message, state: FSMContext):
    if message.text not in database['category']:
        await message.answer('Categoryda hatolik')
        return
    save_product['category'] = message.text
    product_id = str(uuid4())
    save_product['id'] = product_id
    products_: list = database['products']
    products_.append(save_product)

    categories: dict[str, list] = database['category']
    categories[message.text].append(product_id)
    database['products'] = products_
    database['category'] = categories
    await state.clear()
    await message.answer('Saqlandi', reply_markup=kb.admin_panel_keyboard)


@main_router.message(F.from_user.id.in_(ADMIN_LIST), CommandStart())
async def start_for_admin(message: Message):
    await message.answer('Tanlang', reply_markup=kb.admin_panel_keyboard)


@main_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Category ni tanlang', reply_markup=kb.user_panel_keyboard)


class IsCategoryFilter(Filter):

    async def __call__(self, message: Message):
        categories: dict = database.get('category')
        for category in categories.keys():
            if message.text == category:
                return True
        return False


def get_products(category_name: str):
    products_ = []
    for product_ in database['products']:
        if product_['category'] == category_name:
            products_.append(product)
    return products_


@main_router.message(F.text == 'ortga')
async def ortga(message: Message):
    if str(message.from_user.id) in ADMIN_LIST:
        await message.answer('Tanlang...', reply_markup=kb.admin_panel_keyboard)
    else:
        await message.answer('Tanlang...', reply_markup=kb.user_panel_keyboard)


@main_router.message(IsCategoryFilter())
async def start(message: Message):
    _products = get_products(message.text)
    await message.answer(f'{message.text} tanlandi')
