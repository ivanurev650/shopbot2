from aiogram import F, Dispatcher, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from keyboards.reply import main,profile

from database import get as get_db
from database import add as add_db
from database import shop as shop_db

from keyboards.inline import build_goods, build_catalog
router = Router()


@router.message(F.text=='Каталог')
async def catalog(message: Message):

    kb= await build_goods()
    await message.answer('каталог:',reply_markup=kb)
@router.callback_query(F.data.startswith('product:'))
async def after_catalog(query: CallbackQuery):

    product_id = int(query.data.split(':')[1])
    keyboard = await build_catalog(product_id)
    product=await get_db.get_product_by_id(product_id)
    if not product:
        await query.answer('Товар не найден')
    name=product['name']
    price=product['price']
    stock=product['stock']
    await query.message.edit_text(f'''{name},
    💰цена:{price}
осталось:{stock}''',reply_markup=keyboard)
    await query.answer()
@router.message(F.data=='back_to_catalog')
async def to_catalog(callback: CallbackQuery):
    catalog = await build_goods()
    await callback.message.edit_text('Каталог:',reply_markup=catalog)
    await callback.answer()
