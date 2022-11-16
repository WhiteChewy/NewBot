# -*- coding: utf-8 -*-
import os
import logging
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json

from aiogram.dispatcher.filters import Filter
from User import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
user_form = User()


# STATES FOR STATE MACHINE
class Form(StatesGroup):
    # PROFILE states.
    name = State()
    birthdate = State()
    city = State()
    reason = State()
    gender = State()
    profile_photo = State()
    first_side_photo = State()
    second_side_photo = State()
    third_side_photo = State()
    # TAGS states.
    tags = State()       # when active user status changes. data name = name of state


# BOT MESSAGES MECHANICS
# -----------------------------------------------------------------
#-------------------------STARTING DIALOG--------------------------
#------------------------------------------------------------------
#
# WELCOME MESSAGE AND CHOICE GO TO REGISTRATION OR READ ABOUT PROJECT
@dp.message_handler(commands='start')
async def show_starting_menu(message: types.Message):
    photo = open('./pic/start.jpg', 'rb')
    starting_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    about_project_button = types.InlineKeyboardButton(buttons_texts.INFO_ABOUT_PROJECT, callback_data='back')
    starting_inline_keyboard.add(about_project_button)
    starting_inline_keyboard.add(registration_button)
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.WELCOME, reply_markup=starting_inline_keyboard)

# MESSAGE ABOUT PROJECT
@dp.callback_query_handler(text='about')
async def show_about_text(query: types.CallbackQuery):
    about_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    about_keyboard.row( back_button, registration_button)
    await query.message.edit_text(text=texts.ABOUT, reply_markup=about_keyboard)

# MESSAGE ABOUT UNIQUENESS OF PROJECT
@dp.callback_query_handler(text='uniqueness')
async def show_uniqueness(query: types.CallbackQuery):
    uniqueness_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    uniqueness_inline_keyboard.add(back_button, registration_button)
    await query.message.edit_text(text=texts.UNIQUENESS, reply_markup=uniqueness_inline_keyboard)

# MESSAGE ABOUT WHAT IS IMPRINTING
@dp.callback_query_handler(text='imprint')
async def show_imprint(query: types.CallbackQuery):
    imprint_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    imprint_inline_keyboard.add(registration_button)
    imprint_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.IMPRINT, reply_markup=imprint_inline_keyboard)
            
# FIRST OF THREE MESSAGE WITH USER AGREEMENT
@dp.callback_query_handler(text='user_agreement_1')
async def show_user_agreement(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    forward_button = types.InlineKeyboardButton(buttons_texts.FORWARD, callback_data='user_agreement_2')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    empty_button = types.InlineKeyboardButton('1 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=texts.USER_AGREEMENT1, reply_markup=user_agreement_keyboard)
# SECOND OF THREE MESSAGE WITH USER AGREEMENT
@dp.callback_query_handler(text='user_agreement_2')
async def show_user_agreement2(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    forward_button = types.InlineKeyboardButton(buttons_texts.FORWARD, callback_data='user_agreement_3')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='user_agreement_1')
    empty_button = types.InlineKeyboardButton('2 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=texts.USER_AGREEMENT2, reply_markup=user_agreement_keyboard)
# THIRD OF THREE MESSAGE WITH USER AGREEMENT
@dp.callback_query_handler(text='user_agreement_3')
async def show_user_agreement3(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    forward_button = types.InlineKeyboardButton(buttons_texts.BACK_TO_THE_MENU, callback_data='back')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='user_agreement_2')
    empty_button = types.InlineKeyboardButton('3 из 3', callback_data='free')
    user_agreement_keyboard.row(back_button, empty_button, forward_button)
    user_agreement_keyboard.add(registration_button)
    await query.message.edit_text(text=texts.USER_AGREEMENT3, reply_markup=user_agreement_keyboard)

# FAQ MENU
@dp.callback_query_handler(text='faq')
async def show_faq(query: types.CallbackQuery):
    faq_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    concept_button = types.InlineKeyboardButton(buttons_texts.CONCEPT, callback_data='concept')
    photo_button = types.InlineKeyboardButton(buttons_texts.PHOTO, callback_data='photo')
    find_button = types.InlineKeyboardButton(buttons_texts.FIND, callback_data='find')
    investors_button = types.InlineKeyboardButton(buttons_texts.INVESTORS, callback_data='investors')
    journalist_button = types.InlineKeyboardButton(buttons_texts.JOURNALISTS, callback_data='journalists')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK_TO_THE_MENU, callback_data='back')
    faq_inline_keyboard.row(concept_button, photo_button)
    faq_inline_keyboard.row(find_button, investors_button)
    faq_inline_keyboard.row(journalist_button, back_button)
    await query.message.edit_text(text=texts.FAQ_CHOOSE, reply_markup=faq_inline_keyboard)

# BACK TO THE MAIN MENU
@dp.callback_query_handler(text='back')
async def show_back(query: types.CallbackQuery):
    start_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    about_button = types.InlineKeyboardButton(buttons_texts.ABOUT_PROJECT, callback_data='about')
    uniqueness_button = types.InlineKeyboardButton(buttons_texts.UNIQ, callback_data='uniqueness')
    imprinting_button = types.InlineKeyboardButton(buttons_texts.ABOUT_IMPRINTING, callback_data='imprint')
    start_inline_keyboard.row(about_button, uniqueness_button, imprinting_button)
    user_agreement_button = types.InlineKeyboardButton(buttons_texts.USER_AGREEMENT, callback_data='user_agreement_1')
    faq_button = types.InlineKeyboardButton(buttons_texts.FAQ, callback_data='faq')
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    start_inline_keyboard.row(user_agreement_button, faq_button, registration_button)
    await query.message.edit_text(text=texts.ABOUT_MENU, reply_markup=start_inline_keyboard)

# MESSAGE ABOUT CONCEPT
@dp.callback_query_handler(text='concept')
async def show_concept(query: types.CallbackQuery):
    back_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    back_inline_keyboard.add(registration_button)
    back_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.CONCEPT, reply_markup=back_inline_keyboard)

# MESSAGE ABOUT USAGE OF USER PHOTO
@dp.callback_query_handler(text='photo')
async def show_photo(query: types.CallbackQuery):
    photo_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    photo_inline_keyboard.add(registration_button)
    photo_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.PHOTO, reply_markup=photo_inline_keyboard)

# MESSAGE ABOUT PAYING FOR SUBSCRIBE
@dp.callback_query_handler(text='find')
async def show_find(query: types.CallbackQuery):
    find_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    find_inline_keyboard.add(registration_button)
    find_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.FIND, reply_markup=find_inline_keyboard)

# MESSAGE FOR INVESTORS
@dp.callback_query_handler(text='investors')
async def show_investors(query: types.CallbackQuery):
    investors_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    investors_inline_keyboard.add(registration_button)
    investors_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.INVESTORS, reply_markup=investors_inline_keyboard)

# MESSAGE FOR JOURNALISTS
@dp.callback_query_handler(text='journalists')
async def show_journalists(query: types.CallbackQuery):
    journalists_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    journalists_inline_keyboard.add(registration_button)
    journalists_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.JOURNALISTS, reply_markup=journalists_inline_keyboard)


#----------------------------REGISTRATION--------------------------
#------------------------------------------------------------------
#
@dp.callback_query_handler(text='begin')
async def registration_begin(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton(buttons_texts.BEGIN_BUTTON, callback_data='begin_registration')
    keyboard.add(reg_button)
    photo = open('./pic/letsgo.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text= texts.LETS_GO, reply_markup=keyboard)
    # TAGS INITIATION
    await Form.tags.set()
    await state.update_data(moderated_photo=False)
    await state.update_data(moderated_info=False)
    await state.update_data(moderated=False)
    await state.update_data(reuploading_photo=False)
    await state.update_data(alogrithm_studing=False)
    await state.update_data(extra_photos_uploaded=False)
    await state.reset_state(with_data=False)
    await state.update_data(likes=7)
    await state.update_data(super_likes=5)
    await state.update_data(algorithm_steps=31)
    await state.update_data(chat_id = message.from_user.id)


# REGISTRATION RULES
@dp.callback_query_handler(text='begin_registration')
async def begin_registration(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    lets_go_button = types.InlineKeyboardButton(buttons_texts.START_REGISTRATION_BUTTON, callback_data='start_step')
    keyboard.add(lets_go_button)
    await query.message.edit_text(text=texts.REGISTRATION_RULES, reply_markup=keyboard)

# SET name STATE in STATE MACHINE as ACTIVE
@dp.callback_query_handler(text='start_step')
async def show_registration_start_step(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=texts.NAME)
    await Form.name.set()
# SET profile NAME and FINISH NAME STATE in STATE MACHINE
@dp.message_handler(state=Form.name, content_types=types.ContentTypes.TEXT)
async def set_profile_name(message: types.Message, state: FSMContext):
    if any(map(str.isdigit, message.text)): # check if name is "correct"
        await message.reply(texts.NAME)
        return 
    await state.update_data(name=message.text) # set the profile name 
    await state.reset_state(with_data=False) # close the NAME state in STATE MACHINE
    # GENDER CHOOSE MESSAGE AND InlineKeyboard
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton(buttons_texts.GENDER_MALE[0], callback_data='male')
    female_button = types.InlineKeyboardButton(buttons_texts.GENDER_FEMALE[0], callback_data='female')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_GENDER, callback_data='under_construction')
    keyboard.add(male_button, female_button, under_construction_button)
    await bot.send_message(message.chat.id, text=texts.GENDER_CHOOSE, reply_markup=keyboard)

# SET profile GENDER to MALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery, state: FSMContext):
    await Form.gender.set()
    await state.update_data(gender=buttons_texts.GENDER_MALE[1])
    await state.reset_state(with_data=False)
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    # chek the date with POST request
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':message.text})
    # transform answer from string to json-format
    status = json.loads(request.text)
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.update_data(birthday=message.text)
    await state.reset_state(with_data=False) # finish the BIRTHDAY STATE in STATE MACHINE
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton(buttons_texts.MOSCOW, callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton(buttons_texts.SAINT_PETERSBURG, callback_data='saint-p')
    samara_button = types.InlineKeyboardButton(buttons_texts.SAMARA, callback_data='samara')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_CITY, callback_data='under_construction')
    nomad_button = types.InlineKeyboardButton(buttons_texts.NOMAD, callback_data='nomad')
    keyboard.add(moscow_button)
    keyboard.add(saint_p_button)
    keyboard.add(samara_button)
    keyboard.add(under_construction_button)
    keyboard.add(nomad_button)
    await bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)

# SET profile GENDER to FEMALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='female')
async def show_female_menu(query: types.CallbackQuery, state: FSMContext):
    await Form.gender.set()
    await state.update_data(gender=buttons_texts.GENDER_FEMALE[1])
    await state.reset_state(with_data=False)
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    # chek the date with POST requestg
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':message.text})
    # transform answer from string to json-format
    status = json.loads(request.text)
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.update_data(birthday=message.text)
    await state.reset_state(with_data=False) # finish the BIRTHDAY STATE in STATE MACHINE
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton(buttons_texts.MOSCOW, callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton(buttons_texts.SAINT_PETERSBURG, callback_data='saint-p')
    samara_button = types.InlineKeyboardButton(buttons_texts.SAMARA, callback_data='samara')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_CITY, callback_data='under_construction')
    nomad_button = types.InlineKeyboardButton(buttons_texts.NOMAD, callback_data='nomad')
    keyboard.add(moscow_button)
    keyboard.add(saint_p_button)
    keyboard.add(samara_button)
    keyboard.add(under_construction_button)
    keyboard.add(nomad_button)
    bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)


@dp.callback_query_handler(text='under_construction')
async def show_under_construction(message: types.Message):
    """
    THERE ARE TWO GENDERS
    """
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)


# SET city as Moscow and ASK about goal of the relationship
@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery, state: FSMContext):
    await Form.city.set()
    await state.update_data(city=texts.MOSCOW)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='under_constructions')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='under_construction')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='under_construction')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET city as SAINT-PETERSBURG and ASK about goal of the relationship
@dp.callback_query_handler(text='saint-p')
async def add_saintp(query: types.CallbackQuery, state: FSMContext):
    await Form.city.set()
    await state.update_data(city=texts.SAINT_PETERSBURG)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='under_constructions')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='under_construction')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='under_construction')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET city as SAMARA and ASK about goal of the relationship
@dp.callback_query_handler(text='samara')
async def add_samara(query: types.CallbackQuery, state: FSMContext):
    await Form.city.set()
    await state.update_data(city=texts.SAMARA)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='under_constructions')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='under_construction')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='under_construction')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# IF u change cities very often than we SET ur city as a nomad and ASK about goal of the relationship
@dp.callback_query_handler(text='nomad')
async def add_nomad(query: types.CallbackQuery, state= FSMContext):
    await Form.city.set()
    await state.update_data(city=texts.NOMAD)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='under_constructions')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='under_construction')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='under_construction')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET ur relationship goal as SERIOUS RELATIONSHIP and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='srsly')
async def add_reason_srsly(query: types.CallbackQuery, state: FSMContext):
    await Form.reason.set()
    await state.update_data(reason=texts.SERIOUS_REL)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='recomendations')
    download_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# SET ur relationship goal as MAKING FAMILY and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='family')
async def add_reason_family(query: types.CallbackQuery, state: FSMContext):
    await Form.reason.set()
    await state.update_data(reason=texts.FAMILY)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='recomendations')
    download_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# user uploads MAIN PHOTO of his profile. Activate the MAIN PHOTO STATE OF STATE MACHINE. CONFIRMING THE PHOTO
@dp.callback_query_handler(text='upload_main_photo')
async def ad_photo(query: types.CallbackQuery):
    await query.message.edit_text(texts.UPLOAD_PHOTO)
    await Form.profile_photo.set()
# DOWNLOADING MAIN PHOTO OF PROFILE. BECOURSE WE NEED TO FORWARD IT TO MODERATION CHAT
@dp.message_handler(state=Form.profile_photo, content_types=types.ContentTypes.PHOTO)
async def download_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await message.photo[-1].download(destination_file='./pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id)) # DOWNLOADIN MAIN PHOTO 
    profile_photo = './pic/profiles/%s/main_profile_photo.jpg' % (str(message.from_user.id)) # PATH to the MAIN PHOTO
    await state.update_data(profile_photo=profile_photo)
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='confirm_photo')
    again_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='upload_main_photo')
    keyboard.row(confirm_button, again_button)
    #await bot.send_photo(message.from_user.id, file_id)
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_PHOTO, reply_markup=keyboard)

# User MAKE the BASIC ACCOUNT. He can choose to check if nothing wrong or move to uploading extra photos
@dp.callback_query_handler(text='confirm_photo')
async def end_basic_registration(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    watch_profile_button = types.InlineKeyboardButton(buttons_texts.WATCH_PROFILE, callback_data='show_base_profile')
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    keyboard.row(watch_profile_button, next_button)
    await query.message.edit_text(texts.BASE_PROFILE, reply_markup=keyboard)

# SHOWING recomendations to uploading PHOTOS
@dp.callback_query_handler(text='recomendations')
async def show_recomendation(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)

# SHOWING base profile of user
@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery,state: FSMContext):
    data = await state.get_data()
    text = '%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s' % (texts.FIRST_NAME ,data['name'], texts.BIRTHDAY, data['birthday'], texts.GENDER, data['gender'], \
                                                                 texts.CITY, data['city'], texts.REASON, data['reason'])
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    reg_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin')
    keyboard.row(reg_button, next_button)
    photo = open(data['profile_photo'], 'rb')
    await bot.send_photo(message.from_user.id, photo=photo, caption=text, reply_markup=keyboard)


# We need 3 photos from different sides of your face. UPLOADING FIRST and GIVING INFO about PHOTOS that service needs
@dp.callback_query_handler(text='upload_extra_photo')
async def upload_three_photo(message: types.Message):
    photo = open('./pic/3photos.png', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.EXTRA_PHOTOS)
    await Form.first_side_photo.set()
# IF ANSWER OF USER IS PHOTO and STATE first_side_photo is ACTIVE = UPLOAD 1st PHOTO TO SERVER and FINISH THE first side photo STATE IN STATE MACHINE and ACTIVATE second_side_photo STATE
@dp.message_handler(state=Form.first_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_first_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='./pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id))
    user_form.first_photo = './pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
    await Form.second_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE second_side_photo is ACTIVE = UPLOAD 2nd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_second_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='./pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id))
    user_form.second_photo = './pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id)
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
    await Form.third_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE third_side_photo is ACTIVE = UPLOAD 3rd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_third_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='./pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id))
    user_form.third_photo = './pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id)
    await state.reset_state(with_data=False)
    inline_keyboard = types.InlineKeyboardMarkup(resize_true = True)
    chek_button = types.InlineKeyboardButton(buttons_texts.CHECK_EXTRA_PHOTOS, callback_data='show_extra_photos')
    next_step_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='start_alogrithm_educating')
    inline_keyboard.row(chek_button, next_step_button)
    await bot.send_message(message.from_user.id, text=texts.ALL_PHOTOS, reply_markup=inline_keyboard)
# CONFIRMING EXTRA PHOTOS BEFORE UPLOADING
@dp.callback_query_handler(text='show_extra_photos')
async def show_extra_photos(message: types.Message):
    mediagroup = types.MediaGroup()
    mediagroup.attach_photo(types.InputFile('./pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id)))
    mediagroup.attach_photo(types.InputFile('./pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id)))
    mediagroup.attach_photo(types.InputFile('./pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id)))
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    restart_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='download_photo_again')
    next_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='start_alogrithm_educating')
    inline_keyboard.row(next_button, restart_button)
    await bot.send_media_group(message.from_user.id, media=mediagroup)
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_SIDE_PHOTOS, reply_markup=inline_keyboard)

# UPLOADING PHOTOS TO SERVER
@dp.callback_query_handler(text='start_alogrithm_educating')
async def add_other_photos(query: types.CallbackQuery):
    # ----- блок отправки фотографий на сервер ------
    #
    # -----------------------------------------------
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    letsgo_button = types.InlineKeyboardButton(buttons_texts.LETS_GO, callback_data='rules_of_studing')
    inline_keyboard.add(letsgo_button)
    await query.message.edit_text(text=texts.START_EDUCATION, reply_markup=inline_keyboard)


@dp.callback_query_handler(text='rules_of_studing')
async def show_rules_of_studing(query: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    begin_button = types.InlineKeyboardButton(text=buttons_texts.BEGIN_BUTTON, callback_data='first_educational_photo')
    inline_keyboard.add(begin_button)
    await query.message.edit_text(text=texts.RULE_STUDING, reply_markup=inline_keyboard)


@dp.callback_query_handler(text='first_educational_photo')
@dp.callback_query_handler(text='unlike_educate_algorithm')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['algorithm_steps'] > 0 and data['likes'] > 0 and data['super_likes'] > 0:
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps'] > 0 and data['likes'] == 0 and data['super_likes'] > 0:
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps'] > 0 and data['likes'] > 0 and data['super_likes'] == 0:
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps'] > 0 and data['likes'] == 0 and data['super_likes'] == 0:
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    else:
        pass
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text='like_educate_algorithm')
async def second_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['algorithm_steps']-1 > 0 and data['likes']-1 > 0 and data['super_likes'] > 0:
        await state.update_data(likes=data['likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes']-1, data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps']-1 > 0 and data['likes']-1 == 0 and data['super_likes'] > 0:
        await state.update_data(likes=data['likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes']-1, data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
        pass
    elif data['algorithm_steps']-1 > 0 and data['likes']-1 > 0 and data['super_likes'] == 0:
        await state.update_data(likes=data['likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes']-1, data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
        pass
    elif data['algorithm_steps']-1 > 0 and data['likes']-1 == 0 and data['super_likes'] == 0:
        await state.update_data(likes=data['likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes']-1, data['super_likes']), show_alert=True)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
        pass
    else:
        pass


@dp.callback_query_handler(text='superlike_educate_algorithm')
async def third_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['algorithm_steps']-1 > 0 and data['likes'] > 0 and data['super_likes']-1 > 0:
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']-1), show_alert=True)
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps']-1 > 0 and data['likes'] == 0 and data['super_likes']-1 > 0:
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']-1), show_alert=True)
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps']-1 > 0 and data['likes'] > 0 and data['super_likes']-1 == 0:
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']-1), show_alert=True)
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    elif data['algorithm_steps']-1 > 0 and data['likes'] == 0 and data['super_likes']-1 == 0:
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
        await query.answer(text=buttons_texts.ANSWER_STUDY % (31-data['algorithm_steps'], data['likes'], data['super_likes']-1), show_alert=True)
        await state.update_data(super_likes=data['super_likes']-1)
        await state.update_data(algorithm_steps=data['algorithm_steps']-1)
        await state.reset_state(with_data=False)
        file = open('./pic/testing_thirty/%s.jpg' % (32-data['algorithm_steps']), 'rb')
        await query.message.delete()
        await bot.send_photo(data['chat_id'], photo=file, reply_markup=inline_keyboard)
    

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)    
