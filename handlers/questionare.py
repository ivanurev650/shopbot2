from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import database.shop as shop_db
import database.add as add_db
import database.get as get_db
from decimal import Decimal, InvalidOperation

from database.shop import buy_products
from utils.states import Form
router=Router()

@router.message(Command('register'))
async def register(message: Message,state: FSMContext):
    await state.set_state(Form.username)
    await message.answer('Введите ваше имя')

@router.message(Form.username,F.text)
async def username(message: Message,state: FSMContext):




    username=await get_db.get_user(tg_id=message.from_user.id)
    if username:
        await message.answer('Вы уже зарегистрированы!')
        await state.clear()
        return
    await state.update_data(username=message.text)
    data = await state.get_data()


    await add_db.add_user(username=data['username'],tg_id=message.from_user.id)
    username = await get_db.get_user(tg_id=message.from_user.id)
    await message.answer(f"""Ваше имя: {username['username']},
     ваш tg_id: {username["tg_id"]}""")
    await state.clear()





@router.message(Command('order'))
async def order(message: Message,state: FSMContext):
    username = await get_db.get_user(tg_id=message.from_user.id)
    if not username:
        await message.answer('Вы не зарегистрированы!')
        await state.clear()
        return
    await state.set_state(Form.order_product_name)
    await message.answer('Введите имя товара')

@router.message(Form.order_product_name,F.text)
async def order_product_name(message: Message,state: FSMContext):
    await state.update_data(name=(message.text))
    await state.set_state(Form.amount)
    await message.answer("Введите количество товара")


@router.message(Form.amount,F.text)
async def amount(message: Message,state: FSMContext):
    try:
        amount=int(message.text)
    except ValueError:
        await message.answer('Введите число')
        return
    await state.update_data(amount=amount)
    data=await get_db.get_user(tg_id=message.from_user.id)
    user_id=data['id']
    result= await state.get_data()

    await buy_products(user_id)
    await state.clear()







