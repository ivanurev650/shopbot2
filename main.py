from aiogram.client.default import DefaultBotProperties

import asyncio

from aiogram import Bot, Dispatcher
from config_reader import config
from database.add import create_table_users, create_table_orders, create_table_products, create_table_cart
from handlers import user,questionare,admin,catalog,cart


async def main():
    bot = Bot(config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()


    dp.include_routers(
user.router,
        questionare.router,
        admin.router,
        catalog.router,
        cart.router,


    )

    await create_table_users()
    await create_table_orders()
    await create_table_products()
    await create_table_cart()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())