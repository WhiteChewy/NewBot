# -*- coding: utf-8 -*-
import os
import aioschedule
import logging
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json
import asyncio
import base64
import datetime
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import base64
import random
import db_interface as db
import comunication as com
import asyncpg
import aiohttp

from aiogram.dispatcher.filters import Filter
from User import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, DB_PASSWORD, DB_USER

#logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
conn = None


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
    
    help = State()
    why_dont_like=State()
    upload_photo_to_match = State()
    get_help_message = State()
    callback_other = State()
    unlike_meeting = State()
  
    confirm_leaving = State()
    new_match = State()
    has_match=State()
    one_day_to_unmatch = State()
    ending_match = State()
    no_match=State()
    stop_match = State()
  # GAME STATES
    game1 = State()
    game2 = State()
    game3 = State()
    game4 = State()
    game5 = State()
    game6 = State()
    game7 = State()
    game8 = State()
    game9 = State()
    game10 = State()
    game11 = State()
    game12 = State()
  # CHOOSE MEETING PLACE
    meeting_choose = State()
  # MEETING PLACE STATE FOR SPB
    spb_meeting = State()
  # MEETING PLACE STATE FOR MOSCOW
    msc_meeting = State()
  # PAYMENTS STATUS
    payment_cancel = State()        # отмена подписки
    payment_renew_fail = State()    # продление подписки неудачно
    payment_renew_success = State() # продление подписки успешно
    payment_ok = State()    # оплата успешна
    payment_ends = State()  # подписка закончилась
    payment_fail = State()  # отказ от оплаты


# =====================================================================================================================================================================================================
# |                                     SCHEDULER FUNCTIONS                                                                                                                                           |
# L___________________________________________________________________________________________________________________________________________________________________________________________________|
async def get_advice(id: int, state: FSMContext):
  r'''
  Hints scheduler
  '''
  first_day_hints = [texts.HINT_1,
                    texts.HINT_2,
                    texts.HINT_3,
                    texts.HINT_4,
                    texts.HINT_5,
                    ]
  hints = [texts.HINT_6,
          texts.HINT_7,
          texts.HINT_8,
          texts.HINT_9,
          texts.HINT_10
          ]
  random.shuffle(first_day_hints)
  random.shuffle(hints)
  if first_day_hints:
    if await db.is_matching(id, conn):
      await bot.send_message(id, text=first_day_hints.pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(id, state, ))
  elif hints:
    if await db.is_matching(id, conn):
      await bot.send_message(id, text=hints.pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(id, state, ))

async def is_match(id: int):
  r'''
  Get information about is user has match, or not. Return TRUE - if yes, FALSE - if no
  '''
  return await db.is_matching(id, conn)

async def is_premium(id: int):
  r'''
  Get information if user has subscribtion, or not. Return True - if yes, FALSE - if no
  '''
  return await db.is_subscribed(id, conn)

async def is_monday():
  r'''
  If today MONDAY return TRUE, if not return FALSE
  '''
  if not datetime.date.today().weekday():
    return True
  else:
    return False

async def set_state_unmatch(id: int, state: FSMContext):
  r'''
  This function set users matching status to False. Also edit this field in DB
  '''
  await db.set_match_status(id, conn, False)
  # --------------------------------------------------------
  # -------------POST request for some statistics-----------
  #requests.post(url='https://api.amplitude.com/2/httpapi', json={
  #"api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #"events": [
  #  {
  #    "user_id": message.from_user.id,
  #    "event_type": "match_stop_time_gone"
  #  }
  #]
#})
  # --------------------------------------------------------
  await state.reset_state(with_data=False)
  await Form.ending_match.set()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='callback_look')
  dont_like_comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='callback_comunication')
  like_button = types.InlineKeyboardButton(text=buttons_texts.LIKE_LOOK, callback_data='callback_like')
  other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='callback_other')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_comunication_button)
  keyboard.add(like_button)
  keyboard.add(other_button)
  await bot.send_message(id, text=texts.CALLBACK, reply_markup=keyboard)

async def set_state_one_day_to_unmatch(id: int, state: FSMContext):
  r'''Function to warn user that he has only one day left to comunicate with his match'''
  await state.reset_state(with_data=False)
  #scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=1), args=(state,))
  scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state,))
  await Form.has_match.set()
  await bot.send_message(id, text=texts.ONE_DAY_TO_UNMATCH % await db.get_name(await db.get_match_id(id, conn), conn))

async def set_state_has_match(id: int, state: FSMContext):
  r'''Set User matchinbg status as True and edit his profile in data base'''
  await state.update_data(has_match=True)
  await db.set_match_status(id, conn, True)
  #new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
  new_date = datetime.datetime.now() + datetime.timedelta(minutes=30)
  scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=new_date, args=(id, state,))
  await db.set_match_status(id, conn, True)
  await db.set_first_time_status(id, conn, False)
  await bot.send_message(id, text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  
  #--------------------------------------------------------------------------------------
  await Form.has_match.set()
  with open('/pic/find_match.png', 'rb') as img:
    await bot.send_photo(id, photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET) #, callback_data='wanna_meet')
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO) #, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST) #, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG) #, callback_data='end_dialog')
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  with open(await db.get_profile_photo(await db.get_match_id(id, conn), conn), 'rb') as profile_pic:
    await bot.send_photo(id, photo=profile_pic, caption=texts.MATCH_INFO % (await db.get_name(await db.get_match_id(id, conn), conn), await db.get_city(await db.get_match_id(id, conn), conn), await db.get_reason(await db.get_match_id(id, conn), conn)))
  await bot.send_message(id, text=texts.FIND_MATCH, reply_markup= keyboard)
  await get_advice(id, state)

async def schedule_jobs(id: int, state: FSMContext):
  r'''
  Time scheduler to unmatch and warn users by timer. Using AsyncIOScheduler
  '''
  # IF USER NOT SUBSCRIBED
  if not await is_premium(id):
    # IF TODAY IS MONDAY
    if await is_monday():
      if await is_match(id):
        # IF THERE IS MATCH GET INFO ABOUT

        scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=6), args=(id, state, ))
      else:
        scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=30), args=(id, state,))
    # IF TODAY IS NOT MONDAY
    else:
      # IF NOT MONDAY - REPEAT AFTER days_till_monday DAYS
      days_till_monday = 7 - datetime.date.today().weekday()
      new_date = datetime.date.today() + datetime.timedelta(days=days_till_monday)
      run_date = datetime.datetime.combine(new_date, datetime.time(hour=9, minute=0))
      scheduler.add_job(schedule_jobs, 'date', run_date=run_date, args=(id, state,)) # add job to scheduler
  # IF USER SUBSCRIBED
  else:
    if await is_match(id):
      # IF THERE IS MATCH GET INFO ABOUT
      
      await set_state_has_match(id, state)
    # IF THERE IS NO MATCH REPEAT AFTER 10 MINUTES
    else:
      scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=10), args=(id, state,))
      query = types.CallbackQuery
      await state.reset_state(with_data=False)
      keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
      if await db.is_subscribed(id, conn):
          subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
      else:
          subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
      write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
      were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
      if not await db.is_paused(id, conn):
        pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
      else:
        pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
      keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
      with open('pic/main_photo.png', 'rb') as img_file:
        await bot.send_photo(id, photo=img_file)
      if not await db.is_matching(id, conn):
        await Form.no_match.set()
      else:
        await Form.has_match.set()
      if not await db.is_paused(id, conn):
        await bot.send_message(id, text=texts.MAIN_MENU, reply_markup=keyboard)
      else:
        await bot.send_message(id, text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)


# BOT MESSAGES MECHANICS
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------   STARTING DIALOG   -----------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# WELCOME MESSAGE AND CHOICE GO TO REGISTRATION OR READ ABOUT PROJECT
@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
  r'''
  Connecting to database and schedule jobs
  '''
  global conn
  conn = await asyncpg.connect('postgresql://%s:%s@localhost/bot_tg' % (DB_USER, DB_PASSWORD))
  await db.table_ini(conn)
  await db.create_new_user(message.from_user.id, conn)
  await state.reset_state()
  await schedule_jobs(message.from_user.id, state=state)
  await show_starting_menu(message)

async def show_starting_menu(message: types.Message):
    photo = open('pic/start.jpg', 'rb')
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
    photo = open('pic/letsgo.jpg', 'rb')
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
    await db.set_name(message.from_user.id, conn, message.text) # set the profile name 
    #------------------------------------------------------------------------------
    # ---------------------POST request for some STATISTICS------------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
      "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
      "events": [
        {
          "user_id": message.from_user.id,
          "event_type": "bot_reg_name_sent",
          "user_properties": {
            "RegName": message.text 
            }
        }
      ]
      }) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state() # close the NAME state in STATE MACHINE
    # GENDER CHOOSE MESSAGE AND InlineKeyboard
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton(buttons_texts.GENDER_MALE[0], callback_data='male')
    female_button = types.InlineKeyboardButton(buttons_texts.GENDER_FEMALE[0], callback_data='female')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_GENDER, callback_data='other_gender')
    keyboard.add(male_button, female_button, under_construction_button)
    await bot.send_message(message.from_user.id, text=texts.GENDER_CHOOSE, reply_markup=keyboard)

# SET profile GENDER to MALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery, state: FSMContext):
    await db.set_gender(query.from_user.id, conn, buttons_texts.GENDER_MALE[1])
    #-------------------------------------------------------------------------------
    #--------------------------POST request for STATISTIC---------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": query.from_user.id,
#       "event_type": "bot_reg_gender_man_btn",
#       "user_properties": {
#         "Gender": "Мужчина"
#       }
#     }
#   ]
# })
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    # chek the date with POST request
    async with aiohttp.ClientSession() as session:
      async with session.get(url='https://server.unison.dating/check_date', params={'birthday':message.text}) as resp: print( await resp.text())
    # transform answer from string to json-format
    status = json.loads(await resp.text())
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.reset_state()
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    await db.set_birthday(message.from_user.id, conn, date)
    #------------------------------------------------------------------------------
    #-------------------POST request for some STATISTICS---------------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_birthday_sent",
      "user_properties": {
        "Birthday": message.text
      }
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton(buttons_texts.MOSCOW, callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton(buttons_texts.SAINT_PETERSBURG, callback_data='saint-p')
    samara_button = types.InlineKeyboardButton(buttons_texts.SAMARA, callback_data='samara')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_CITY, callback_data='other_city')
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
    await db.set_gender(query.from_user.id, buttons_texts.GENDER_FEMALE[1])
    #------------------------------------------------------------------------------
    #--------------------------POST request for STATISTIC--------------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_gender_woman_btn",
      "user_properties": {
        "Gender": "Женщина"
      }
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state()
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    # chek the date with POST requestg
    async with aiohttp.ClientSession() as session:
      async with session.get(url='https://server.unison.dating/check_date', params={'birthday':message.text}) as resp: print( await resp.text())
    # transform answer from string to json-format
    status = json.loads(await resp.text())
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    await db.set_birthday(message.from_user.id, conn, date)
    #------------------------------------------------------------------------------
    #-------------------POST request for some STATISTICS---------------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_birthday_sent",
      "user_properties": {
        "Birthday": message.text
      }
    }
  ]
}) as resp: print(await resp.text())
    
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    moscow_button = types.InlineKeyboardButton(buttons_texts.MOSCOW, callback_data='moscow')
    saint_p_button = types.InlineKeyboardButton(buttons_texts.SAINT_PETERSBURG, callback_data='saint-p')
    samara_button = types.InlineKeyboardButton(buttons_texts.SAMARA, callback_data='samara')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_CITY, callback_data='other_city')
    nomad_button = types.InlineKeyboardButton(buttons_texts.NOMAD, callback_data='nomad')
    keyboard.add(moscow_button)
    keyboard.add(saint_p_button)
    keyboard.add(samara_button)
    keyboard.add(under_construction_button)
    keyboard.add(nomad_button)
    bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)

@dp.callback_query_handler(text='subscribe')
async def subscribe_post_func(query: types.CallbackQuery, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_our_telegram_subscribe_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------

@dp.callback_query_handler(text='under_construction')
async def show_under_construction(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='other_city')
async def show_under_construction(message: types.Message, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_city_other_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='other_gender')
async def show_under_construction(message: types.Message, state: FSMContext):
    """
    THERE ARE TWO GENDERS
    """
    #------------------------------------------------------------------------------
    #------------------------POST request for some STATISTIC-----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_gender_other_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='friends')
async def show_under_construction(message: types.Message, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_purpose_friendship_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='no_duty')
async def show_under_construction(message: types.Message, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_purpose_hookup_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='other_reason')
async def show_under_construction(message: types.Message, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_purpose_difficult_to_answer_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

# SET city as Moscow and ASK about goal of the relationship
@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery, state: FSMContext):
    await db.set_city(query.from_user.id, conn, texts.MOSCOW)
    #------------------------------------------------------------------------------
    #---------------------    POST request for some STATISTIC    ------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_city_moscow_btn",
      "user_properties": {
        "City": "Москва"
      }
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='no_duty')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='other_reason')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET city as SAINT-PETERSBURG and ASK about goal of the relationship
@dp.callback_query_handler(text='saint-p')
async def add_saintp(query: types.CallbackQuery, state: FSMContext):
    await db.set_city(query.from_user.id, conn, texts.SAINT_PETERSBURG)
    #------------------------------------------------------------------------------
    #---------------------    POST request for some STATISTIC    ------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_city_peterburg_btn",
      "user_properties": {
        "City": "Санкт-Петербург"
      }
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='no_duty')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='other_reason')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET city as SAMARA and ASK about goal of the relationship
@dp.callback_query_handler(text='samara')
async def add_samara(query: types.CallbackQuery, state: FSMContext):
    await db.set_city(query.from_user.id, conn, texts.SAMARA)
    #------------------------------------------------------------------------------
    #---------------------    POST request for some STATISTIC    ------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_city_moscow_btn",
      "user_properties": {
        "City": "Самара"
      }
    }
  ]
 }) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='no_duty')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='other_reason')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# IF u change cities very often than we SET ur city as a nomad and ASK about goal of the relationship
@dp.callback_query_handler(text='nomad')
async def add_nomad(query: types.CallbackQuery, state= FSMContext):
    await db.set_city(query.from_user.id, conn, texts.NOMAD)
    #------------------------------------------------------------------------------
    #---------------------    POST request for some STATISTIC    ------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_city_moscow_btn",
      "user_properties": {
        "City": "Кочевник"
      }
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    seriously_button = types.InlineKeyboardButton(buttons_texts.SERIOUS_REL, callback_data='srsly')
    family_button = types.InlineKeyboardButton(buttons_texts.FAMILY, callback_data='family')
    friends_button = types.InlineKeyboardButton(buttons_texts.FRIENDS, callback_data='friends')
    withou_obligations_button = types.InlineKeyboardButton(buttons_texts.FREE_USE, callback_data='no_duty')
    no_answer_button = types.InlineKeyboardButton(buttons_texts.STUCK_ANSWER, callback_data='other_reason')
    keyboard.add(seriously_button)
    keyboard.add(family_button)
    keyboard.add(friends_button)
    keyboard.add(withou_obligations_button)
    keyboard.add(no_answer_button)
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET ur relationship goal as SERIOUS RELATIONSHIP and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='srsly')
async def add_reason_srsly(query: types.CallbackQuery, state: FSMContext):
    await db.set_reason(query.from_user.id, conn, texts.SERIOUS_REL)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_purpose_serious_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    recomendations_button = types.InlineKeyboardButton(buttons_texts.PHOTO_RECOMENDATION, callback_data='recomendations')
    download_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(recomendations_button)
    keyboard.add(download_photo_button)
    await query.message.edit_text(texts.MODERATION, reply_markup=keyboard)

# SET ur relationship goal as MAKING FAMILY and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='family')
async def add_reason_family(query: types.CallbackQuery):
    await db.set_reason(query.from_user.id, conn, texts.FAMILY)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_purpose_family_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
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
    await message.photo[-1].download(destination_file='pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id)) # DOWNLOADIN MAIN PHOTO 
    with open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'rb') as img:
      base64_img = base64.b64encode(img.read())
      await state.update_data(profile_photo = base64_img)
    await db.set_profile_photo(message.from_user.id, conn, base64_img.decode('utf-8'))
    os.remove(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id))
    await state.reset_state(with_data=False)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_profile_photo_sent"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='confirm_photo')
    again_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='upload_main_photo')
    keyboard.row(confirm_button, again_button)
    # img = open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'wb')
    # img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    # img.close()
    # with open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'rb') as img:
    #   await bot.send_photo(message.from_user.id, img)
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
async def show_recomendation(query: types.CallbackQuery, state:FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_reg_guidelines_btn"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)

# SHOWING base profile of user
@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery):
    text = '%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s' % (texts.FIRST_NAME ,await db.get_name(message.from_user.id, conn), texts.BIRTHDAY, await db.get_birthday(message.from_user.id, conn), texts.GENDER, await db.get_gender(message.from_user.id, conn), \
                                                                 texts.CITY, await db.get_city(message.from_user.id, conn), texts.REASON, await db.get_reason(message.from_user.id, conn))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    reg_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin')
    keyboard.row(reg_button, next_button)
    
    img = open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'wb')
    img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img.close()

    with open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'rb') as img:
      await bot.send_photo(message.from_user.id, photo=img, caption=text, reply_markup=keyboard)


# We need 3 photos from different sides of your face. UPLOADING FIRST and GIVING INFO about PHOTOS that service needs
@dp.callback_query_handler(text='upload_extra_photo')
async def upload_three_photo(message: types.Message):
    photo = open('pic/3photos.png', 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.EXTRA_PHOTOS)
    await Form.first_side_photo.set()
# IF ANSWER OF USER IS PHOTO and STATE first_side_photo is ACTIVE = UPLOAD 1st PHOTO TO SERVER and FINISH THE first side photo STATE IN STATE MACHINE and ACTIVATE second_side_photo STATE
@dp.message_handler(state=Form.first_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_first_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id))
    with open(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id), 'rb') as img:
      base64_img = base64.b64encode(img.read())
      await state.update_data(first_extra_photo = base64_img)
    await db.set_1st_extra_photo(message.from_user.id, conn, base64_img.decode('utf-8'))
    os.remove(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id))
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_profile_dataset_photo1_sent"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
    await Form.second_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE second_side_photo is ACTIVE = UPLOAD 2nd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_second_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id))
    with open(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id), 'rb') as img:
      base64_img = base64.b64encode(img.read())
      await state.update_data(second_extra_photo = base64_img)
    await db.set_2nd_extra_photo(message.from_user.id, conn, base64_img.decode('utf-8'))
    os.remove(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id))
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_profile_dataset_photo2_sent"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
    await Form.third_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE third_side_photo is ACTIVE = UPLOAD 3rd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_third_photo(message: types.Message, state: FSMContext):
    await message.photo[-1].download(destination_file='pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id))
    with open(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id), 'rb') as img:
      base64_img = base64.b64encode(img.read())
      await state.update_data(third_extra_photo = base64_img)
    await db.set_1st_extra_photo(message.from_user.id, conn, base64_img.decode('utf-8'))
    os.remove(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id))
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": message.from_user.id,
      "event_type": "bot_reg_profile_dataset_photo3_sent"
    }
  ]
}) as resp: print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    inline_keyboard = types.InlineKeyboardMarkup(resize_true = True)
    chek_button = types.InlineKeyboardButton(buttons_texts.CHECK_EXTRA_PHOTOS, callback_data='show_extra_photos')
    next_step_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='start_alogrithm_educating')
    inline_keyboard.row(chek_button, next_step_button)
    await bot.send_message(message.from_user.id, text=texts.ALL_PHOTOS, reply_markup=inline_keyboard)
    #--------------------------TRANSFORMIN IMGs TO  base64 string-------------------
    b64_profile_photo = await db.get_profile_photo(message.from_user.id, conn)
    b64_first_photo = await db.get_1st_extra_photo(message.from_user.id, conn)
    b64_second_photo = await db.get_2nd_extra_photo(message.from_user.id, conn)
    b64_third_photo = await db.get_3rd_extra_photo(message.from_user.id, conn)
    #-------------------------------------------------------------------------------
    #------------------POST request to upload photos to profile on server-----------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://server.unison.dating/user/add_photos/self?user_id=%s'%message.from_user.id, json={
  "main_photo": b64_profile_photo,
  "other_photos": [
    b64_first_photo,
    b64_second_photo,
    b64_third_photo
  ]
}) as resp: print(await resp.text())
    
    #-------------------------------------------------------------------------------
    #--------------    POST request to send profile to moderation    ---------------
    if not await db.is_moderated(message.from_user.id, conn) or not await db.is_photo_ok(message.from_user.id, conn) or not await db.is_info_ok(message.from_user.id, conn):
      async with aiohttp.ClientSession() as session:
        async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
  "chat_id": "-1001693622168",
  "text": "Пользователь требует ПОВТОРНОЙ модерации: \n UserID: %s; \n Имя: %s; \n Пол: %s; \n День рождения: %s; \n Город: %s; \n Цель знакомства: %s; " % 
                                                      (message.from_user.id, await db.get_name(message.from_user.id, conn), await db.get_gender(message.from_user.id, conn),
                                                      await db.get_birthday(message.from_user.id, conn), await db.get_city(message.from_user.id, conn), await db.get_reason(message.from_user.id, conn))
}) as resp: print(await resp.text())
    else:
      async with aiohttp.ClientSession() as session:
        async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
"chat_id":"-1001693622168",
"text": "Новый пользователь требует модерации: \n UserID: %s; \n Имя: %s; \n Пол: %s; \n День рождения: %s; \n Город: %s; \n Цель знакомства: %s; " % 
                                                (message.from_user.id, await db.get_name(message.from_user.id), await db.get_gender(message.from_user.id, conn),
                                                await db.get_birthday(message.from_user.id, conn), await db.get_city(message.from_user.id, conn), await db.get_reason(message.from_user.id, conn))

}) as resp: print(await resp.text())
    #-------------------------------------------------------------------------------
    #------   POST request to send profile main photo   ----------------------------
    img = open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'wb')
    img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img.close()

    with open(r'pic/profiles/%s/main_profile_photo.jpg' % (message.from_user.id), 'rb') as img:
      async with aiohttp.ClientSession() as session:
        async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendPhoto', json={
"chat_id":"-1001693622168",
"photo": img,
"caption":"Фото профиля"
}) as resp: print(await resp.text())
    #-------------------------------------------------------------------------------
    #---------------------    POST request to send additional photos    ------------
    img1 = open(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id), 'wb')
    img1.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img1.close()
    img1 = open(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id), 'rb')
    
    img2 = open(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id), 'wb')
    img2.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img2.close()
    img2 = open(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id), 'rb')

    img3 = open(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id), 'wb')
    img3.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img3.close()
    img3 = open(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id), 'rb')

    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMediaGroup', json={
  "chat_id": "-1001693622168",
  "media": [
    {
      "type": "photo",
      "media": img1,
      "caption": "Дополнительные фото"
    },
    {
      "type": "photo",
      "media": img2
    },
    {
      "type": "photo",
      "media": img3
    }
  ]
}) as resp: print(await resp.text())
    os.remove(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id))
    os.remove(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id))
    os.remove(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id))
  

# CONFIRMING EXTRA PHOTOS BEFORE UPLOADING
@dp.callback_query_handler(text='show_extra_photos')
async def show_extra_photos(message: types.Message):
    b64_first_photo = await db.get_1st_extra_photo(message.from_user.id, conn)
    b64_second_photo = await db.get_2nd_extra_photo(message.from_user.id, conn)
    b64_third_photo = await db.get_3rd_extra_photo(message.from_user.id, conn)
    #1
    img = open(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id), 'wb')
    img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img.close()
    #2
    img = open(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id), 'wb')
    img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img.close()
    #3
    img = open(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id), 'wb')
    img.write(base64.decodebytes(bytes(await db.get_profile_photo(message.from_user.id, conn), encoding='utf-8')))
    img.close()
    mediagroup = types.MediaGroup()
    mediagroup.attach_photo(types.InputFile('pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id)))
    mediagroup.attach_photo(types.InputFile('pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id)))
    mediagroup.attach_photo(types.InputFile('pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id)))
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    restart_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='download_photo_again')
    next_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='start_alogrithm_educating')
    inline_keyboard.row(next_button, restart_button)
    await bot.send_media_group(message.from_user.id, media=mediagroup)
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_SIDE_PHOTOS, reply_markup=inline_keyboard)
    os.remove(r'pic/profiles/%s/third_extra_photo.jpg' % (message.from_user.id))
    os.remove(r'pic/profiles/%s/second_extra_photo.jpg' % (message.from_user.id))
    os.remove(r'pic/profiles/%s/first_extra_photo.jpg' % (message.from_user.id))

# UPLOADING PHOTOS TO SERVER
@dp.callback_query_handler(text='start_alogrithm_educating')
async def add_other_photos(query: types.CallbackQuery):
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
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://server.unison.dating/user/init?user_id=%s'%query.from_user.id, json={
    "next_id": await db.get_algorithm_steps(query.from_user.id, conn) - 30
}) as resp: print (await resp.text())
    #---------------------------------------------------------------------------------------
    #------------------------------POST request for some STATISTICS-------------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_training_start_btn"
    }
  ]
}) as resp: print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    if await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    else:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-await db.get_algorithm_steps(query.from_user.id, conn), await db.get_likes(query.from_user.id, conn), await db.get_super_likes(query.from_user.id, conn)), show_alert=True)
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------POST request to GET PHOTO and MAKING DATASET--------------------------------------------------------
#     async with aiohttp.ClientSession() as session:
#       async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
#   "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
# }) as resp: print(await resp.text())
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    request = json.loads(await resp.text())
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%30-await db.get_algorithm_steps(query.from_user.id, conn), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='unlike_educate_algorithm')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    #---------------------------------------------------------------------------------------
    #--------------------------    POST request for some STATISTICS    ---------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_training_dislike_btn"
    }
  ]
}) as resp: print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    await state.reset_state(with_data=False)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    if await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn) > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    else:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-await db.get_algorithm_steps(query.from_user.id, conn), await db.get_likes(query.from_user.id, conn), await db.get_super_likes(query.from_user.id, conn)), show_alert=True)
#     async with aiohttp.ClientSession() as session:
#       async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
#   "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
#   "answer": {
#     30-await db.get_algorithm_steps(query.from_user.id, conn): "0"
#   }
# }) as resp: print(await resp.text())
    request = json.loads(await resp.text())
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%30-await db.get_algorithm_steps(query.from_user.id, conn), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='like_educate_algorithm')
async def second_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    #---------------------------------------------------------------------------------------
    #--------------------------    POST request for some STATISTICS    ---------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_training_like_btn"
    }
  ]
}) as resp: print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    await db.set_likes(query.from_user.id, conn, await db.get_likes(query.from_user.id)-1)
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
    if await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn)-1 > 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn)-1 == 0 and await db.get_super_likes(query.from_user.id, conn) > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn)-1 > 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn)-1 == 0 and await db.get_super_likes(query.from_user.id, conn) == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    else:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-await db.get_algorithm_steps(query.from_user.id, conn), await db.get_likes(query.from_user.id, conn)-1, await db.get_super_likes(query.from_user.id, conn)), show_alert=True)
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------POST request to GET PHOTO and MAKING DATASET--------------------------------------------------------
#     async with aiohttp.ClientSession() as session:
#       async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
#   "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
#   "answer": {
#     30-await db.get_algorithm_steps(query.from_user.id, conn): "1"
#   }
# }) as resp: print(await resp.text())
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    request = json.loads(await resp.text())
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%30-await db.get_algorithm_steps(query.from_user.id, conn), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='superlike_educate_algorithm')
async def third_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    #---------------------------------------------------------------------------------------
    #--------------------------    POST request for some STATISTICS    ---------------------
    async with aiohttp.ClientSession() as session:
      async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": query.from_user.id,
      "event_type": "bot_training_superlike_btnt"
    }
  ]
}) as resp: print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    await db.set_superlikes(query.from_user.id, conn, await db.get_super_likes(query.message.id, conn)-1)
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    if await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn)-1 > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn)-1 > 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn) > 0 and await db.get_super_likes(query.from_user.id, conn)-1 == 0:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    elif await db.get_algorithm_steps(query.from_user.id, conn)-1 > 0 and await db.get_likes(query.from_user.id, conn) == 0 and await db.get_super_likes(query.from_user.id, conn)-1 == 0:
        inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    else:
        super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='free')
        likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='free')
        unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final')
        inline_keyboard.row(likes_button, super_like_button)
        inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-await db.get_algorithm_steps(query.from_user.id, conn), await db.get_likes(query.from_user.id, conn), await db.get_super_likes(query.from_user.id, conn)-1), show_alert=True)
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------POST request to GET PHOTO and MAKING DATASET--------------------------------------------------------
#     async with aiohttp.ClientSession() as session:
#       async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
#   "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
#   "answer": {
#     30-await db.get_algorithm_steps(query.from_user.id, conn): "2"
#   }
# }) as resp: print(await resp.text())
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    request = json.loads(await resp.text())
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%30-await db.get_algorithm_steps(query.from_user.id, conn), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='final')
async def registration_final(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, text=texts.FINAL_MESSAGE)
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=scheduler.start())    
