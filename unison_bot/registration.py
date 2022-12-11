# -*- coding: utf-8 -*-
import os

import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json
import base64
import datetime
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import base64
import random
import db_interface as db
import asyncpg
import aiohttp
import re

from starting_menu import *
from pathlib import Path
#from aiogram.dispatcher.filters import Filter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, DB_PASSWORD, DB_USER, TESTING_TOKEN, BOT_MODERATOR

bot = Bot(token=TESTING_TOKEN)
moderator_bot = Bot(token=BOT_MODERATOR)
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

    extra_photo_1 = State()
    extra_photo_2 = State()
    extra_photo_3 = State()

# **************************************************************************************************************************************************************************************************
# ********************************GAME SECTION******************************************************************************************************************************************************
@dp.callback_query_handler(state = Form.game1)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_ONE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_ONE)

@dp.callback_query_handler(state = Form.game2)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TWO)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_TWO)
  
@dp.callback_query_handler(state = Form.game3)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_THREE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_THREE)
  
@dp.callback_query_handler(state = Form.game4)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_FOUR)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_FOUR)
  
@dp.callback_query_handler(state = Form.game5)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_FIVE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_FIVE)
  
@dp.callback_query_handler(state = Form.game6)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_SIX)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_SIX)
  
@dp.callback_query_handler(state = Form.game7)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_SIX)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_SIX)
  
@dp.callback_query_handler(state = Form.game8)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_EIGHT)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_EIGHT)
  
@dp.callback_query_handler(state = Form.game9)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_NINE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_NINE)
  
@dp.callback_query_handler(state = Form.game10)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TEN)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_TEN)
  
@dp.callback_query_handler(state = Form.game11)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_ELEVEN)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_ELEVEN)
  
@dp.callback_query_handler(state=Form.game12)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TWELVE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.GAME_TWELVE)
  
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************
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
  Get information if user has subscription, or not. Return True - if yes, FALSE - if no
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

async def set_state_unmatch(id: int, state: FSMContext, unmatch_menu=True):
  r'''
  This function set users matching status to False. Also edit this field in DB
  '''
  if not unmatch_menu:
    await db.set_match_status(id, conn, False)
    # --------------------------------------------------------
    # -------------POST request for some statistics-----------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": id,
    #         "event_type": "match_stop_time_gone"
    #       }
    #     ]
    #   }) as resp: pass
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
  else:
      await state.reset_state()
      await db.set_matching_pause_status(id, conn, False)
      await show_unpaused_no_match_menu(id)

async def set_state_one_day_to_unmatch(id: int, state: FSMContext):
  r'''Function to warn user that he has only one day left to comunicate with his match'''
  await state.reset_state()
  scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=1), args=(id, state, False, ))
  #scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state,))
  await Form.has_match.set()
  await bot.send_message(id, text=texts.ONE_DAY_TO_UNMATCH % await db.get_name(await db.get_match_id(id, conn), conn))

async def set_state_has_match(id: int, state: FSMContext):
    r'''Set User matchinbg status as True and edit his profile in data base'''
    await db.set_first_time_status(id, conn, False)
    await bot.send_message(id, text=texts.NEW_MATCH)
    #--------------------------------------------------------------------------------------
    #-----------------   getting match INFO   ---------------------------------------------
    match_id = await db.get_match_id(id, conn)
    match_name = await db.get_name(match_id, conn)
    match_city = await db.get_city(match_id, conn)
    match_reason = await db.get_reason(match_id, conn)
    #--------------------------------------------------------------------------------------
    #-----------------   getting photo of match   -----------------------------------------
    # with open(Path(r'profiles/%s/profile_photo.jpg'% match_id), 'wb') as prof_pic:
    #   b64_photo = await db.get_b64_profile_photo(match_id, conn)
    #   prof_pic = prof_pic.write(b64_photo)
    #-------   set_state_to_has_match   ---------------------------------------------------
    with open(Path('pic/find_match.png'), 'rb') as img:
      await bot.send_photo(id, photo=img)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET)
    send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO)
    send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST)
    end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG)
    keyboard.row(wanna_meet_button, send_photo_button)
    keyboard.row(send_request, end_dialog)
    with open(Path(r'profiles/%s/profile_photo.jpg'% match_id), 'rb') as profile_pic:
      await bot.send_photo(id, photo=profile_pic, caption=texts.MATCH_INFO % (match_name, match_city, match_reason))
    #os.remove(Path(r'profiles/%s/profile_photo.jpg'% match_id))
    await bot.send_message(id, text=texts.FIND_MATCH, reply_markup= keyboard)
    await get_advice(id, state)
    await Form.has_match.set()

async def schedule_jobs(id: int, state: FSMContext, edit = False, query = None, show_menu=True):
  r'''
  Time scheduler to unmatch and warn users by timer. Using AsyncIOScheduler
  '''
  # IF USER NOT SUBSCRIBED
  if not await is_premium(id):
    # IF TODAY IS MONDAY
    if await is_monday():
      # IF THERE IS MATCH FOR USER
      if await is_match(id):
          # SHEDULE WARNING ABOUT ENDING TIME
          if not await db.is_paused(id, conn):
              new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
              #new_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
              if not scheduler.get_job('unmatch_%s' % id):
                scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=new_date, args=(id, state, ), id='unmatch_%s' % id)
              # SHOW HAS MATCH STATUS
              await set_state_has_match(id, state)
      # IF THERE IS NO MATCH FOR USER BUT ITS STILL MONDAY
      else:
        if not await db.is_paused(id, conn):
          # SCHEDULE REPEATING THIS FUNCTION
          if not scheduler.get_job('check_%s' % id):
            scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=30), args=(id, state,), id='check_%s' % id)
          # SHOW UNMATCH MENU
          await set_state_unmatch(id, state)
    # IF TODAY IS NOT MONDAY
    else:
      # IF NOT MONDAY - REPEAT AFTER days_till_monday DAYS and SHOW UNMATCH MENU
      days_till_monday = 7 - datetime.date.today().weekday()
      new_date = datetime.date.today() + datetime.timedelta(days=days_till_monday)
      run_date = datetime.datetime.combine(new_date, datetime.time(hour=9, minute=0))
      if not scheduler.get_job('monday_%s' % id):
        scheduler.add_job(schedule_jobs, 'date', run_date=run_date, args=(id, state, False, ), id = 'monday_%s' % id) # add job to scheduler
      if show_menu:
        if not await db.is_paused(id, conn):
          if edit:
            await show_unpaused_no_match_menu(id, True, query)
          else:
            await show_unpaused_no_match_menu(id)
        else:
          if edit:
            await show_paused_menu(id, True, query)
          else:
            await show_paused_menu(id)
  # IF USER SUBSCRIBED
  else:
    if await is_match(id):
      # SHEDULE WARNING ABOUT ENDING TIME
      new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
      #new_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
      if not await db.is_paused(id, conn):
          if not scheduler.get_job('unmatch_%s' % id):
            scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=new_date, args=(id, state, ), id='unmatch_%s' % id)
      # SHOW HAS MATCH STATUS
          await set_state_has_match(id, state)
    # IF THERE IS NO MATCH REPEAT AFTER 10 MINUTES
    # SHOW UNMATCH
    else:
      await state.reset_state()
      if show_menu:
        if not await db.is_paused(id, conn):
          if edit:
            if not scheduler.add_job('check_%s' % id):
                scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=30), args=(id, state, False, ), id= 'check_%s' % id)
            await show_unpaused_no_match_menu(id, True, query)
          else:
            if not scheduler.add_job('check_%s' % id):
                scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=30), args=(id, state, False, ), id= 'check_%s' % id)
            await show_unpaused_no_match_menu(id)
        else:
          if edit:
            scheduler.remove_job(job_id='check_%s' % id, jobstore='default')
            await show_paused_menu(id, True, query)
          else:
            scheduler.remove_job(job_id='check_%s' % id, jobstore='default')
            await show_paused_menu(id)


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
  conn = await asyncpg.connect('postgresql://%s:%s@localhost/bot_db' % (DB_USER, DB_PASSWORD))
  await db.table_ini(conn)
  await db.create_new_user(message.from_user.id, conn)
  await db.set_algorithm_steps(message.from_user.id, conn, 30)
  await db.set_likes(message.from_user.id, conn, 7)
  await db.set_superlikes(message.from_user.id, conn, 5)
  await state.reset_state()
  await show_starting_menu(message.from_user.id)
  #await schedule_jobs(message.from_user.id, state=state)

async def show_unpaused_no_match_menu(id: int, edit=False, query=None):
    r'''
    Showing unpaused menu when server find matches
    If edit = False - menu will be send by separate message and query wil be None
    if edit = True - menu will edit message will be in query argument(MUST BE types.CallbackQuery)
    '''
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(id, conn):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscription')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscriptions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    keyboard.add(subscribes_button)
    keyboard.add(write_help)
    keyboard.add(were_in_telegram_button)
    keyboard.add(pause_button)
    if edit:
        await query.message.edit_text(text=texts.MAIN_MENU)
        await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
        await bot.send_message(id, text=texts.MAIN_MENU, reply_markup=keyboard)

async def show_paused_menu(id: int, edit=False, query=None):
    r'''
    Showing paused menu when server find matches
    If edit = False - menu will be send by separate message and query wil be None
    if edit = True - menu will edit message will be in query argument(MUST BE types.CallbackQuery)
    '''
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(id, conn):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscription')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscriptions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    keyboard.add(subscribes_button)
    keyboard.add(write_help)
    keyboard.add(were_in_telegram_button)
    keyboard.add(pause_button)
    if edit:
        await query.message.edit_text(text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)
    else:
        await bot.send_message(id, text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)

async def show_starting_menu(id: int):
    photo = open(Path('pic/start.jpg'), 'rb')
    starting_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    about_project_button = types.InlineKeyboardButton(buttons_texts.INFO_ABOUT_PROJECT, callback_data='back')
    starting_inline_keyboard.add(about_project_button)
    starting_inline_keyboard.add(registration_button)
    await bot.send_photo(id, photo)
    await bot.send_message(id, text=texts.WELCOME, reply_markup=starting_inline_keyboard)

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
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    uniqueness_inline_keyboard.add(back_button, registration_button)
    await query.message.edit_text(text=texts.UNIQUENESS, reply_markup=uniqueness_inline_keyboard)

# MESSAGE ABOUT WHAT IS IMPRINTING
@dp.callback_query_handler(text='imprint')
async def show_imprint(query: types.CallbackQuery):
    imprint_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    imprint_inline_keyboard.add(registration_button)
    imprint_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.IMPRINT, reply_markup=imprint_inline_keyboard)
            
# FIRST OF THREE MESSAGE WITH USER AGREEMENT
@dp.callback_query_handler(text='user_agreement_1')
async def show_user_agreement(query: types.CallbackQuery):
    user_agreement_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
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
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
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
    start_inline_keyboard.add(about_button)
    start_inline_keyboard.add(uniqueness_button)
    start_inline_keyboard.add(imprinting_button)
    user_agreement_button = types.InlineKeyboardButton(buttons_texts.USER_AGREEMENT, callback_data='user_agreement_1')
    faq_button = types.InlineKeyboardButton(buttons_texts.FAQ, callback_data='faq')
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    start_inline_keyboard.add(user_agreement_button)
    start_inline_keyboard.add(faq_button)
    start_inline_keyboard.add(registration_button)
    await query.message.edit_text(text=texts.ABOUT_MENU, reply_markup=start_inline_keyboard)

# MESSAGE ABOUT CONCEPT
@dp.callback_query_handler(text='concept')
async def show_concept(query: types.CallbackQuery):
    back_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    back_inline_keyboard.add(registration_button)
    back_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.CONCEPT, reply_markup=back_inline_keyboard)

# MESSAGE ABOUT USAGE OF USER PHOTO
@dp.callback_query_handler(text='photo')
async def show_photo(query: types.CallbackQuery):
    photo_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    photo_inline_keyboard.add(registration_button)
    photo_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.PHOTO, reply_markup=photo_inline_keyboard)

# MESSAGE ABOUT PAYING FOR SUBSCRIBE
@dp.callback_query_handler(text='find')
async def show_find(query: types.CallbackQuery):
    find_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    find_inline_keyboard.add(registration_button)
    find_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.FIND, reply_markup=find_inline_keyboard)

# MESSAGE FOR INVESTORS
@dp.callback_query_handler(text='investors')
async def show_investors(query: types.CallbackQuery):
    investors_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    investors_inline_keyboard.add(registration_button)
    investors_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.INVESTORS, reply_markup=investors_inline_keyboard)

# MESSAGE FOR JOURNALISTS
@dp.callback_query_handler(text='journalists')
async def show_journalists(query: types.CallbackQuery):
    journalists_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
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
    with open(Path('pic/letsgo.jpg'), 'rb') as photo:
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #   "events": [
    #     {
    #       "user_id": message.from_user.id,
    #       "event_type": "bot_reg_name_sent",
    #       "user_properties": {
    #         "RegName": message.text 
    #         }
    #     }
    #   ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state() # close the NAME state in STATE MACHINE
    # GENDER CHOOSE MESSAGE AND InlineKeyboard
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    male_button = types.InlineKeyboardButton(buttons_texts.GENDER_MALE[0], callback_data='male')
    female_button = types.InlineKeyboardButton(buttons_texts.GENDER_FEMALE[0], callback_data='female')
    under_construction_button = types.InlineKeyboardButton(buttons_texts.OTHER_GENDER, callback_data='other_gender')
    keyboard.add(male_button)
    keyboard.add(female_button)
    keyboard.add(under_construction_button)
    await bot.send_message(message.from_user.id, text=texts.GENDER_CHOOSE, reply_markup=keyboard)

# SET profile GENDER to MALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery, state: FSMContext):
    await db.set_gender(query.from_user.id, conn, buttons_texts.GENDER_MALE[1])
    #-------------------------------------------------------------------------------
    #--------------------------POST request for STATISTIC---------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_gender_man_btn",
    #         "user_properties": {
    #           "Gender": "Мужчина"
    #         }
    #       }
    #     ]
    #   }) as resp: pass
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    # check birthday string in format DD.MM.YYYY
    if not re.match(pattern=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', string=message.text):
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    # chek the date with POST request
    async with aiohttp.ClientSession() as session:
      async with session.get(url='https://server.unison.dating/check_date', params={'birthday':message.text}) as resp:
        status = json.loads(await resp.text())
        # print( await resp.text())
    # transform answer from string to json-format
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.reset_state()
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    await db.set_birthday(message.from_user.id, conn, date)
    #------------------------------------------------------------------------------
    #-------------------POST request for some STATISTICS---------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_birthday_sent",
    #         "user_properties": {
    #           "Birthday": message.text
    #         }
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    await db.set_gender(query.from_user.id, conn,  buttons_texts.GENDER_FEMALE[1])
    #------------------------------------------------------------------------------
    #--------------------------POST request for STATISTIC--------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_gender_woman_btn",
    #         "user_properties": {
    #         "Gender": "Женщина"
    #         }
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state()
    await query.message.edit_text(texts.BIRTHDATE)
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    if not re.match(pattern=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', string=message.text).span == (0, 10):
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    # chek the date with POST requestg
    async with aiohttp.ClientSession() as session:
      async with session.get(url='https://server.unison.dating/check_date', params={'birthday':message.text}) as resp: 
            # transform answer from string to json-format
        status = json.loads(await resp.text())
        # print( await resp.text())
    # server reply with string like '{"status":"ok","parsed_date":"YYYY-MM-DD"}' if date OK and '{"status":"invalid_date"}' if date is NOT OK
    if status['status'] != 'ok': # repeat if date is not OK.
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    await db.set_birthday(message.from_user.id, conn, date)
    #------------------------------------------------------------------------------
    #-------------------POST request for some STATISTICS---------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_birthday_sent",
    #         "user_properties": {
    #         "Birthday": message.text
    #       }
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # _____________________________________________________________________________
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_our_telegram_subscribe_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # _____________________________________________________________________________
    pass

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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_city_other_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_gender_other_btn"
    #       }
    #     ]
    #   }) as resp:  pass#print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_purpose_friendship_btn"
    #       }
    #     ]
    #   }) as resp: pass#print(await resp.text())
    #______________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='no_duty')
async def show_under_construction(message: types.Message, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_purpose_hookup_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # _____________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await bot.send_message(message.from_user.id, text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='reason_again')
async def reason_again(query: types.CallbackQuery, state: FSMContext):
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

@dp.callback_query_handler(text='other_reason')
async def show_under_construction(query: types.CallbackQuery, state: FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_purpose_difficult_to_answer_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # _____________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.CHANGE_REASON, callback_data='reason_again')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

# SET city as Moscow and ASK about goal of the relationship
@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery, state: FSMContext):
    await db.set_city(query.from_user.id, conn, texts.MOSCOW)
    #------------------------------------------------------------------------------
    #---------------------    POST request for some STATISTIC    ------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_city_moscow_btn",
    #         "user_properties": {
    #           "City": "Москва"
    #         }
    #       }
    #     ]
    #   }) as resp: pass#print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_city_peterburg_btn",
    #         "user_properties": {
    #         "City": "Санкт-Петербург"
    #       }
    #     }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_city_moscow_btn",
    #         "user_properties": {
    #           "City": "Самара"
    #         }
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_city_moscow_btn",
    #         "user_properties": {
    #           "City": "Кочевник"
    #         }
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #         {
    #           "user_id": query.from_user.id,
    #           "event_type": "bot_reg_purpose_serious_btn"
    #         }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # _____________________________________________________________________________
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_purpose_family_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
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
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id))
    await db.set_profile_photo(message.from_user.id, conn, img)
    await state.reset_state(with_data=False)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_profile_photo_sent"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='confirm_photo')
    again_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='upload_main_photo')
    keyboard.row(confirm_button, again_button)
    # await bot.send_photo(message.from_user.id, photo=await db.get_profile_photo(message.from_user.id, conn))
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
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_guidelines_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_PHOTO, callback_data='upload_main_photo')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)

# SHOWING base profile of user
@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery):
    text = '%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s\n\n%s: %s' % (texts.FIRST_NAME ,await db.get_name(message.from_user.id, conn),
                                                              texts.BIRTHDAY, await db.get_birthday(message.from_user.id, conn),
                                                              texts.GENDER, await db.get_gender(message.from_user.id, conn), \
                                                              texts.CITY,
                                                              await db.get_city(message.from_user.id, conn),
                                                              texts.REASON,
                                                              await db.get_reason(message.from_user.id, conn))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    reg_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin')
    keyboard.row(reg_button, next_button)
    img = await db.get_profile_photo(message.from_user.id, conn)
    await bot.send_photo(message.from_user.id, photo=img, caption=text, reply_markup=keyboard)


# We need 3 photos from different sides of your face. UPLOADING FIRST and GIVING INFO about PHOTOS that service needs
@dp.callback_query_handler(text='upload_extra_photo')
async def upload_three_photo(message: types.Message):
    photo = open(Path('pic/3photos.png'), 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.EXTRA_PHOTOS)
    await Form.first_side_photo.set()
# IF ANSWER OF USER IS PHOTO and STATE first_side_photo is ACTIVE = UPLOAD 1st PHOTO TO SERVER and FINISH THE first side photo STATE IN STATE MACHINE and ACTIVATE second_side_photo STATE
@dp.message_handler(state=Form.first_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_first_photo(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/first_photo.jpg' % message.from_user.id))
    await db.set_1st_extra_photo(message.from_user.id, conn, img)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_profile_dataset_photo1_sent"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
    await Form.second_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE second_side_photo is ACTIVE = UPLOAD 2nd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_second_photo(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/second_photo.jpg' % message.from_user.id))
    await db.set_2nd_extra_photo(message.from_user.id, conn, img)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_profile_dataset_photo2_sent"
    #       }
    #     ]
    #   }) as resp: pass # print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
    await Form.third_side_photo.set() # also we can use "state.next()"
# IF ANSWER OF USER IS PHOTO and STATE third_side_photo is ACTIVE = UPLOAD 3rd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.PHOTO)
async def upload_third_photo(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/third_photo.jpg' % message.from_user.id))
    await db.set_3rd_extra_photo(message.from_user.id, conn, img)
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_reg_profile_dataset_photo3_sent"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    await state.reset_state(with_data=False)
    inline_keyboard = types.InlineKeyboardMarkup(resize_true = True)
    chek_button = types.InlineKeyboardButton(buttons_texts.CHECK_EXTRA_PHOTOS, callback_data='show_extra_photos')
    next_step_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='start_alogrithm_educating')
    inline_keyboard.row(chek_button, next_step_button)
    await bot.send_message(message.from_user.id, text=texts.ALL_PHOTOS, reply_markup=inline_keyboard)
    with open(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id), 'rb') as profile:
        with open(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id), 'rb') as first:
            with open(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id), 'rb') as second:
                with open(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id), 'rb') as third:
                    b64_profile = base64.b64encode(profile.read())
                    b64_first = base64.b64encode(first.read())
                    b64_second = base64.b64encode(second.read())
                    b64_third = base64.b64encode(third.read())
                    await db.set_b64_profile_photo(message.from_user.id, conn, b64_profile)
                    await db.set_b64_1st_photo(message.from_user.id, conn, b64_first)
                    await db.set_b64_2nd_photo(message.from_user.id, conn, b64_second)
                    await db.set_b64_3rd_photo(message.from_user.id, conn, b64_third)
                    #-------------------------------------------------------------------------------
                    #--------------    POST request to send profile to moderation    ---------------
    # with open(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id), 'rb') as profile:
    #     with open(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id), 'rb') as first:
    #         with open(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id), 'rb') as second:
    #             with open(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id), 'rb') as third:
    #                 if await db.is_moderated(message.from_user.id, conn):
    #                   if not await db.is_photo_ok(message.from_user.id, conn) or not await db.is_info_ok(message.from_user.id, conn):
    #                       await moderator_bot.send_message(-1001693622168, text=texts.REMODERATION % (message.from_user.id,
    #                                                         await db.get_name(message.from_user.id, conn),
    #                                                         await db.get_gender(message.from_user.id, conn),
    #                                                         await db.get_birthday(message.from_user.id, conn),
    #                                                         await db.get_city(message.from_user.id, conn),
    #                                                         await db.get_reason(message.from_user.id, conn)))
    #                   else:
    #                       await moderator_bot.send_message(-1001693622168, text=texts.NEW_MODERATION % (message.from_user.id,
    #                                                         await db.get_name(message.from_user.id, conn),
    #                                                         await db.get_gender(message.from_user.id, conn),
    #                                                         await db.get_birthday(message.from_user.id, conn),
    #                                                         await db.get_city(message.from_user.id, conn),
    #                                                         await db.get_reason(message.from_user.id, conn)))
    #                 #-------------------------------------------------------------------------------
    #                 #------   POST request to send profile main photo   ----------------------------
    #                 img = await db.get_profile_photo(message.from_user.id, conn)
    #                 await moderator_bot.send_photo(-1001693622168, profile, caption=texts.PROFILE_PHOTO)
    #                 #-------------------------------------------------------------------------------
    #                 #-------------------------------------------------------------------------------
    #                 #------------------POST request to upload photos to profile on server-----------
    #                 # async with aiohttp.ClientSession() as session:
    #                 #   async with session.post(url='https://server.unison.dating/user/add_photos/self?user_id=%s' % message.from_user.id, json={
    #                 #       "main_photo": await db.get_profile_photo(message.from_user.id, conn),#str(b64_profile),
    #                 #       "other_photos": [
    #                 #         await db.get_1st_extra_photo(message.from_user.id, conn),#str(b64_first),
    #                 #         await db.get_2nd_extra_photo(message.from_user.id, conn),#str(b64_second),
    #                 #         await db.get_3rd_extra_photo(message.from_user.id, conn)#str(b64_third)
    #                 #       ]
    #                 #   }) as resp: pass#print(await resp.text())
    #                 #---------------------    POST request to send additional photos    ------------
    #                 media = types.MediaGroup()
    #                 media.attach_photo(first, texts.SIDE_PHOTOS)
    #                 media.attach_photo(second)
    #                 media.attach_photo(third)
    #                 await moderator_bot.send_media_group(-1001693622168, media=media)
    # keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    # confirm = types.InlineKeyboardButton(text=buttons_texts.CONFIRM_PROFILE, url='https://server.unison.dating/moder/pass?user_id=%s' % message.from_user.id)
    # deny_info = types.InlineKeyboardButton(text=buttons_texts.DENY_INFO, url='https://server.unison.dating/moder/info_no_pass?user_id=%s' % message.from_user.id)
    # deny_photo = types.InlineKeyboardButton(text=buttons_texts.DENY_PHOTO, url='https://server.unison.dating/moder/photo_no_pass?user_id=%s' % message.from_user.id)
    # deny_all = types.InlineKeyboardButton(text=buttons_texts.DENY_ALL, url='https://server.unison.dating/moder/no_pass?user_id=%s' % message.from_user.id)
    # keyboard.add(confirm)
    # keyboard.add(deny_info)
    # keyboard.add(deny_photo)
    # keyboard.add(deny_all)
    # await moderator_bot.send_message(-1001693622168, text=texts.MODERATE_BOT, reply_markup=keyboard)
    os.remove(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id))
    os.remove(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id))
    os.remove(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id))
    os.remove(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id))
  

# CONFIRMING EXTRA PHOTOS BEFORE UPLOADING
@dp.callback_query_handler(text='show_extra_photos')
async def show_extra_photos(message: types.Message):
    #1
    img1 = await db.get_1st_extra_photo(message.from_user.id, conn)
    #2
    img2 = await db.get_2nd_extra_photo(message.from_user.id, conn)
    #3
    img3 = await db.get_3rd_extra_photo(message.from_user.id, conn)
    mediagroup = types.MediaGroup()
    mediagroup.attach_photo(img1)
    mediagroup.attach_photo(img2)
    mediagroup.attach_photo(img3)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    restart_button = types.InlineKeyboardButton(buttons_texts.NO, callback_data='upload_extra_photo')
    next_button = types.InlineKeyboardButton(buttons_texts.YES, callback_data='start_alogrithm_educating')
    inline_keyboard.row(next_button, restart_button)
    await bot.send_media_group(message.from_user.id, media=mediagroup)
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_SIDE_PHOTOS, reply_markup=inline_keyboard)


# UPLOADING PHOTOS TO SERVER
@dp.callback_query_handler(text='start_alogrithm_educating')
async def add_other_photos(query: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    letsgo_button = types.InlineKeyboardButton(buttons_texts.LETS_GO, callback_data='rules_of_studing')
    inline_keyboard.add(letsgo_button)
    await query.message.edit_text(text=texts.START_EDUCATION, reply_markup=inline_keyboard)

# ---------- EDUCATING ALGORITHM -----------------------------------------------------------------------
@dp.callback_query_handler(text='rules_of_studing')
async def show_rules_of_studing(query: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    begin_button = types.InlineKeyboardButton(text=buttons_texts.BEGIN_BUTTON, callback_data='first_educational_photo')
    inline_keyboard.add(begin_button)
    await query.message.edit_text(text=texts.RULE_STUDING, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='first_educational_photo')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s'%query.from_user.id, json={
    #       "next_id": await db.get_algorithm_steps(query.from_user.id, conn) - 30
    #   }) as resp: pass #print (await resp.text())
    #---------------------------------------------------------------------------------------
    #------------------------------POST request for some STATISTICS-------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_training_start_btn"
    #       }
    #     ]     
    #   }) as resp: pass#print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id, conn)
    likes = await db.get_likes(query.from_user.id, conn)
    super_likes = await  db.get_super_likes(query.from_user.id, conn)
    super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
    likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
    inline_keyboard.row(likes_button, super_like_button)
    inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-steps, likes, super_likes), show_alert=True)
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------POST request to GET PHOTO and MAKING DATASET--------------------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
    #     "next_id": 31-steps,
    #   }) as resp: 
    #       request = json.loads(await resp.text()) 
    #      #print(await resp.text())
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'% (31 - steps), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='unlike_educate_algorithm')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    # --------------------------------------------------------------------------------------
    # -------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_training_dislike_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # ______________________________________________________________________________________
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id, conn)
    likes = await db.get_likes(query.from_user.id, conn)
    super_likes = await  db.get_super_likes(query.from_user.id, conn)
    if steps > 1:
        if  likes > 0:
            if super_likes > 0:
              # if steps and likes and super_likes are ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
                # if setps and likes are ok and super_likes are =< 0
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        else:
          # if steps are ok likes are not ok and superlikes are ok
            if super_likes > 0:
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
          # if steps are ok and likes and superlikes are not ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    # if last step
    else:
        # have likes
        if likes > 0:
          # and super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # and no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        # have no likes
        else:
          # have super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-steps, likes, super_likes), show_alert=True)
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
    #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
    #     "answer": {
    #       30-steps: "0"
    #     }
    #   }) as resp: 
    #       response = json.loads(await resp.text()) 
    #       #print(await resp.text())
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=response['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%(31-steps), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='like_educate_algorithm')
async def second_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    # --------------------------------------------------------------------------------------
    # -------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_training_like_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # ______________________________________________________________________________________
    await db.set_likes(query.from_user.id, conn, await db.get_likes(query.from_user.id, conn)-1)
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id, conn)
    likes = await db.get_likes(query.from_user.id, conn)
    super_likes = await  db.get_super_likes(query.from_user.id, conn)
    if steps > 1:
        if  likes > 0:
            if super_likes > 0:
              # if steps and likes and super_likes are ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
                # if setps and likes are ok and super_likes are =< 0
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        else:
          # if steps are ok likes are not ok and superlikes are ok
            if super_likes > 0:
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
          # if steps are ok and likes and superlikes are not ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    # if last step
    else:
        # have likes
        if likes > 0:
          # and super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # and no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        # have no likes
        else:
          # have super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-steps, likes, super_likes), show_alert=True)
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #--------------------------------------------------POST request to GET PHOTO and MAKING DATASET--------------------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
    #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
    #     "answer": {
    #       30-steps: "1"
    #     }
    #   }) as resp: 
    #     request = json.loads(await resp.text())
          #print(await resp.text())
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg' % (31-steps), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='superlike_educate_algorithm')
async def third_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    #---------------------------------------------------------------------------------------
    #--------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_training_superlike_btnt"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #---------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------
    await db.set_superlikes(query.from_user.id, conn, await db.get_super_likes(query.from_user.id, conn)-1)
    await db.set_algorithm_steps(query.from_user.id, conn, await db.get_algorithm_steps(query.from_user.id, conn)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id, conn)
    likes = await db.get_likes(query.from_user.id, conn)
    super_likes = await  db.get_super_likes(query.from_user.id, conn)
    if steps > 1:
        if  likes > 0:
            if super_likes > 0:
              # if steps and likes and super_likes are ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
                # if setps and likes are ok and super_likes are =< 0
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        else:
          # if steps are ok likes are not ok and superlikes are ok
            if super_likes > 0:
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            else:
          # if steps are ok and likes and superlikes are not ok
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='unlike_educate_algorithm')
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    # if last step
    else:
        # have likes
        if likes > 0:
          # and super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # and no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='final_like')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
        # have no likes
        else:
          # have super likes
            if super_likes > 0:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='final_super_like')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
            # no super likes
            else:
                super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='no_superlikes')
                likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='no_likes')
                unlike_button = types.InlineKeyboardButton(buttons_texts.UNLIKE, callback_data='final_unlike')
                inline_keyboard.row(likes_button, super_like_button)
                inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-steps, likes, super_likes), show_alert=True)
    # -----------------------------------------------------------------------------------------------------------------------------------------------------
    # ----------------------------------------------   POST request to GET PHOTO and MAKING DATASET   -----------------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s' % query.from_user.id, json={
    #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id, conn),
    #     "answer": {
    #       30-await db.get_algorithm_steps(query.from_user.id, conn): "2"
    #     }
    #   }) as resp: 
    #        request = json.loads(await resp.text())
    #        print(await resp.text())
    # _____________________________________________________________________________________________________________________________________________________

    await query.message.delete()
    #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
    with open('pic/testing_thirty/%s.jpg'%(31-steps), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)

@dp.callback_query_handler(text='final_like')
async def registration_final(message: types.Message, state: FSMContext):
    # --------------------------------------------------------------------------------------
    # -------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_training_like_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # ______________________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
    skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
    keyboard.add(extra_photo)
    keyboard.add(skip)
    await bot.send_message(message.chat.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
    # await schedule_jobs(message.from_user.id, state=state)

@dp.callback_query_handler(text='final_super_like')
async def registration_final(message: types.Message, state: FSMContext):
    # --------------------------------------------------------------------------------------
    # -------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_training_superlike_btnt"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # ______________________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
    skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
    keyboard.add(extra_photo)
    keyboard.add(skip)
    await bot.send_message(message.chat.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
    # await schedule_jobs(message.from_user.id, state=state)

@dp.callback_query_handler(text='final_unlike')
async def registration_final(message: types.Message, state: FSMContext):
    # --------------------------------------------------------------------------------------
    # -------------------------    POST request for some STATISTICS    ---------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_training_dislike_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    # ______________________________________________________________________________________
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
    skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
    keyboard.add(extra_photo)
    keyboard.add(skip)
    await bot.send_message(message.from_user.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
    # await schedule_jobs(message.from_user.id, state=state)

@dp.callback_query_handler(text='no_superlikes')
async def no_superlikes(query: types.CallbackQuery):
    await query.answer(text=texts.NO_SUPERLIKES)

@dp.callback_query_handler(text='no_likes')
async def no_likes(query: types.CallbackQuery):
    await query.answer(text=texts.NO_LIKES)

@dp.callback_query_handler(text='skip')
async def skip(message: types.Message, state: FSMContext):
    await schedule_jobs(message.from_user.id, state=state)

# ========= Uploading photos of persons who user likes =================================================
@dp.callback_query_handler(text='likes_photo')
async def likes_photo(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    photo_recomendation = types.InlineKeyboardButton(text=buttons_texts.PHOTO_RECOMENDATION, callback_data='ex_recomendations')
    upload_photos = types.InlineKeyboardButton(text=buttons_texts.UPLOAD_EXTRA_PHOTO, callback_data='upload_extra')
    keyboard.add(photo_recomendation)
    keyboard.add(upload_photos)
    await query.message.edit_text(text=texts.EX_PHOTOS, reply_markup=keyboard)

@dp.callback_query_handler(text='upload_extra')
async def upload_extra(query: types.CallbackQuery):
    await query.message.edit_text(text=texts.FIRST_EX_PHOTOS)
    await Form.extra_photo_1.set()
@dp.message_handler(state=Form.extra_photo_1, content_types=types.ContentTypes.PHOTO)
async def extra_photo_1(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id))
    with open(Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
        b64_str = base64.b64encode(photo.read())
        await db.set_b64_likes_photo_1(message.from_user.id, conn, b64_str)
    os.remove(Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id))
    await state.reset_state()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_photo = types.InlineKeyboardButton(text=buttons_texts.SECOND_EXTRA, callback_data='second_extra')
    end_photo = types.InlineKeyboardButton(text=buttons_texts.STOP_UPLOADING, callback_data='stop_uploading')
    keyboard.add(next_photo)
    keyboard.add(end_photo)
    await bot.send_message(message.from_user.id, text=texts.SECOND_EXTRA_PHOTO, reply_markup=keyboard)

@dp.callback_query_handler(text='second_extra')
async def second_extra(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text=texts.SECOND_EX_PHOTO)
    await Form.extra_photo_2.set()
@dp.message_handler(state=Form.extra_photo_2, content_types=types.ContentTypes.PHOTO)
async def extra_photo_second(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id))
    with open(Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
        b64_str = base64.b64encode(photo.read())
        await db.set_b64_likes_photo_2(message.from_user.id, conn, b64_str)
    os.remove(Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id))
    await state.reset_state()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_photo = types.InlineKeyboardButton(text=buttons_texts.THIRD_EXTRA, callback_data='third_extra')
    end_photo = types.InlineKeyboardButton(text=buttons_texts.STOP_UPLOADING, callback_data='stop_uploading')
    keyboard.add(next_photo)
    keyboard.add(end_photo)
    await bot.send_message(message.from_user.id, text=texts.THIRD_EXTRA_PHOTO, reply_markup=keyboard)

@dp.callback_query_handler(text='third_extra')
async def third_extra(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, text=texts.THIRD_EX_PHOTOS)
    await Form.extra_photo_3.set()
@dp.message_handler(state=Form.extra_photo_3, content_types=types.ContentTypes.PHOTO)
async def extra_photo_third(message: types.Message, state: FSMContext):
    img = message.photo[-1].file_id
    await message.photo[-1].download(destination_file=Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id))
    with open(Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
        b64_str = base64.b64encode(photo.read())
        await db.set_b64_likes_photo_3(message.from_user.id, conn, b64_str)
    os.remove(Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id))
    await state.reset_state()
    await schedule_jobs(message.from_user.id, state)

@dp.callback_query_handler(text='stop_uploading')
async def stop_uploading(message: types.Message, state: FSMContext):
    await schedule_jobs(message.from_user.id, state)

@dp.callback_query_handler(text='ex_recomendations')
async def show_recomendation(query: types.CallbackQuery, state:FSMContext):
    #------------------------------------------------------------------------------
    #-------------------------POST request for some STATISTIC----------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_reg_guidelines_btn"
    #       }
    #     ]
    #   }) as resp: pass #print(await resp.text())
    #------------------------------------------------------------------------------
    #------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    upload_photo_button = types.InlineKeyboardButton(buttons_texts.UPLOAD_EXTRA_PHOTO, callback_data='upload_extra')
    keyboard.add(upload_photo_button)
    await query.message.edit_text(texts.PHOTO_RECOMENDATION, reply_markup=keyboard)
# ______________________________________________________________________________________________________


@dp.message_handler(commands='start_no_match')
async def registration_final(message: types.Message, state: FSMContext):
    global conn
    conn = await asyncpg.connect('postgresql://%s:%s@localhost/bot_db' % (DB_USER, DB_PASSWORD))
    await bot.send_message(message.chat.id, text=texts.FINAL_MESSAGE)
    await db.set_matching_pause_status(message.from_user.id, conn, False)
    await schedule_jobs(message.from_user.id, state=state)
    #scheduler.start()
#+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#|                               WAITING FOR MATCH                                                                                                                            |
#L____________________________________________________________________________________________________________________________________________________________________________l
# IF sheduler set state no_match as active 
@dp.message_handler(state=Form.no_match)
async def messaging_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(message.from_user.id, conn):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscription')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscriptions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not await db.is_paused(message.from_user.id, conn): 
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    if not await db.is_matching(message.from_user.id, conn):
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    if not await db.is_paused(message.from_user.id, conn):
      await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=keyboard)
    else:
      await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.no_match)
async def message_reaction_if_text(message: types.Message):
  if message.text == buttons_texts.MAIN_MENU and not await db.is_matching(message.from_user.id, conn):
    if await db.is_paused(message.from_user.id, conn):
      await show_paused_menu(message.from_user.id)
    else:
      await show_unpaused_no_match_menu(message.from_user.id)

@dp.callback_query_handler(text='main_menu')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    if not await db.is_paused(query.from_user.id, conn):
      await show_unpaused_no_match_menu(query.from_user.id, edit=True, query=query)
    else:
      await show_paused_menu(query.from_user.id, edit=True, query=query)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                       checking, getting and cancel subscription                                                                                                          |
# L__________________________________________________________________________________________________________________________________________________________________________l   
# If user have subscription let him to unsubscribe
@dp.callback_query_handler(text='have_subscription')
async def abandon_subsribtion(query: types.CallbackQuery):
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #     {
    #     "user_id": query.from_user.id,
    #     "event_type": "bot_menu_subscribe_btn"
    #     }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    abandon_button = types.InlineKeyboardButton(text=buttons_texts.DENY, callback_data='deny_subscribtion')
    back_button = types.InlineKeyboardButton(text=buttons_texts.BACK, callback_data='main_menu')
    keyboard.add(abandon_button, back_button)
    await query.message.edit_text(text=texts.WHAT_TO_DO)
    await query.message.edit_reply_markup(reply_markup=keyboard)
# If user doesnt have subscription ascks him if he want subscription
@dp.callback_query_handler(text='doesnt_have_subscriptions')
async def subscribe(query: types.CallbackQuery):
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #   "events": [
    #     {
    #       "user_id": query.from_user.id,
    #       "event_type": "bot_menu_subscribe_btn"
    #     }
    #   ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    get_subscribe = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSCRIBE, callback_data='subscribe')
    back_button = types.InlineKeyboardButton(text=buttons_texts.BACK, callback_data='main_menu')
    keyboard.row(back_button, get_subscribe)
    await query.message.edit_text(text=texts.SUBSCRIBE_INFO)
    await query.message.edit_reply_markup(reply_markup=keyboard)
# Get subscription
@dp.callback_query_handler(text='subscribe')
async def pay_subscribe(query: types.CallbackQuery):
    #--------------------------------------------------------------------------------------
    #----------------------POST request for getting payment url----------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/payment/request?user_id=%s' % query.from_user.id, json={
    #     "amount": "870"
    #   }) as resp:
    #     payment = json.loads(await resp.text())
    #     await db.set_payment_url(query.from_user.id, conn, payment['url'])
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
    keyboard.add(main_menu_button)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #   "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_subscribe_pay_btn"
    #       }
    #     ]
    #   }) as resp: pass
    #______________________________________________________________________________________
    await query.message.edit_text(texts.PAY_URL % await db.get_payment_url(query.from_user.id, conn))
    await query.message.edit_reply_markup(reply_markup=keyboard) 

@dp.callback_query_handler(text='deny_subscribtion')
async def abbandon_subscribe(query: types.CallbackQuery):
    await db.set_subscribtion_status(query.from_user.id, conn, False)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #       "user_id": query.from_user.id,
    #       "event_type": "bot_subscribe_cancel"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------   
    #----------------------POST request for some statistics--------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/payment/cancel?user_id%s' % query.from_user.id, json={}) as resp: pass
    #-------------------------------------------------------------------------------------- 
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    back_button = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
    keyboard.add(back_button)
    await query.message.edit_text(text=texts.PAYMENT_CANCEL)
    await query.message.edit_reply_markup(reply_markup=keyboard)

# ===========================================================================================================================================================================+
# |                        HELP USER                                                                                                                                         |
# L__________________________________________________________________________________________________________________________________________________________________________l
@dp.callback_query_handler(text='help')
async def get_help(query: types.CallbackQuery, state: FSMContext):
  await db.set_help_status(query.from_user.id, conn, True)
  await state.reset_state(with_data=False)
  #-------------------------------------------------------------------------
  #----------------------POST request for some STATISTICS-------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #        "user_id": query.from_user.id,
  #         "event_type": "bot_menu_support_btn"
  #       }
  #     ]
  #   }) as resp: pass
  await query.message.edit_text(text=texts.GET_HELP)
  await Form.help.set()
@dp.message_handler(state=Form.help, content_types=types.ContentTypes.TEXT)
async def help_message(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  # ------------------------------------------------------------------------
  # -----------------   FORWARDING HELP   ----------------------------------
  async with aiohttp.ClientSession() as session:
    async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
      "chat_id": "-776565232",
      "text": texts.HELP_MESSAGE % (message.from_user.id, 
                                    await db.get_name(message.from_user.id, conn), 
                                    message.text, 
                                    '[Profile ](tg://user?id=%s)' % message.from_user.id)
    }) as resp: pass
  # ________________________________________________________________________
  await db.set_help_status(message.from_user.id, conn, False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  back = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
  keyboard.add(back)
  await bot.send_message(message.from_user.id, text=texts.AFTER_HELP, reply_markup=keyboard)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                         TELEGRAM NEWS URL                                                                                                                                |
# L__________________________________________________________________________________________________________________________________________________________________________l
@dp.callback_query_handler(text='our_telegram')
async def send_telegram_url(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  subscribe_button = types.InlineKeyboardButton(text=buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='user_pressed_tg')
  back_button = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
  keyboard.add(subscribe_button)
  keyboard.add(back_button)
  await query.message.edit_text(text=texts.OUR_TG, reply_markup=keyboard)
@dp.callback_query_handler(text='user_pressed_tg')
async def request_when_tg_pressed(message: types.Message):
  #-------------------------------------------------------------------------
  #-------------POST request for some STATISTICS-----------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_our_telegram_subscribe_btn"
  #       }
  #     ]
  #   }) as resp: pass
  pass

# +=========================================================================================================================================================================+
# |                         PAUSE FINDING MATCH                                                                                                                             |
# L_________________________________________________________________________________________________________________________________________________________________________l
# Main menu when user pause finding his match
@dp.callback_query_handler(text='paused_main_menu')
async def pause_menu(query: types.CallbackQuery, state: FSMContext):
  await state.reset_state()
  await db.set_matching_pause_status(query.from_user.id, conn, True)
  #-------------------------------------------------------------------------
  #---------------------POST request for STATISTIC--------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi',json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": query.from_user.id,
  #         "event_type": "bot_menu_pause_btn"
  #       }
  #     ]
  #   }) as resp: pass
  #---------------------POST request to END finding match-------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/pause?user_id=%s' % query.from_user.id, json={"pause": "true"}) as resp: pass
  #-------------------------------------------------------------------------
  await schedule_jobs(query.from_user.id, state, edit=True, query=query)


# Main menu when user in proces of finding his match
@dp.callback_query_handler(text='unpaused_main_menu')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    await db.set_matching_pause_status(query.from_user.id, conn, False)
    #-------------------------------------------------------------------------
    #---------------------POST request for STATISTIC--------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_menu_resume_btn"
    #       }
    #     ]     
    #   }) as resp: pass
    #------------------   POST request to UNPAUSE finding   ------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/pause?user_id=%s' % query.from_user.id, json={"pause": "false"}) as resp: pass
    #-------------------------------------------------------------------------
    await schedule_jobs(query.from_user.id, state=state, edit=True, query=query)


# +==========================================================================================================================================================================+
# |**************************************************************************************************************************************************************************|
# |----------------------   MATHCING AND MESSAGING   ------------------------------------------------------------------------------------------------------------------------|
# |**************************************************************************************************************************************************************************|
# L__________________________________________________________________________________________________________________________________________________________________________l
# FORCE HAS_MATCH
@dp.message_handler(commands = 'has_match')
async def start_communicating(message: types.Message, state: FSMContext):
  # await db.set_first_time_status(message.from_user.id, conn, True)
  await bot.send_message(message.from_user.id, text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  
  #--------------------------------------------------------------------------------------
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(message.from_user.id, photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET)
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO)
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST)
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG)
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  with open(await db.get_profile_photo(await db.get_match_id(id, conn), conn), 'rb') as profile_pic:
    await bot.send_photo(message.from_user.id, photo=profile_pic, caption=texts.MATCH_INFO % (await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), await db.get_city(await db.get_match_id(message.from_user.id, conn), conn), await db.get_reason(await db.get_match_id(message.from_user.id, conn), conn)))
  await bot.send_message(message.from_user.id, text=texts.FIND_MATCH, reply_markup= keyboard)

# COMMANDS WHILE COMUNICATION
@dp.message_handler(state=Form.has_match, content_types=types.ContentTypes.TEXT)
async def forwarding_messages(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  if message.text == buttons_texts.WANNA_MEET:
    # -------------------------------------------------------
    # -----POST request for UNISON THAT USER WANNA MEET------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/wanna_meet?user_id=%s'%data['user_id'], json={
    #     "match_id": await db.get_match_id(message.from_user.id, conn)
    #   }) as resp: pass
    # -------------------------------------------------------
    # -------------POST request for some STATISTICS----------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": message.from_user.id,
    #         "event_type": "bot_meeting_ask"
    #       }
    #     ]
    #   }) as resp: pass
    # -------------------------------------------------------
    await bot.send_message(message.from_user.id, text=texts.WANNA_MEET)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_meeting')
    deny_button = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='are_u_deny_meeting')
    keyboard.row(confirm_button, deny_button)
    #sending message to match person
    await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.COFIRM_MEET % await db.get_name(message.from_user.id, conn), reply_markup=keyboard)
  # SENDING PHOTO   
  elif message.text == buttons_texts.SEND_PHOTO:
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id ,text=texts.UPLOAD_PHOTO_TO_MATCH)
    await state.reset_state(with_data=False)
    await Form.upload_photo_to_match.set()
  elif message.text == buttons_texts.END_DIALOG:
    await state.reset_state()
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to some STATISTIC--------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events":[{
    #       "user_id": message.from_user.id,
    #       "event_type": "bot_chating_end_btn"
    #     }]
    #   }) as resp: pass
    # #--------------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
    deny = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='deny_leaving')
    keyboard.row(confirm, deny)
    await Form.has_match.set()
    await bot.send_message(message.from_user.id, text=texts.CONFIRMING_LEAVING_CHAT, reply_markup=keyboard)
  elif message.text == buttons_texts.SEND_REQUEST:
    #data = await state.get_data()
    await bot.send_message(message.from_user.id, text=texts.COMUNICATION_HELP)
    await state.reset_state(with_data=False)
    await Form.get_help_message.set()
  else:
      await bot.send_message(await db.get_match_id(message.from_user.id, conn), text = message.text)

# IF U RECIVE MEETING MESSAGE AND AGREE TO IT
@dp.callback_query_handler(text='confirm_meeting')
async def congirm_meeting_message(message: types.Message, state: FSMContext):
  await db.set_meeting_status(message.from_user.id, conn, True)
  #data = await state.get_data()
  # --------POST request for STATISTICS ----------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_approve"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  # --------POST request for STATISTICS ----------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/meet_confirm?user_id=%s' % message.from_user.id, json={ "match_id": await db.get_match_id(message.from_user.id, conn) }) as resp: pass
  # ----------------------------------------------------------------
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.MATCH_AGREE % await db.get_name(message.from_user.id, conn))
  # game = random.randint(1, 12)
  # if game == 1:
  #   await Form.game1.set()
  # elif game == 2:
  #   await Form.game2.set()
  # elif game == 3:
  #   await Form.game3.set()
  # elif game == 4:
  #   await Form.game4.set()
  # elif game == 5:
  #   await Form.game5.set()
  # elif game == 6:
  #   await Form.game6.set()
  # elif game == 7:
  #   await Form.game7.set()
  # elif game == 8:
  #   await Form.game8.set()
  # elif game == 9:
  #   await Form.game9.set()
  # elif game == 10:
  #   await Form.game10.set()
  # elif game == 11:
  #   await Form.game11.set()
  # elif game == 12:
  #   await Form.game12.set()
  if await db.get_city(message.from_user.id, conn) == texts.SAINT_PETERSBURG:
    #await state.reset_state(with_data=False)
    #data = await state.get_data()
    await bot.send_message(message.from_user.id, text=texts.GREETING_MENU_SPB_PLACE % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
    mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
    jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
    keyboard.add(smena_menu_button)
    keyboard.add(mickey_monkeys_button)
    keyboard.add(jack_chan_button)
    await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
  elif db.get_city(message.from_user.id, conn) == texts.MOSCOW_HELLO:
    await bot.send_message(message.from_user.id, text=texts.MOSCOW_HELLO % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
    propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
    she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
    keyboard.add(double_b)
    keyboard.add(propoganda)
    keyboard.add(she)
    await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)

dp.callback_query_handler(text='spb_menu')
async def spb_menu(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
  mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
  jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
  keyboard.add(smena_menu_button)
  keyboard.add(mickey_monkeys_button)
  keyboard.add(jack_chan_button)
  await query.message.edit_text(text=texts.MENU_SPB_PLACE)
  await query.message.edit_reply_markup(reply_markup=keyboard)

@dp.callback_query_handler(text='msc_menu')
async def msc_menu(message: types.Message, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
  propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
  she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
  keyboard.add(double_b)
  keyboard.add(propoganda)
  keyboard.add(she)
  await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)

@dp.callback_query_handler(text='are_u_deny_meeting')
async def are_u_deny_meeting(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  yes = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='deny_meeting')
  no = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='confirm_meeting')
  keyboard.row(yes, no)
  await query.message.edit_text(text=texts.ARE_U_SURE_END)
  await query.message.edit_reply_markup(reply_markup=keyboard)

@dp.callback_query_handler(text='deny_meeting')
async def deny_meeting(message: types.Message, state: FSMContext):
  #----------------------------------------------------------------------------------
  #---------------POST request to STOP MATCHING on SERVER----------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
  #     "reason": "no interest"
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC--------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": "userId",
  #         "event_type": "bot_meeting_reject"
  #       }
  #     ]
  #   }) as resp: pass
  #______________________________________________________________________________________
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
  comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
  ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
  other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
  keyboard.add(look_button, comunication_button)
  keyboard.add(ignore_button, other_button)
  await bot.send_message(message.from_user.id, text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)


# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |           TIME TO END COMUNICATING                                                                                                                                        |
# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.callback_query_handler(text='callback_look')
async def dont_like_look(message: types.Message, state: FSMContext):
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "reason_stop_don't_like"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'не понравился внешне')
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)

@dp.callback_query_handler(text='callback_comunication')
async def dont_like_comunication(message: types.Message, state: FSMContext):
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "reason_stop_don't_like_messaging"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'не понравилось общение')
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)

@dp.callback_query_handler(text='callback_like')
async def everything_ok(message: types.Message, state: FSMContext):
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "reason_stop_like_but_time_gone"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'Понравился, но время общения истекло')
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)


@dp.callback_query_handler(text='callback_other')
async def callback_other(message: types.Message, state: FSMContext):
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "reason_stop_other"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  await state.reset_state(with_data=False)
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_REASON)
  await Form.callback_other.set()
@dp.message_handler(state=Form.callback_other, content_types= types.ContentTypes.TEXT)
async def set_message_other(message: types.Message, state: FSMContext):
  await db.set_reason_to_stop(message.from_user.id, conn, message.text)
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await Form.has_match.set()
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)


@dp.callback_query_handler(text='unlike_meeting')
async def set_was_meeting_no(message: types.Message, state: FSMContext):
  await db.set_meeting_status(message.from_user.id, conn, False)
  await state.reset_state(with_data=False)
  #------------------------------------------------------------------
  #-----------------POST requset for some STATISTICS-----------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "meeting_not_happens"
  #       }
  #     ]
  #   }) as resp: pass
  # _________________________________________________________________
  await bot.send_message(message.from_user.id, text=texts.REASON_MEETING)
  await Form.unlike_meeting.set()
@dp.message_handler(state=Form.unlike_meeting, content_types= types.ContentTypes.TEXT)
async def set_meeting_reaction(message: types.Message, state: FSMContext):
  await db.set_meeting_reaction(message.from_user.id, conn, message.text)
  state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)


@dp.callback_query_handler(text='ok_meeting')
async def set_was_meeting_yes(message: types.Message, state: FSMContext):
  await db.set_meeting_status(message.from_user.id, conn, True)
  await state.reset_state(with_data=False)
  #------------------------------------------------------------------
  #-----------------POST requset for some STATISTICS-----------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #      {
  #        "user_id": message.from_user.id,
  #        "event_type": "meeting_happens"
  #       }
  #     ]
  #   }) as resp: pass
  #------------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  like_meeting_button = types.InlineKeyboardButton(text=buttons_texts.LIKE_MEETING, callback_data='all_like')
  neutral_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NEUTRAL_MEETING, callback_data='neutral_meeting')
  dont_like_button = types.InlineKeyboardButton(text=buttons_texts.DONT_LIKE_MEETING, callback_data='dont_like_meeting')
  keyboard.add(like_meeting_button)
  keyboard.add(neutral_meeting_button)
  keyboard.add(dont_like_button)
  await bot.send_message(message.from_user.id, text=texts.LIKE_ABOT_MEETING, reply_markup=keyboard)

@dp.callback_query_handler(text='all_like')
async def set_meeting_reaction_ok(message: types.Message, state: FSMContext):
  await db.set_meeting_reaction(message.from_user.id, conn, 'Встреча понравилась')
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(message.from_user.id, text=texts.END_DIALOG % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not await db.is_paused(message.from_user.id, conn):
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  await Form.no_match.set()
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(message.from_user.id, photo=img_file ,reply_markup=reply_keyboard)
  if not await db.is_paused(message.from_user.id, conn):
    await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  await db.set_match_id_manualy(message.from_user.id, conn, 0)
  await db.set_reason_to_stop(message.from_user.id, conn, 'Вышло время')

@dp.callback_query_handler(text='neutral_meeting')
async def set_meeting_reaction_neutral(message: types.Message, state: FSMContext):
  await db.set_meeting_reaction(message.from_user.id, conn, 'Ничего особенного')
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)

@dp.callback_query_handler(text='dont_like_meeting')
async def set_meeting_reaction_negative(message: types.Message, state: FSMContext):
  await db.set_meeting_reaction(message.from_user.id, conn, 'Не понравилась')
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)

@dp.callback_query_handler(text='meeting_look')
async def set_why_meeting_bad_look(message: types.Message, state: FSMContext):
  await db.set_why_meeting_bad(message.from_user.id, conn, 'Не понравился внешне')
  await state.reset_state(with_data=False)
  # --------------POST request to END MATCHING--------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
  #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id, conn),
  #     "was_meeting": await db.is_meeting(message.from_user.id, conn),
  #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id, conn),
  #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id, conn)
  #   }) as resp: pass
  # --------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(message.from_user.id, text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not await db.is_paused(message.from_user.id, conn):
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(message.from_user.id, photo=img_file ,reply_markup=reply_keyboard)
  if not await db.is_paused(message.from_user.id, conn):
    await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  await db.set_match_id_manualy(message.from_user.id, conn, 0)
  await db.set_reason_to_stop(message.from_user.id, conn, 'Время вышло')
  await Form.no_match.set()

@dp.callback_query_handler(text='meeting_behavior')
async def set_why_meeting_bad_behavior(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  await db.set_why_meeting_bad(message.from_user.id, conn, 'Не понравился внешне')
  # --------------POST request to END MATCHING--------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
  #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id, conn),
  #     "was_meeting": await db.is_meeting(message.from_user.id, conn),
  #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id, conn),
  #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id, conn)
  #   }) as resp: pass
  # --------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(message.from_user.id, text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id, conn):
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not await db.is_paused(message.from_user.id):
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(message.from_user.id, photo=img_file ,reply_markup=reply_keyboard)
  if not await db.is_paused(message.from_user.id, conn):
    await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  await db.set_match_id_manualy(message.from_user.id, conn, 0)
  await db.set_reason_to_stop(message.from_user.id, conn, 'Время вышло')
  await Form.no_match.set()

@dp.callback_query_handler(text='meeting_place')
async def set_why_meeting_bad_place(message: types.Message, state: FSMContext):
  await db.set_why_meeting_bad(message.from_user.id, conn, 'Не понравился внешне')
  await state.reset_state(with_data=False)
  # --------------POST request to END MATCHING--------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
  #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id, conn),
  #     "was_meeting": await db.is_meeting(message.from_user.id, conn),
  #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id, conn),
  #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id, conn)
  #   }) as resp: pass
  # --------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if await db.is_subscribed(message.from_user.id, conn):#data['subscribtion']:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(message.from_user.id, text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id):
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not await db.is_paused(message.from_user.id):
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(message.from_user.id, photo=img_file ,reply_markup=reply_keyboard)
  if not await db.is_paused(message.from_user.id):
    await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  await db.set_match_id_manualy(message.from_user.id, conn, 0)
  await db.set_reason_to_stop(message.from_user.id, conn, 'Время вышло')
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.stop_match)
async def stoping_match(message: types.Message, state: FSMContext):
    #data = await state.get_data()
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    if await db.is_subscribed(message.from_user.id, conn):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    keyboard.add(subscribes_button)
    await bot.send_message(message.from_user.id, text=texts.END_DIALOG, reply_markup=keyboard)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(message.from_user.id, conn):
        subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not await db.is_paused(message.from_user.id, conn):#data['matching_pause']:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
    reply_keyboard.add(main_menu)
    with open('./pic/main_photo.png', 'rb') as img_file:
      await bot.send_photo(message.from_user.id, photo=img_file ,reply_markup=reply_keyboard)
    if not await db.is_paused(message.from_user.id, conn):
      await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
    else:
      await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
    await db.set_match_id_manualy(message.from_user.id, conn, 0)
    await db.set_reason_to_stop(message.from_user.id, conn, 'Время вышло')
    await Form.no_match.set()

# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                               MEETING PLACE                                                                                                                               |
# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# ____________SPB_______________________
@dp.callback_query_handler(text='smena')
async def show_smena(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_smena')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.SMENA_COFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_smena')
async def choose_smena(message: types.Message):
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_smena"
  #       }
  #     ]
  #   }) as resp: pass
  # -------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.SMENA_MEET_PLACE)
  await Form.has_match.set()

@dp.callback_query_handler(text='mickey')
async def show_mickey(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_mickey')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.MICKEY_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_mickey')
async def choose_mickey(message: types.Message):
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_mickey_monkey"
  #       }
  #     ]
  #   }) as resp: pass
  # -------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.MICKEY_MEET_PLACE)
  await Form.has_match.set()

@dp.callback_query_handler(text='jack_and_chan')
async def show_jack(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_jack')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.JACK_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_jack')
async def choose_jack(message: types.Message):
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_lack_chan"
  #       }
  #     ]
  #   }) as resp: pass
  # -------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.JACK_MEET_PLACE)
  await Form.has_match.set()

# ____________MSC_______________________
@dp.callback_query_handler(text='double_b')
async def doube_b(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_double_b')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.DOUBLE_B_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_double_b')
async def choose_double_b(message: types.Message):
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_dabl_be"
  #       }
  #     ]   
  #   }) as resp: pass
  # -------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.DOUBLE_B_PLACE)
  await Form.has_match.set()

@dp.callback_query_handler(text='propoganda')
async def propoganda(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_propoganda')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.PROPOGANDA_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_propoganda')
async def choose_propoganda(message: types.Message):
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_propoganda"
  #       }
  #     ]
  #   }) as resp: pass
  # -------------------------------------------
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.PROPOGANDA_PLACE)
  await Form.has_match.set()

@dp.callback_query_handler(text='she')
async def she(message: types.Message):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_she')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.SHE_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_she')
async def choose_she(message: types.Message):
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_meeting_place_she"
  #       }
  #     ]   
  #   }) as resp:pass
  # -------------------------------------------
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.SHE_PLACE)
  await Form.has_match.set()

# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                    PAYMENTS EVENTS                                                                                                                                        |
# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

@dp.callback_query_handler(state=Form.payment_renew_fail)
async def payment_renew_fail(message: types.Message, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_RENEWAL_FAIL, reply_markup=keyboard)

@dp.callback_query_handler(state=Form.payment_renew_success)
async def payment_renew_success(message: types.Message, state: FSMContext):
  # ----------------------------------------------------------------------------
  # ---------------   POST request for some STATISTICS   -----------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_payment_renew_success"
  #       }
  #     ]
  #   }) as resp: pass
  # ___________________________________________________________________________
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_RENEWAL_SUC)

@dp.callback_query_handler(state=Form.payment_ok)
async def payment_ok(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/payment?user_id=%s' % message.from_user.id, json={
  #     "status_payment": "pass"}) as resp: pass
  # ----------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_NEW_SUC)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_subscribe_pay_success"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------
  # ---------SENDING INFO to MODERATION CHAT------------
  await bot.send_message(-776565232, text=texts.PAYMENTS_FOR_MODERATION % (message.from_user.id,
                                                                          await db.get_name(message.from_user.id, conn),
                                                                          message.from_user.id), parse_mode='markdown')
  # ----------------------------------------------------
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ends)
async def payment_ends(message: types.Message, state: FSMContext):
  await db.set_subscribtion_status(message.from_user.id, conn, False)
  # ----------------------------------------------------------------
  # ----------------POST request for some STATISTICS----------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events":[
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_subscribe_pay_ended"
  #       }
  #     ]
  #   }) as resp: pass
  # ----------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id, conn):
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='have_subscribtion')
  else:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_ENDS, reply_markup=keyboard)

@dp.callback_query_handler(state=Form.payment_fail)
async def payment_fail(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  # ---------------------------------------------------------------
  # ---------------POST request for some STATISTICS----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "bot_subscribe_pay_reject"
#     }
#   ]
# })
  # ---------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  again = types.InlineKeyboardButton(text=buttons_texts.TRY_AGAIN, callback_data='doesnt_have_subscribtions')
  keyboard.add(again)
  bot.send_message(message.from_user.id, text=texts.PAYMENT_FAIL, reply_markup=keyboard)
  await Form.no_match.set()

# +===========================================================================================================================================================================+
# |                     ENDING COMUNICATION                                                                                                                                   |
# +===========================================================================================================================================================================+
# 
@dp.callback_query_handler(text='deny_leaving')
async def deny_leaving(query: types.CallbackQuery, state: FSMContext):
  await query.message.delete()
  await Form.has_match.set()
  
# LEAVE THE CHAT
@dp.callback_query_handler(text='confirm_leaving')
async def delete_match_info(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
    comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
    ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
    other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
    keyboard.add(look_button, comunication_button)
    keyboard.add(ignore_button, other_button)
    await query.message.edit_text(text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)


@dp.callback_query_handler(text='dont_like_look')
async def dont_like_look(query: types.CallbackQuery, state: FSMContext):
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to some STATISTIC------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": query.from_user.id,
    #         "event_type": "bot_chating_self_end_reason_ugly"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------POST reuqest to some STATISTIC------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #       "user_id": await db.get_match_id(query.from_user.id, conn),
    #         "event_type": "bot_chating_partner_end_reason_ugly"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    await db.set_reason_to_stop(query.from_user.id, conn, 'Не понравился внешне')
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to stop MATCH----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % query.from_user.id, json={
    #     "reason": await db.get_reason_to_stop(query.from_user.id, conn)
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": await db.get_match_id(query.from_user.id, conn),
    #         "event_type": "bot_chating_ended_partner_choosing"
    #       }
    #     ]
    #   }) as resp: pass
    # -------------------------------------------------------------------------------------
    await state.reset_state()
    match_id = await db.get_match_id(query.from_user.id, conn)
    # sending MATCH USER message about leaving the chat-----------------
    keyboard1 = types.InlineKeyboardMarkup(resize_keyboard = True)
    confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='match_confirm_leaving')
    keyboard1.add(confirm_leaving_button)
    await bot.send_message(match_id, text=texts.USER_LEAVE_CAHT, reply_markup=keyboard1)
    # __________________________________________________________________
    scheduler.remove_job('unmatch_%s' % query.from_user.id, 'default')
    scheduler.remove_job('unmatch_%s' % match_id, 'default')
    # DELETE MATCH INFO --------------------------------------------------------------------------------------------
    await db.set_match_id_manualy(match_id, conn, 0)
    await db.set_match_id_manualy(query.from_user.id, conn, 0)

    await db.set_match_status(query.from_user.id, conn, False)
    await db.set_match_status(match_id, conn, False)
    await schedule_jobs(query.from_user.id, state)

@dp.callback_query_handler(text='match_confirm_leaving', state=Form.has_match)
async def match_confirm_leaving(query: types.CallbackQuery, state: FSMContext):
    await schedule_jobs(query.from_user.id, state)
# CANCEL LEAVING

@dp.callback_query_handler(text='ignore')
async def show_ignore(message: types.Message, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_chating_self_end_reason_noreply"
  #       }
  #     ]
  #   }) as resp: pass
  # #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_self_end_reason_noreply"
  #       }
  #     ]
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'собеседник не отвечает')
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
  #     "reason": await db.get_reason_to_stop(message.from_user.id, conn)
  #     }) as resp: pass
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_ended_partner_choosing"
  #       }
  #     ]
  #   }) as resp: pass
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.callback_query_handler(text='dont_like_comunication')
async def dont_like_comunication(message: types.Message, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_chating_partner_end_reason_stupid"
  #       }
  #     ]
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_partner_end_reason_stupid"
  #       }
  #     ]
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, "не понравилось общение")
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
  #     "reason": await db.get_reason_to_stop(message.from_user.id, conn)
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_ended_partner_choosing"
  #       }
  #     ]
  #   }) as resp: pass
  await bot.send_message(message.from_user.id, text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.callback_query_handler(text='dont_like_other')
async def dont_like_other(message: types.Message, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_chating_self_end_reason_else"
  #       }
  #     ]
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_partner_end_reason_else"
  #       }
  #     ]
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  await state.reset_state()
  await Form.why_dont_like.set()
@dp.message_handler(state=Form.why_dont_like, content_types=types.ContentTypes.TEXT)
async def set_reason(message: types.Message, state: FSMContext):
  await db.set_reason_to_stop(message.from_user.id, conn, message.text)
  await state.reset_state(with_data=False)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
  #     "reason": await db.get_reason_to_stop(message.from_user.id, conn)
  #   }) as resp: pass
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": await db.get_match_id(message.from_user.id, conn),
  #         "event_type": "bot_chating_ended_partner_choosing"
  #       }
  #     ]
  #   }) as resp: pass
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

# +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                   FORWARDING PHOTOS                                                                                                                                     |
# +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.message_handler(state=Form.upload_photo_to_match, content_types=types.ContentType.PHOTO)
async def upload_photo_to_match(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  photo_id = message.photo[-1].file_id
  #-----------------------------------------------------------------
  #----------------POST request for some statistics-----------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_send_photo_to_user"
  #       }
  #     ]
  #   }) as resp: pass
  #-----------------------------------------------------------------
  # WE FORWARDING PHOTO SO IT CAN BE DONE WITH ID OF IMAGE
  await bot.send_photo(await db.get_match_id(message.from_user.id, conn), photo=photo_id)

# +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                 COMLAIN WHILE COMUNICATION                                                                                                                            |
# +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.message_handler(state=Form.get_help_message, content_types=types.ContentTypes.TEXT)
async def get_comunication_help_message(message: types.Message, state: FSMContext):
  help_message = message.text
  await state.reset_state(with_data=False)
  # await bot.send_message(-776565232, text=texts.COMPLAIN_MODERATION % (message.from_user.id,
  #                                                                     await db.get_name(message.from_user.id, conn),
  #                                                                     message.from_user.id,
  #                                                                     help_message), parse_mode='markdown')
  #----------------------------------------------------------------------------------
  #---------------------POST request for some STATISTIC------------------------------]
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
  #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #     "events": [
  #       {
  #         "user_id": message.from_user.id,
  #         "event_type": "bot_chating_send_petition"
  #       }
  #     ]  
  #   }) as resp: pass
  #----------------------------------------------------------------------------------
  await Form.has_match.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=scheduler.start())    
