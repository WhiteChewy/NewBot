# -*- coding: utf-8 -*-
import logging
import requests
import texts

from User import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_form = User()
scheduler = AsyncIOScheduler()
scheduler.start()
# форма нашего пользователя
class Form(StatesGroup):
    value = State()
    birthdate = State()
    profile_photo = State()
    first_side_photo = State()
    second_side_photo = State()
    third_side_photo = State()


@dp.message_handler(commands='start')
@dp.callback_query_handler(text='begin')
async def registration_begin(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton('✅Начать', callback_data='begin_registration')
    keyboard.add(reg_button)
    photo = open('./pic/letsgo.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text= texts.LETS_GO, reply_markup=keyboard)


@dp.callback_query_handler(text='begin_registration')
async def show_rules(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    lets_go_button = types.InlineKeyboardButton('✅ Перейти к заполнению', callback_data='lets_go')
    keyboard.add(lets_go_button)
    await query.message.edit_text(text=texts.REGISTRATION_RULES, reply_markup=keyboard)

# Ввод имени
@dp.callback_query_handler(text='lets_go')
async def show_registration_start(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=texts.NAME)
    await Form.value.set()

# Ожидаем пока пользователь введет имя и сохраняем его
@dp.message_handler(state=Form.value, content_types=types.ContentTypes.TEXT)
async def process_name(message: types.Message, state: FSMContext):
    if any(map(str.isdigit, message.text)):
        await message.reply(texts.NAME)
        return
    async with state.proxy() as data:
        data['value'] = message.text
    
    user_form.fname = data['value']
    await state.finish()
    # сообщение о выборе пола
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton('Я мужчина, ищу женщину', callback_data='male')
    female_button = types.InlineKeyboardButton('Я женщина, ищу мужчину', callback_data='female')
    other_button = types.InlineKeyboardButton('Другое', callback_data='other')
    keyboard.add(male_button, female_button, other_button)
    await bot.send_message(message.chat.id, text="🟢 Укажите ваш пол и кого вы ищете:", reply_markup=keyboard)


@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery):
    user_form.gender = 'М'
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = message.text
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':data['birthdate']})
    if request.text[11:13] != 'ok':
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    user_form.birthdate = data['birthdate']
    await state.finish()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton('🏢 Москва', callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton('🏬 Санкт-Петербург', callback_data='saint-p')
    samara_button = types.InlineKeyboardButton('🏤 Самара', callback_data='samara')
    other_button = types.InlineKeyboardButton('🌆 Другой город', callback_data='other')
    nomad_button = types.InlineKeyboardButton('🏇 Я кочевник', callback_data='nomad')
    keyboard.add(moscow_button)
    keyboard.add(saint_p_button)
    keyboard.add(samara_button)
    keyboard.add(other_button)
    keyboard.add(nomad_button)
    await bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)


@dp.callback_query_handler(text='female')
async def show_female_menu(query: types.CallbackQuery):
    user_form.gender = 'Ж'
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = message.text
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':data['birthdate']})
    if request.text[11:13] != 'ok':
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    user_form.birthdate = data['birthdate']
    await state.finish()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton('🏢 Москва', callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton('🏬 Санкт-Петербург', callback_data='saint-p')
    samara_button = types.InlineKeyboardButton('🏤 Самара', callback_data='samara')
    other_button = types.InlineKeyboardButton('🌆 Другой город', callback_data='other')
    nomad_button = types.InlineKeyboardButton('🏇 Я кочевник', callback_data='nomad')
    keyboard.add(moscow_button)
    keyboard.add(saint_p_button)
    keyboard.add(samara_button)
    keyboard.add(other_button)
    keyboard.add(nomad_button)
    bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)

@dp.callback_query_handler(text='other')
async def show_other(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton('✅ Подписаться на наш канал', url='https://t.me/UnisonDating')
    again_button = types.InlineKeyboardButton('🔁 Начать регистрацию с начала', callback_data='begin_registration')
    keyboard.add(subscribe_button)
    keyboard.add(again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)


@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery):
    user_form.city = 'Москва'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton('💙 Серьёзные отношения', callback_data='srsly')
    family_button = types.InlineKeyboardButton('💜 Создание семьи', callback_data='family')
    friends_button = types.InlineKeyboardButton('Дружба и общение', callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton('Встречи без обязательств', callback_data='without')
    no_answer_button = types.InlineKeyboardButton('Затрудняюсь ответить', callback_data='noanswer')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text('🎯 Выберите с какой целью вы ищете новые знакомства', reply_markup=keyboard)

@dp.callback_query_handler(text='saint-p')
async def add_saintp(query: types.CallbackQuery):
    user_form.city = 'Санкт-Петербург'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton('💙 Серьёзные отношения', callback_data='srsly')
    family_button = types.InlineKeyboardButton('💜 Создание семьи', callback_data='family')
    friends_button = types.InlineKeyboardButton('Дружба и общение', callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton('Встречи без обязательств', callback_data='without')
    no_answer_button = types.InlineKeyboardButton('Затрудняюсь ответить', callback_data='noanswer')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text('🎯 Выберите с какой целью вы ищете новые знакомства', reply_markup=keyboard)

@dp.callback_query_handler(text='samara')
async def add_samara(query: types.CallbackQuery):
    user_form.city = 'Самара'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton('💙 Серьёзные отношения', callback_data='srsly')
    family_button = types.InlineKeyboardButton('💜 Создание семьи', callback_data='family')
    friends_button = types.InlineKeyboardButton('Дружба и общение', callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton('Встречи без обязательств', callback_data='without')
    no_answer_button = types.InlineKeyboardButton('Затрудняюсь ответить', callback_data='noanswer')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text('🎯 Выберите с какой целью вы ищете новые знакомства', reply_markup=keyboard)


@dp.callback_query_handler(text='nomad')
async def add_nomad(query: types.CallbackQuery):
    user_form.city = 'Кочевник'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton('💙 Серьёзные отношения', callback_data='srsly')
    family_button = types.InlineKeyboardButton('💜 Создание семьи', callback_data='family')
    friends_button = types.InlineKeyboardButton('Дружба и общение', callback_data='other')
    withou_obligations_button = types.InlineKeyboardButton('Встречи без обязательств', callback_data='other')
    no_answer_button = types.InlineKeyboardButton('Затрудняюсь ответить', callback_data='other')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text('🎯 Выберите с какой целью вы ищете новые знакомства', reply_markup=keyboard)


@dp.callback_query_handler(text='srsly')
async def add_reason_srsly(query: types.CallbackQuery):
    user_form.reason = 'Серьезные отношения'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton('Рекомендации по загрузке', callback_data='recomendation')
    download_photo_button = types.InlineKeyboardButton('Загрузить фото', callback_data='download_main')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)


@dp.callback_query_handler(text='family')
async def add_reason_family(query: types.CallbackQuery):
    user_form.reason = 'Создание семьи'
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton('Рекомендации по загрузке', callback_data='recomendation')
    download_photo_button = types.InlineKeyboardButton('Загрузить фото профиля', callback_data='download_main')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# перед обработкой этого события надо отправить user_form в чат модерации на модерацию
@dp.callback_query_handler(text='download_main')
async def ad_photo(query: types.CallbackQuery):
    await query.message.edit_text(texts.DOWNLOAD_PHOTO)
    await Form.profile_photo.set()
@dp.message_handler(state=Form.profile_photo, content_types=types.ContentTypes.PHOTO)
async def download_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    user_form.profile_photo = file_id
    await state.finish()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton('✅Да', callback_data='confirm_photo')
    again_button = types.InlineKeyboardButton('❌Нет', callback_data='download_main')
    keyboard.add(confirm_button, again_button)
    await bot.send_photo(message.from_user.id, file_id)
    await bot.send_message(message.from_user.id, text='Вы действительно хотите установить это фото профиля? Помните фотографии отправляются на модерацию людьми, обмануть систему не получится.', reply_markup=keyboard)

@dp.callback_query_handler(text='confirm_photo')
async def end_basic_registration(message: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    watch_profile_button = types.InlineKeyboardButton('🧾Посмотреть профиль', callback_data='show_base_profile')
    next_button = types.InlineKeyboardButton('Следующий шаг➡️', callback_data='next_step')
    keyboard.row(watch_profile_button, next_button)
    await bot.send_message(message.from_user.id, texts.BASE_PROFILE, reply_markup=keyboard)


@dp.callback_query_handler(text='recomendation')
async def show_recomendation(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton('Загрузить фото', callback_data='download_main')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)


@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery):
    text = 'Name: %s\n\nBirthday: %s\n\nGender: %s\n\nCity: %s\n\nYou want from relationships: %s' % (user_form.fname, user_form.birthdate, user_form.gender, user_form.city, user_form.reason)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton('Перейти к следующему шагу', callback_data='next_step')
    reg_button = types.InlineKeyboardButton('Начать регистрацию заново', callback_data='begin')
    keyboard.add(reg_button, next_button)
    await bot.send_photo(message.from_user.id, photo= user_form.profile_photo, caption=text, reply_markup=keyboard)



@dp.callback_query_handler(text='next_step')
async def upload_three_photo(message: types.Message):
    photo = open('./pic/3photos.png', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.THREE_PHOTOS)
    await Form.first_side_photo.set()
@dp.message_handler(state=Form.first_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_first_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    user_form.first_photo = photo_id
    await state.finish()
    await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
    await Form.second_side_photo.set()
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_second_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    user_form.second_photo = photo_id
    await state.finish()
    await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
    await Form.third_side_photo.set()
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_third_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    user_form.third_photo = photo_id
    await state.finish()
    await bot.send_photo(message.from_user.id, photo=user_form.first_photo)
    await bot.send_photo(message.from_user.id, photo=user_form.second_photo)
    await bot.send_photo(message.from_user.id, photo=user_form.third_photo)
    await bot.send_message(message.from_user.id, text=texts.ALL_PHOTO)



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
