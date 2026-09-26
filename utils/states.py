import asyncio
import aiosqlite
import aiogram.fsm
from aiogram.fsm.state import StatesGroup, State
class Form(StatesGroup):
    product_name=State()
    order_product_name=State()
    price=State()
    stock=State()
    username=State()
    user_id=State()
    amount=State()
    product_id=State()



    update_product_name = State()
    update_product_price = State()
    update_product_stock = State()
    delete_order_id = State()