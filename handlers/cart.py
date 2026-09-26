from aiogram import F, Dispatcher, Router
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from keyboards.reply import main
from keyboards.inline import build_cart

from database import get as get_db
from database import add as add_db
from database import shop as shop_db
router = Router()
@router.callback_query(F.data.startswith('add_to_cart:'))
async def add_to_cart(callback:CallbackQuery):

    user = await get_db.get_user(callback.from_user.id)
    user_id = user['id']
    product_id = int(callback.data.split(":")[1])
    await add_db.add_product_to_cart(user_id, product_id)

    await callback.answer('Добавлено')

@router.callback_query(F.data.startswith("remove_from_cart:"))
async def remove_from(callback: CallbackQuery):
    user = await get_db.get_user(callback.from_user.id)
    user_id = user['id']
    product_id=int(callback.data.split(":")[1])
    await shop_db.remove_from_cart(user_id, product_id)
    cart = await get_db.get_cart(user_id)
    if not cart:
        await callback.message.edit_text('Корзина пустая')
        await callback.answer()
        return
    text= []
    for item in cart:
        text.append(f'{item["name"]},- {item["quantity"]}шт.')
    cart_text = '\n'.join(text)
    kb= await build_cart(user_id)
    await callback.message.edit_text(cart_text,
                                     reply_markup=kb)


    await callback.answer()


@router.message(F.text == "Корзина")
async def my_cart(message: Message):
    user = await get_db.get_user(message.from_user.id)
    user_id = user['id']
    cart = await get_db.get_cart(user_id)
    kb=await build_cart(user_id)
    text = 'Ваша корзина:'
    if not cart:
        await message.answer('Корзина пуста')
        return

    for item in cart:
        quantity = item["quantity"]
        total = item["total"]
        name=item["name"]
        text += f'''{name},
                    Количество: {quantity},
                    Итого: {total} рублей

'''
    await message.answer(text,reply_markup=kb)