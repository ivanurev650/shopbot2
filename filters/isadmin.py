from typing import List
from database.get import get_user
from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = await get_user(message.from_user.id)
        if user and user['role'] == 'admin':
            return True
        return False


class IsManager(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user = await get_user(message.from_user.id)
        if user and user['role'] == 'manager':
            return True
        return False