# -*- coding: utf-8 -*-
import config
import logging

from ru_message_texts import *
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# сообщение и стартовые кнопки перейти сразу к регистрации или прочитать что это за проект
@dp.message_handler(commands='start')
async def show_starting_menu(message: types.Message):
    photo = open('./pic/start.jpg', 'rb')
    starting_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    about_project_button = types.InlineKeyboardButton('ℹ️ Читать о проекте', callback_data='1back')
    starting_inline_keyboard.add(registration_button)
    starting_inline_keyboard.add(about_project_button)
    await bot.send_photo(message.from_user.id, photo, caption=WELCOME, reply_markup=starting_inline_keyboard)

# сообщение с информацией о проекте
@dp.callback_query_handler(text='about')
async def show_about_text(query: types.CallbackQuery):
    about_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    about_keyboard.add(registration_button)
    about_keyboard.add(back_button)
    await query.message.edit_text(text=ABOUT, reply_markup=about_keyboard)

# сообщение с информацией об уникальности проекта
@dp.callback_query_handler(text='uniqueness')
async def show_uniqueness(query: types.CallbackQuery):
    uniqueness_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    uniqueness_inline_keyboard.add(registration_button)
    uniqueness_inline_keyboard.add(back_button)
    await query.message.edit_text(text=UNIQUENESS, reply_markup=uniqueness_inline_keyboard)

# сообщение с информацией об импринтинге
@dp.callback_query_handler(text='imprint')
async def show_imprint(query: types.CallbackQuery):
    imprint_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    imprint_inline_keyboard.add(registration_button)
    imprint_inline_keyboard.add(back_button)
    await query.message.edit_text(text=IMPRINT, reply_markup=imprint_inline_keyboard)
            
# сообщение с пользовательским соглашением
@dp.callback_query_handler(text='user_agreement_1')
async def show_user_agreement(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    forward_button = types.InlineKeyboardButton('Вперед➡️', callback_data='user_agreement_2')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    empty_button = types.InlineKeyboardButton('1 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=USER_AGREEMENT1, reply_markup=user_agreement_keyboard)


@dp.callback_query_handler(text='user_agreement_2')
async def show_user_agreement2(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    forward_button = types.InlineKeyboardButton('Вперед➡️', callback_data='user_agreement_3')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='user_agreement_1')
    empty_button = types.InlineKeyboardButton('2 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=USER_AGREEMENT2, reply_markup=user_agreement_keyboard)


@dp.callback_query_handler(text='user_agreement_3')
async def show_user_agreement3(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    forward_button = types.InlineKeyboardButton('🔁Обратно в меню', callback_data='back')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='user_agreement_2')
    empty_button = types.InlineKeyboardButton('3 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=USER_AGREEMENT3, reply_markup=user_agreement_keyboard)

# меню часто задоваемых вопросов
@dp.callback_query_handler(text='faq')
async def show_faq(query: types.CallbackQuery):
    faq_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    concept_button = types.InlineKeyboardButton('📊Концепция сервиса', callback_data='concept')
    photo_button = types.InlineKeyboardButton('🖼Фото пользователей', callback_data='photo')
    find_button = types.InlineKeyboardButton('💑Поиск пары и оплата', callback_data='find')
    investors_button = types.InlineKeyboardButton('📈Партнеры и инвесторы', callback_data='investors')
    journalist_button = types.InlineKeyboardButton('📝Для журналистов', callback_data='journalists')
    back_button = types.InlineKeyboardButton('⬅️Назад в главное меню', callback_data='back')
    faq_inline_keyboard.row(concept_button, photo_button)
    faq_inline_keyboard.row(find_button, investors_button)
    faq_inline_keyboard.row(journalist_button, back_button)
    await query.message.edit_text(text='Выберете раздел FAQ.', reply_markup=faq_inline_keyboard)

# действия начала регистрации
@dp.callback_query_handler(text='register')
async def show_register(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='back')
    keyboard.add(back_button)
    await query.message.edit_text(text='Извините, сюда пока нельзя.', reply_markup=keyboard)

# возвращение в главное меню
@dp.callback_query_handler(text='1back')
async def show_back(message: types.Message):
    start_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    about_button = types.InlineKeyboardButton('🧾О проекте', callback_data='about')
    uniqueness_button = types.InlineKeyboardButton('🔮Уникальность', callback_data='uniqueness')
    imprinting_button = types.InlineKeyboardButton('💡Что такое импринтинг', callback_data='imprint')
    start_inline_keyboard.row(about_button, uniqueness_button, imprinting_button)
    user_agreement_button = types.InlineKeyboardButton('📝Соглашение', callback_data='user_agreement_1')
    faq_button = types.InlineKeyboardButton('❓Частые вопросы', callback_data='faq')
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    start_inline_keyboard.row(user_agreement_button, faq_button, registration_button)
    await bot.send_message(message.from_user.id, text='Вы можете нажать любую кнопку ниже, и узнать всю необходимую информацию о нашем проекте.', reply_markup=start_inline_keyboard)


@dp.callback_query_handler(text='back')
async def show_back(query: types.CallbackQuery):
    start_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    about_button = types.InlineKeyboardButton('🧾О проекте', callback_data='about')
    uniqueness_button = types.InlineKeyboardButton('🔮Уникальность', callback_data='uniqueness')
    imprinting_button = types.InlineKeyboardButton('💡Что такое импринтинг', callback_data='imprint')
    start_inline_keyboard.row(about_button, uniqueness_button, imprinting_button)
    user_agreement_button = types.InlineKeyboardButton('📝Соглашение', callback_data='user_agreement_1')
    faq_button = types.InlineKeyboardButton('❓Частые вопросы', callback_data='faq')
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='register')
    start_inline_keyboard.row(user_agreement_button, faq_button, registration_button)
    await query.message.edit_text(text='Вы можете нажать любую кнопку ниже, и узнать всю необходимую информацию о нашем проекте.', reply_markup=start_inline_keyboard)


# сообщение о концепте проекта
@dp.callback_query_handler(text='concept')
async def show_concept(query: types.CallbackQuery):
    back_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    back_inline_keyboard.add(registration_button)
    back_inline_keyboard.add(back_button)
    await query.message.edit_text(text=CONCEPT, reply_markup=back_inline_keyboard)

# сообщение информации о фотографиях
@dp.callback_query_handler(text='photo')
async def show_photo(query: types.CallbackQuery):
    photo_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    photo_inline_keyboard.add(registration_button)
    photo_inline_keyboard.add(back_button)
    await query.message.edit_text(text= PHOTO, reply_markup=photo_inline_keyboard)

# сообщение о поисках и оплатах услуг
@dp.callback_query_handler(text='find')
async def show_find(query: types.CallbackQuery):
    find_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    find_inline_keyboard.add(registration_button)
    find_inline_keyboard.add(back_button)
    await query.message.edit_text(text=FIND, reply_markup=find_inline_keyboard)

# сообщение для инвесторов
@dp.callback_query_handler(text='investors')
async def show_investors(query: types.CallbackQuery):
    investors_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    investors_inline_keyboard.add(registration_button)
    investors_inline_keyboard.add(back_button)
    await query.message.edit_text(text=INVESTORS, reply_markup=investors_inline_keyboard)

# сообщение для журналистов
@dp.callback_query_handler(text='journalists')
async def show_journalists(query: types.CallbackQuery):
    journalists_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton('✅Начать регистрацию', callback_data='registr')
    back_button = types.InlineKeyboardButton('⬅️Назад', callback_data='faq')
    journalists_inline_keyboard.add(registration_button)
    journalists_inline_keyboard.add(back_button)
    await query.message.edit_text(text=JOURNALISTS, reply_markup=journalists_inline_keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
