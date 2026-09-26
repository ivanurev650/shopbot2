from aiogram.types import InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.get import get_cart, get_user, get_product_by_name,get_product_by_id, get_products


async def build_catalog(product_id):

    builder = InlineKeyboardBuilder()

    builder.button(
            text="🛒Добавить",
            callback_data=f"add_to_cart:{product_id}"
        )
    builder.button(
        text='Назад',
        callback_data='back_to_catalog'
    )
    builder.adjust(1)
    return builder.as_markup()


async def build_cart(user_id):
    cart = await get_cart(user_id)
    builder = InlineKeyboardBuilder()

    for item in cart:
        builder.button(

            text=f'❌{item['name']}',
            callback_data=f"remove_from_cart:{item['product_id']}"
        )

    return builder.as_markup()
async def build_order():
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Оформить заказ',
        callback_data='checkout'
        )
    return builder.as_markup()



async def build_goods():
    products = await get_products()
    builder = InlineKeyboardBuilder()
    for product in products:

        builder.button(
        text=product['name'],
        callback_data=f'product:{product["id"]}'
    )
    builder.adjust(1)
    return builder.as_markup()