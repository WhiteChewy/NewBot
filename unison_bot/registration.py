# -*- coding: utf-8 -*-
import logging
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json

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
    name = State()
    birthdate = State()
    profile_photo = State()
    first_side_photo = State()
    second_side_photo = State()
    third_side_photo = State()

# WELCOME MESSAGE and start button
@dp.message_handler(commands='start')
@dp.callback_query_handler(text='begin')
async def registration_begin(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton(buttons_texts.BEGIN_BUTTON, callback_data='begin_registration')
    keyboard.add(reg_button)
    photo = open('./pic/letsgo.jpg', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text= texts.LETS_GO, reply_markup=keyboard)

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
    async with state.proxy() as data:
        data['value'] = message.text
    
    user_form.fname = data['value'] # set the profile name 
    await state.finish() # close the NAME state in STATE MACHINE
    # GENDER CHOOSE MESSAGE AND InlineKeyboard
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton(buttons_texts.GENDER_MALE[0], callback_data='male')
    female_button = types.InlineKeyboardButton(buttons_texts.GENDER_FEMALE[0], callback_data='female')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_GENDER, callback_data='under_construction')
    keyboard.add(male_button, female_button, under_construction_button)
    await bot.send_message(message.chat.id, text=texts.GENDER_CHOOSE, reply_markup=keyboard)

# SET profile GENDER to MALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery):
    user_form.gender = buttons_texts.GENDER_MALE[1]
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = message.text
    # chek the date with POST request
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':data['birthdate']})
    # transform answer from string to json-format
    status = json.loads(request.text)
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    user_form.birthdate = data['birthdate']
    await state.finish() # finish the BIRTHDAY STATE in STATE MACHINE
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
async def show_female_menu(query: types.CallbackQuery):
    user_form.gender = buttons_texts.GENDER_FEMALE[1]
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = message.text
    # chek the date with POST requestg
    request = requests.get(url='https://server.unison.dating/check_date', params={'birthday':data['birthdate']})
    # transform answer from string to json-format
    status = json.loads(request.text)
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    user_form.birthdate = data['birthdate']
    await state.finish() # finish the BIRTHDAY STATE in STATE MACHINE
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
    keyboard.add(subscribe_button)
    keyboard.add(again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)


# SET city as Moscow and ASK about goal of the relationship
@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery):
    user_form.city = buttons_texts.MOSCOW[2:] # IF U CHANGE LANG CHECK EMOJI
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
async def add_saintp(query: types.CallbackQuery):
    user_form.city = buttons_texts.SAINT_PETERSBURG[2:] # IF U CHANGE LANG CHECK EMOJI
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
async def add_samara(query: types.CallbackQuery):
    user_form.city = buttons_texts.SAMARA[2:] # IF U CHANGE LANG CHECK EMOJI
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
async def add_nomad(query: types.CallbackQuery):
    user_form.city = buttons_texts.NOMAD[4:] # IF U CHANGE LANG CHECK EMOJI
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
async def add_reason_srsly(query: types.CallbackQuery):
    user_form.reason = buttons_texts.SERIOUS_REL[2:] # IF U CHANGE LANG CHECK EMOJI
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='recomendation')
    download_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# SET ur relationship goal as MAKING FAMILY and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='family')
async def add_reason_family(query: types.CallbackQuery):
    user_form.reason = buttons_texts.FAMILY[2:] # IF U CHANGE LANG CHECK EMOJI
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='recomendations')
    download_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# user uploads MAIN PHOTO of his profile. Activate the MAIN PHOTO STATE OF STATE MACHINE. CONFIRMING THE PHOTO
@dp.callback_query_handler(text='upload_main_photo')
async def ad_photo(query: types.CallbackQuery):
    await query.message.edit_text(texts.DOWNLOAD_PHOTO)
    await Form.profile_photo.set()
# DOWNLOADING MAIN PHOTO OF PROFILE. BECOURSE WE NEED TO FORWARD IT TO MODERATION CHAT
@dp.message_handler(state=Form.profile_photo, content_types=types.ContentTypes.PHOTO)
async def download_photo(message: types.Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await message.photo[-1].download(destination_file='./pic/profile/%s/main_profile_photo.jpg' % (str(message.from_user.id))) # DOWNLOADIN MAIN PHOTO 
    user_form.profile_photo = './pic/profile/%s/main_profile_photo.jpg' % (str(message.from_user.id)) # PATH to the MAIN PHOTO
    await state.finish() 
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='confirm_photo')
    again_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='upload_main')
    keyboard.add(confirm_button, again_button)
    await bot.send_photo(message.from_user.id, file_id)
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_PHOTO, reply_markup=keyboard)

# User MAKE the BASIC ACCOUNT. He can choose to check if nothing wrong or move to uploading extra photos
@dp.callback_query_handler(text='confirm_photo')
async def end_basic_registration(message: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    watch_profile_button = types.InlineKeyboardButton(buttons_texts.WATCH_PROFILE, callback_data='show_base_profile')
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    keyboard.add(watch_profile_button)
    keyboard.add(next_button)
    await bot.send_message(message.from_user.id, texts.BASE_PROFILE, reply_markup=keyboard)

# SHOWING recomendations to uploading PHOTOS
@dp.callback_query_handler(text='recomendations')
async def show_recomendation(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='download_main')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)

# SHOWING base profile of user
@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery):
    text = 'Name: %s\n\nBirthday: %s\n\nGender: %s\n\nCity: %s\n\nYou want from relationships: %s' % (user_form.fname, user_form.birthdate, user_form.gender, user_form.city, user_form.reason)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    reg_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin')
    keyboard.add(reg_button, next_button)
    await bot.send_photo(message.from_user.id, photo= user_form.profile_photo, caption=text, reply_markup=keyboard)


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
    await message.photo[-1].download(destination_file='./pic/profile/%s/first_extra_photo.jpg' % (str(message.from_user.id)))
    user_form.first_photo = './pic/profile/%s/first_extra_photo.jpg' % (str(message.from_user.id))
    await state.finish() 
    await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
    await Form.second_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE second_side_photo is ACTIVE = UPLOAD 2nd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_second_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='./pic/profile/%s/second_extra_photo.jpg' % (str(message.from_user.id)))
    user_form.second_photo = './pic/profile/%s/second_extra_photo_%s.jpg' % (str(message.from_user.id))
    await state.finish()
    await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
    await Form.third_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE third_side_photo is ACTIVE = UPLOAD 3rd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_third_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='./pic/profile/%s/third_extra_photo.jpg' % (str(message.from_user.id)))
    user_form.third_photo = './pic/profiles/%s/third_extra_photo.jpg' % (str(message.from_user.id))
    await state.finish()
    inline_keyboard = types.InlineKeyboardMarkup(resize_true = True)
    chek_button = types.InlineKeyboardButton(buttons_texts.CHECK_EXTRA_PHOTOS, callback_data='show_extra_photos')
    next_step_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='wait_moderation')
    inline_keyboard.add(chek_button)
    inline_keyboard.add(next_step_button)
    await bot.send_message(message.from_user.id, text=texts.ALL_PHOTOS, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='show_extra_photos')
async def show_extra_photos(message: types.Message):
    mediagroup = types.MediaGroup()
    mediagroup.attach_photo(types.InputFile('./pic/profile/first_extra_photo_%s.jpg' % (str(message.from_user.id))))
    mediagroup.attach_photo(types.InputFile('./pic/profile/second_extra_photo_%s.jpg' % (str(message.from_user.id))))
    mediagroup.attach_photo(types.InputFile('./pic/profile/third_extra_photo_%s.jpg' % (str(message.from_user.id))), texts.CONFIRMING_SIDE_PHOTOS)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    restart_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='download_photo_again')
    next_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='upload_extra_photo')
    inline_keyboard.row(next_button, restart_button)
    await bot.send_media_group(message.from_user.id, media=mediagroup, reply_markup=inline_keyboard)
    pass


@dp.callback_query_handler(text='next_button')
async def add_other_photos(query: types.CallbackQuery):
    # ----- блок отправки фотографий на сервер ------
    #
    # -----------------конец блока-------------------
    await query.answer('Фотографии успешно загруженны для модерации', show_alert=True)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendation_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='another_photos')
    upload_button = types.InlineKeyboardButton()
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
