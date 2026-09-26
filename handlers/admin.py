from decimal import Decimal, InvalidOperation

from aiogram import F,  Router
from aiogram.fsm import state

from utils.states import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command


from database import get as get_db
from database import add as add_db
from database import shop as shop_db

from filters.isadmin import IsAdmin


router = Router()




@router.message(IsAdmin(),
                Command('product'))
async def product(message: Message, state: FSMContext):

    await state.set_state(Form.product_name)
    await message.answer("Введите имя товара")#,reply_markup)?

@router.message(Form.product_name,F.text)
async def name(message: Message,state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.stock)
    await message.answer('Введите количество товара')

@router.message(Form.stock,F.text)
async def stock(message: Message,state: FSMContext):
    try:
        stock=int(message.text)
    except ValueError:
        await message.answer('Введите число!')
        return
    await state.update_data(stock=stock)
    await state.set_state(Form.price)
    await message.answer('Введите цену товара')

@router.message(Form.price,F.text)
async def price(message: Message,state: FSMContext):
    try:
        price=Decimal(message.text)
    except InvalidOperation:
        await message.answer('Введите число')
        return
    await state.update_data(price=price)
    await message.answer('Настройка товара завершена')
    data=await state.get_data()
    name=data['name']
    if name:
        await message.answer("Такой товар уже существует")
        await state.clear()
        return
    await add_db.add_product(
        name, stock=data['stock'],
                         price=str(data['price']))

    product = await get_db.get_product_by_name(name)

    await message.answer(f'''Название: {product['name']}
Цена:{product['price']}
Остаток: {product['stock']}''')
    await state.clear()
    await message.answer('Регистрация товара завершена')


@router.message(IsAdmin(),
                F.text.lower() == 'обновить товар')
async def update_product(message: Message, state: FSMContext):


    await state.set_state(Form.update_product_name)
    await message.answer('Введите название товара')

@router.message(Form.update_product_name,F.text)
async def update_product_name(message: Message, state: FSMContext):
    product=await get_db.get_product_by_name(message.text)
    if not product:
        await message.answer('Товар не найден')
        await state.clear()
        return
    await state.update_data(name=message.text)
    await state.set_state(Form.update_product_price)
    await message.answer('Введите новую цену')

@router.message(Form.update_product_price,F.text)
async def update_product_price(message: Message, state: FSMContext):
    try:
        price=Decimal(message.text)
    except InvalidOperation:
        await message.answer('Введите число')
        return
    await state.update_data(price=price)
    await state.set_state(Form.update_product_stock)
    await message.answer('Введите новый остаток')


@router.message(Form.update_product_stock,F.text)
async def update_product_stock(message: Message, state: FSMContext):
    try:
        stock=int(message.text)
    except ValueError:
        await message.answer('Введите число')
        return

    data = await state.get_data()
    name = data['name']
    price = data['price']

    updated=await shop_db.update_product(price,stock,name)
    if updated:
        await message.answer('Товар обновлен')
    else:
        await message.answer("Товар не обновлен")

    await state.clear()


@router.message(IsAdmin(),
                F.text.lower() == 'удалить заказ')
async def delete_order_start(message: Message, state: FSMContext):
    await state.set_state(Form.delete_order_id)
    await message.answer('Введите id заказа')

@router.message(Form.delete_order_id,F.text)
async def delete_order_process(message: Message, state: FSMContext):
    try:
        order_id=int(message.text)
    except ValueError:
        await message.answer('Введите число')
        return
    order=await get_db.get_order(order_id)
    if not order:
        await message.answer('Заказ не найден')
        await state.clear()
        return
@router.message(IsAdmin(),
                F.text=="Все заказы")
async def all_orders(message: Message, state: FSMContext):
    await state.set_state(Form.user_id)
    await message.answer('Введите user_id пользователя')
@router.message(IsAdmin(),
     Form.user_id           )

async def all_orders_process(message: Message,state: FSMContext):
    user_id=int(message.text)
    text=''

    orders=await get_db.get_orders(user_id)
    if not orders:
        return
    for item in orders:
        text+=(f'''№{item["id"]},'''
               f'''{item["name"]},'''
               f'''цена:{item["price"]},'''
               f'''остаток:{item["amount"]}\n''')
    await message.answer(text)
    await state.clear()
    return
