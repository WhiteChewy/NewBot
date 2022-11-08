# -*- coding: utf-8 -*-
import os
import config
import logging
import User
import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# форма нашего пользователя
class Form(StatesGroup):
    name = State()

@dp.message_handler(commands='start')
async def start(message: types.Message):
    keyboard = types.inline_keyboard.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registration')
    keyboard.add(reg_button)
    photo = open('./pic/start.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await message.answer("""👋 Добро пожаловать!
    
Создайте свой профиль и пройдите небольшой тест, который поможет роботу понять, кто вам действительно подходит.
    
Робот будет еженедельно подбирать для вас наиболее подходящую пару, с которой вы сможете пообщаться, чтобы лучше узнать друг друга!""",
     reply_markup=keyboard)


# async def reg_start(chat_id):
    


async def registration(chat_id):
    await Form.name.set()
    await bot.send_message(chat_id, """Представьтесь, пожалуйста!

Напишите своё имя, оно будет указано в вашем профиле и его будут видеть другие пользователи системы.

Не используйте прозвища и никнеймы, это может вызвать негативное впечатление при первом знакомстве.    
    """)

@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    
    await Form.next()
    await message.reply('Привет '+data['name'])


@dp.callback_query_handler(lambda call: True)
async def registration_callback(call):
    if call.data == 'registration':
        reg_keyboard = types.inline_keyboard.InlineKeyboardMarkup(resize_keyboard=True)
        reg_start_button = types.InlineKeyboardButton('✅ Перейти к заполнению', callback_data='registration_start')
        reg_keyboard.add(reg_start_button)
        await bot.send_message(call.message.chat.id, """В процессе регистрации будет сформирован ваш профиль и взяты данные для поиска.
        
Отнеситесь к процессу регистрации ответственно.
        
Регистрация будет проходить в три этапа:
➡️ Формирование профиля и личного датасета.
➡️ Тест на определение личных предпочтений фенотипа партнёра.
➡️ Дополнение датасета важными данными для улучшения поиска.
        
Вся регистрация займёт не больше 3-5 минут.""",
        reply_markup=reg_keyboard)
    pass
    if call.data == 'registration_start':
        await registration(call.message.chat.id)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
