from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton,
                           KeyboardButtonPollType,
                           ReplyKeyboardRemove)



main = ReplyKeyboardMarkup(
    keyboard=[
      [KeyboardButton(text='Профиль')],[KeyboardButton(text='Каталог')],
      [KeyboardButton(text='Корзина')]

    ],resize_keyboard=True)




profile = ReplyKeyboardMarkup(

    keyboard=[
        [KeyboardButton(text='Мои заказы')], [KeyboardButton(text='Мои данные')],
        [KeyboardButton(text='Назад')]

    ],resize_keyboard=True
)



