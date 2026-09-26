from aiogram import F,  Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import  CommandStart

from database.shop import buy_products
from keyboards.reply import main,profile

from database import get as get_db
from database import add as add_db
from database import shop as shop_db


router = Router()


async def success(message: Message):
    await message.answer('Запрос выполнен')


async def error(message: Message):
    await message.answer("Ошибка")


@router.message(CommandStart())
async def start(message: Message):
    if not await get_db.get_user(message.from_user.id):
        await add_db.add_user(message.from_user.first_name, message.from_user.id)

        await message.answer("Вы зарегистрированы!", reply_markup=main)
    else:
        await message.answer('С возвращением!', reply_markup=main)




@router.message(F.text.lower() == 'всего потрачено')
async def spend_money(message: Message):
    user = await get_db.get_user(message.from_user.id)
    if not user:
        await message.answer("Вы не зарегистрированы")
        return

    user_id = user['id']
    money = await shop_db.spend_money(user_id)
    await message.answer(str(money))




@router.message(F.text.lower() == 'больше двух заказов')
async def more_than_two(message: Message):
    user = await get_db.get_user(message.from_user.id)
    if not user:
        await message.answer("Вы не зарегистрированы")
        return
    user_id = user['id']
    result=await get_db.get_more_than_two(user_id)
    await message.answer(str(result))




@router.message(F.text.lower() == 'все товары')
async def get_all_products(message: Message):
    result=await get_db.get_products()
    await message.answer(str(result))

@router.message(F.text == 'Профиль')
async def my_profile(message: Message):
    await message.answer("Ваш профиль",reply_markup=profile)
@router.message(F.text=='Назад')
async def to_main(message:Message):
    await message.answer('Главное меню:',reply_markup=main)
@router.message(F.text == 'Мои заказы')
async def user_orders(message: Message):
    user = await get_db.get_user(message.from_user.id)
    if not user:
        return
    user_id = user['id']
    orders=await get_db.get_orders(user_id)
    if not orders:
        await message.answer("Вы ничего не заказали")
        return
    text=''
    for order in orders:
        text+=(f'Заказ:{order["id"]},\n'
            f'{order["name"]},\n'
               f'Цена:{order["price"]},\n'
               f'Количество:{order["amount"]}\n\n')
    await message.answer(text)

@router.message(F.text=="Мои данные")
async def my_info(message: Message):
    user = await get_db.get_user(message.from_user.id)
    money=await shop_db.spend_money(user['id'])

    await message.answer(f'''id:{user["id"]},
tg_id:{user["tg_id"]},
username:{user["username"]},
role:{user["role"]},
Всего потрачено:
{money}''',),
@router.callback_query(F.data=='checkout')
async def checkout(callback: CallbackQuery):
    data=await get_db.get_user(callback.from_user.id)
    user_id = data['id']
    order,text=await buy_products(user_id)
    if not order:
        await callback.answer(text)
        return
    await callback.message.edit_text(text)
    await callback.answer()

@router.message(F.text=='Статистика')
async def statistics(message: Message):
    statistics=await get_db.get_statistics()
    await message.answer(f'''Пользователи:{statistics["users"]}
                             Заказов:{statistics["orders"]}
                             Заказано товаров:{statistics["amount"]}  
                             Товаров в каталоге:{statistics["products"]}
                             На складе:{statistics["stock"]}  
                             Выручка:{statistics["total"]}
                             Средний чек:{statistics["average"]}     
                                
                                
                                
                                ''')

