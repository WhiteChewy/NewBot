# -*- coding: utf-8 -*-
import os
import config
import logging
import datetime

from User import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_form = User()

# форма нашего пользователя
class Form(StatesGroup):
    value = State()


class Gender_Form(StatesGroup):
    gender = State()

@dp.message_handler(commands='begin')
async def start(message: types.Message):
    keyboard = types.inline_keyboard.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registration')
    keyboard.add(reg_button)
    photo = open('./pic/start.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text="""👋 Добро пожаловать!
    
Создайте свой профиль и пройдите небольшой тест, который поможет роботу понять, кто вам действительно подходит.
    
Робот будет еженедельно подбирать для вас наиболее подходящую пару, с которой вы сможете пообщаться, чтобы лучше узнать друг друга!""",
    reply_markup=keyboard)


# Ожидаем пока пользователь введет имя и сохраняем его
@dp.message_handler(state=Form.value)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
    
    await Form.next()
    user_form.name = data['value']
    print(user_form)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton('Я мужчина, ищу женщину', callback_data='male')
    female_button = types.InlineKeyboardButton('Я женщина, ищу мужчину', callback_data='female')
    other_button = types.InlineKeyboardButton('Другое', callback_data='other')
    keyboard.add(male_button, female_button, other_button)
    await bot.send_message(message.chat.id, text="🟢 Укажите ваш пол и кого вы ищете:", reply_markup=keyboard)


@dp.callback_query_handler(text='registration')
async def show_registration(message: types.Message):
    reg_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    reg_start_button = types.InlineKeyboardButton('✅ Перейти к заполнению', callback_data='registration_start')
    reg_keyboard.add(reg_start_button)
    await bot.send_message(message.from_user.id, text="""В процессе регистрации будет сформирован ваш профиль и взяты данные для поиска.
        
Отнеситесь к процессу регистрации ответственно.
        
Регистрация будет проходить в три этапа:
➡️ Формирование профиля и личного датасета.
➡️ Тест на определение личных предпочтений фенотипа партнёра.
➡️ Дополнение датасета важными данными для улучшения поиска.
        
Вся регистрация займёт не больше 3-5 минут.""", reply_markup=reg_keyboard)


@dp.callback_query_handler(text='registration_start')
async def show_registration_start(message: types.Message):
    await Form.value.set()
    await bot.send_message(message.from_user.id, """Представьтесь, пожалуйста!

Напишите своё имя, оно будет указано в вашем профиле и его будут видеть другие пользователи системы.

Не используйте прозвища и никнеймы, это может вызвать негативное впечатление при первом знакомстве.    
    """)


@dp.callback_query_handler(text='male')
async def show_male_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'inside male')


@dp.callback_query_handler(text='female')
async def show_female_menu(message: types.Message):
    await bot.send_message(message.from_user.id, 'inside female')


@dp.callback_query_handler(text='other')
async def show_other(message: types.Message):
    await bot.send_message(message.from_user.id, 'WHAT THE F*CK ARE U?!')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
