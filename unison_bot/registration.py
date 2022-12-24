# -*- coding: utf-8 -*-
import os
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json
import base64
import datetime
import random
import db_interface as db
import asyncpg
import aiohttp
import re
import app_logger
import aiofiles
import logging

from dateutil.relativedelta import relativedelta
from payments import PRICES
from aiologger import Logger
from pathlib import Path
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, DB_PASSWORD, DB_USER, DB_ADRESS, TESTING_TOKEN, BOT_MODERATOR, PAY_TOKEN


bot = Bot(token=TESTING_TOKEN)
moderator_bot = Bot(token=BOT_MODERATOR)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
logger = app_logger.get_logger(__name__)

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
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_ONE)

@dp.callback_query_handler(state = Form.game2)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TWO)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_TWO)
  
@dp.callback_query_handler(state = Form.game3)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_THREE)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_THREE)
  
@dp.callback_query_handler(state = Form.game4)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_FOUR)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_FOUR)
  
@dp.callback_query_handler(state = Form.game5)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_FIVE)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_FIVE)
  
@dp.callback_query_handler(state = Form.game6)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_SIX)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_SIX)
  
@dp.callback_query_handler(state = Form.game7)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_SIX)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_SIX)
  
@dp.callback_query_handler(state = Form.game8)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_EIGHT)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_EIGHT)
  
@dp.callback_query_handler(state = Form.game9)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_NINE)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_NINE)
  
@dp.callback_query_handler(state = Form.game10)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TEN)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_TEN)
  
@dp.callback_query_handler(state = Form.game11)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_ELEVEN)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_ELEVEN)
  
@dp.callback_query_handler(state=Form.game12)
async def game_one(message: types.Message, state: FSMContext):
  await state.reset_state()
  await bot.send_message(message.from_user.id, text=texts.GAME_TWELVE)
  await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.GAME_TWELVE)
  
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
    if await db.is_matching(id):
      await bot.send_message(id, text=first_day_hints.pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(id, state, ))
  elif hints:
    if await db.is_matching(id):
      await bot.send_message(id, text=hints.pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(id, state, ))

async def is_match(id: int) -> bool:
  r'''
  Get information about is user has match, or not. Return TRUE - if yes, FALSE - if no
  '''
  return await db.is_matching(id)

async def is_premium(id: int) -> bool:
  r'''
  Get information if user has subscription, or not. Return True - if yes, FALSE - if no
  '''
  return await db.is_subscribed(id)

async def is_monday() -> bool:
  r'''
  If today MONDAY return TRUE, if not return FALSE
  '''
  if not datetime.date.today().weekday():
    return True
  else:
    return False

async def set_state_unmatch(id: int, state: FSMContext, first_name: str, last_name: str,  unmatch_menu=False):
    r'''
    This function set users matching status to False. Also edit this field in DB.
    id - users telegram id, state - state of Finite State Machine, unmatch_menu - do u wish to show unmatch_menu with callback,
    show_menu - do u wish to show unmatch menu
    '''
    if unmatch_menu:
        logger.info('[%s@%s_%s] показываю unmatch menu' % (id, first_name, last_name))
        await db.set_match_status(id, False)
        logger.warning('[%s@%s_%s] установил match status равным False' % (id, first_name, last_name))
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
        logger.warning('[%s@%s_%s] FSM state has_match OFF' % (id, first_name, last_name))
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
        logger.info('[%s@%s_%s] Вывод меню отзыва об общении с парой' % (id, first_name, last_name))
    else:
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state has_match OFF' % (id, first_name, last_name))
        is_matching = await db.is_matching(id)
        logger.warning('[%s@%s_%s] получил из бд статус найденной пары [%s]' % (id, first_name, last_name, is_matching))
        is_paused = await db.is_paused(id)
        if is_paused:
            await db.set_matching_pause_status(id, False)
            logger.warning('[%s@%s_%s] занес в БД статус паузы в поиске партнера [%s]' % (id, first_name, last_name, False))
        if is_matching:
            await db.set_match_status(id, False)
            logger.warning('[%s@%s_%s] занес в БД статус найденной пары [%s]' % (id, first_name, last_name, False))
        logger.info('[%s@%s_%s] Вывод меню Пара не найдена - Поиск пары' % (id, first_name, last_name))
        await show_unpaused_no_match_menu(id)

async def set_state_one_day_to_unmatch(id: int, state: FSMContext, first_name: str, last_name: str):
    r'''Function to warn user that he has only one day left to comunicate with his match'''
    #scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=1), args=(id, state, first_name, last_name, True, ))
    scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state, first_name, last_name, True, ))
    match_id = await db.get_match_id(id)
    logger.warning('[%s@%s_%s] получил match id из БД' % (id, first_name, last_name))
    match_name = await db.get_name(match_id)
    logger.warning('[%s@%s_%s] получил match name из БД' % (id, first_name, last_name))
    logger.info('[%s@%s_%s] отправлено предупреждение о том что остался один день до unmatch' % (id, first_name, last_name))
    bot.send_message(id, text=texts.ONE_DAY_TO_UNMATCH % match_name)

async def set_state_has_match(id: int, state: FSMContext, first_name: str, last_name: str, show_menu = True):
    r'''Set User matchinbg status as True and edit his profile in data base'''
    # if its first match for user
    await Form.has_match.set()
    st = dp.current_state(chat=await db.get_match_id(id), user=await db.get_match_id(id))
    await st.set_state(Form.has_match)
    logger.warning('[%s@%s_%s] получил статус first time' % (id, first_name, last_name))
    if await db.is_first_time(id):
        await db.set_first_time_status(id, False)
        logger.warning('[%s@%s_%s] установить статус first time равный False' % (id, first_name, last_name))
    await bot.send_message(id, text=texts.NEW_MATCH)
    #--------------------------------------------------------------------------------------
    #-----------------   getting match INFO   ---------------------------------------------
    logger.warning('[%s@%s_%s] получил match id равный [%s]' % (id, first_name, last_name, await db.get_match_id(id)))
    logger.warning('[%s@%s_%s] получил match name равный [%s]' % (id, first_name, last_name, await db.get_name(await db.get_match_id(id))))
    logger.warning('[%s@%s_%s] получил match city равный [%s]' % (id, first_name, last_name, await db.get_city(await db.get_match_id(id))))
    logger.warning('[%s@%s_%s] получил match_reason равный [%s]' % (id, first_name, last_name, await db.get_reason(await db.get_match_id(id))))
    # _____________________________________________________________________________________
    # ----------------   creating match photo from base64 string   ------------------------
    await db.get_b64_profile_photo(await db.get_match_id(id))
    logger.warning('[%s@%s_%s] получил фотографию мэтча как строку base64' % (id, first_name, last_name))
    b64_im = await db.get_b64_profile_photo(await db.get_match_id(id))
    try:
        async with aiofiles.open(Path(r'profiles/%s/match_photo.jpg' % id), 'wb') as match_photo:
            await match_photo.write(base64.b64decode(b64_im[1:]))
        logger.warning('[%s@%s_%s] записал фото из строки base64 profiles/%s/match_photo.jpg' % (id, first_name, last_name, id))
    except:
        logger.warning('[%s@%s_%s] ошибка во время открытия match_photo.jpg.' % (id, first_name, last_name))
        await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    # _____________________________________________________________________________________
    try:
        async with aiofiles.open(Path('pic/find_match.png'), 'rb') as img:
            await bot.send_photo(id, photo=img)
    except:
        logger.warning('[%s@%s_%s] ошибка во время открытия match_photo.jpg.' % (id, first_name, last_name))
        await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    # Create inline keyboard for match menu
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET)
    send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO)
    send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST)
    end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG)
    keyboard.row(wanna_meet_button, send_photo_button)
    keyboard.row(send_request, end_dialog)
    try:
        async with aiofiles.open(Path(r'profiles/%s/match_photo.jpg' % id), 'rb') as profile_pic:
            await bot.send_photo(id, photo=profile_pic, caption=texts.MATCH_INFO % (await db.get_name(await db.get_match_id(id)), 
                                                                                    await db.get_city(await db.get_match_id(id)), 
                                                                                    await db.get_reason(await db.get_match_id(id))))
        logger.warning('[%s@%s_%s] отправил фотографию мэтча' % (id, first_name, last_name))
    except:
        logger.warning('[%s@%s_%s] ошибка во время открытия match_photo.jpg.' % (id, first_name, last_name))
        await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    # running os.remove in async way
    try:
        os.remove(Path(r'profiles/%s/match_photo.jpg' % id))
        logger.warning('[%s@%s_%s] удалил фотографию мэтча profiles/%s/match_photo' % (id, first_name, last_name, id))
    except(FileNotFoundError):
        logger.warning('[%s@%s_%s] файл match_photo.jpg не найден.' % (id, first_name, last_name))
        await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    except:
        logger.warning('[%s@%s_%s] файл match_photo.jpg найден. Но что то пошло не так.' % (id, first_name, last_name))
        await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    await bot.send_message(id, text=texts.FIND_MATCH, reply_markup= keyboard)
    await get_advice(id, state)
    logger.info('[%s@%s_%s] вывел совет' % (id, first_name, last_name))
    logger.warning('[%s@%s_%s] FSM state has_match ON' % (id, first_name, last_name))
    

async def schedule_jobs(id: int, state: FSMContext, first_name ='', last_name='', need_edit = False, query = None, show_menu=True):
    r'''
    Time scheduler to unmatch and warn users by timer. Using AsyncIOScheduler
    id - user telegram id, 
    '''
    #logger.info('[%s@%s_%s] запуск диспетчера задач с выводом нужных меню' % (id, first_name, last_name))
    if dp.get_current().current_state() == Form.no_match:
        await state.reset_state()
    
    # IF USER NOT SUBSCRIBED
    if not await is_premium(id) and not await db.is_first_time(id):
        # IF TODAY IS MONDAY
        if await is_monday():
          # IF THERE IS MATCH FOR USER
          if await is_match(id):
              # SHEDULE WARNING ABOUT ENDING TIME
              if not await db.is_paused(id):
                  #new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
                  new_date = datetime.datetime.now() + datetime.timedelta(minutes=10)
                  if not scheduler.get_job('unmatch_%s' % id):
                      scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=new_date, args=(id, state, first_name, last_name, ), id='unmatch_%s' % id)
                      logger.warning('[%s@%s_%s] add job one_day_to_unmatch [not premium, not first time, today monday, has match not paused]' % (id, first_name, last_name))
                  # SHOW HAS MATCH STATUS
                  if show_menu:
                      logger.warning('[%s@%s_%s] set_state_has_match [show menu]' % (id, first_name, last_name))
                      await set_state_has_match(id, state)
          # IF THERE IS NO MATCH FOR USER BUT ITS STILL MONDAY
          else:
            if not await db.is_paused(id):
              # SCHEDULE REPEATING THIS FUNCTION
              if not scheduler.get_job('check_%s' % id):
                  scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=5), args=(id, state, first_name, last_name, ), id='check_%s' % id)
                  logger.warning('[%s@%s_%s] add job schedule_jobs [not premium, not first time, monday, no match, not paused]' % (id, first_name, last_name))
              # SHOW UNMATCH MENU
              if show_menu:
                  logger.warning('[%s@%s_%s] set_state_unmatch [show menu]' % (id, first_name, last_name))
                  await set_state_unmatch(id, state)
        # IF TODAY IS NOT MONDAY
        else:
          # IF NOT MONDAY - REPEAT AFTER days_till_monday DAYS and SHOW UNMATCH MENU
          days_till_monday = 7 - datetime.date.today().weekday()
          new_date = datetime.date.today() + datetime.timedelta(days=days_till_monday)
          run_date = datetime.datetime.combine(new_date, datetime.time(hour=9, minute=0))
          if not scheduler.get_job('monday_%s' % id):
            scheduler.add_job(schedule_jobs, 'date', run_date=run_date, args=(id, state, first_name, last_name, False, ), id = 'monday_%s' % id) # add job to scheduler
            #logger.warning('[%s@%s_%s] add job schedule_jobs [not premium, not first time, not monday]' % (id, first_name, last_name))
          if show_menu:
            if not await db.is_paused(id):
              if need_edit:
                  #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu, not paused, need edit]' % (id, first_name, last_name))
                  await show_unpaused_no_match_menu(id, first_name, last_name, True, query)
              else:
                  #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu, not paused, not need edit]' % (id, first_name, last_name))
                  await show_unpaused_no_match_menu(id, first_name, last_name)
            else:
              if need_edit:
                  #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu, paused, need edit]' % (id, first_name, last_name))
                  await show_paused_menu(id, first_name, last_name, True, query)
              else:
                  #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu, paused, not need edit]' % (id, first_name, last_name))
                  await show_paused_menu(id, first_name, last_name)
    # IF USER SUBSCRIBED or ITS FIRST TIME
    else:
      if await is_match(id):
        # SHEDULE WARNING ABOUT ENDING TIME 
        #new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
        if await db.is_first_time(id):
            await db.set_first_time_status(id, False)
        if not await db.is_paused(id):
            if not scheduler.get_job('unmatch_%s' % id):
              scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=datetime.datetime.now() + datetime.timedelta(minutes=10), args=(id, state, first_name, last_name, ), id='unmatch_%s' % id)
              logger.warning('[%s@%s_%s] add job one_day_to_unmatch [premium, has match, not paused]' % (id, first_name, last_name))
        # SHOW HAS MATCH STATUS
            logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu]' % (id, first_name, last_name))
            await set_state_has_match(id, state, first_name, last_name)
      # IF THERE IS NO MATCH REPEAT AFTER 10 MINUTES
      # SHOW UNMATCH
      else:
        #await state.reset_state()
        if not await db.is_paused(id):
          if need_edit:
            if not scheduler.get_job('check_%s' % id):
                scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state, first_name, last_name, False, None, False, ), id= 'check_%s' % id)
                #logger.warning('[%s@%s_%s] add job schedule_jobs [premium, no match, not paused, need_edit]' % (id, first_name, last_name))
            if show_menu:
                #logger.info('[%s@%s_%s] показать меню при паузе в поиске партнера' % (id, first_name, last_name))
                await show_unpaused_no_match_menu(id, first_name, last_name, True, query)
          else:
            if not scheduler.get_job('check_%s' % id):
                scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state, first_name, last_name, False, None, False, ), id= 'check_%s' % id)
                #logger.warning('[%s@%s_%s] add job schedule_jobs [premium, no match, not paused, not need edit]' % (id, first_name, last_name))
            # if we need to show menu
            if show_menu:
                #logger.info('[%s@%s_%s] показать меню при поиске партнера' % (id, first_name, last_name))
                await show_unpaused_no_match_menu(id, first_name, last_name)
        else:
          if need_edit:
            if scheduler.get_job('check_%s' % id, 'default'):
                scheduler.remove_job(job_id='check_%s' % id, jobstore='default')
                #logger.warning('[%s@%s_%s] remove job schedule_jobs [premium, no match, paused, need edit]' % (id, first_name, last_name))
            if show_menu:
                #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu]' % (id, first_name, last_name))
                await show_paused_menu(id, first_name, last_name, True, query)
          else:
            if scheduler.get_job('check_%s' % id):
                scheduler.remove_job(job_id='check_%s' % id, jobstore='default')
                #logger.warning('[%s@%s_%s] remove job schedule_jobs [premium, no mathc, paused, not need edit]' % (id, first_name, last_name))
            if show_menu:
                #logger.warning('[%s@%s_%s] remove job schedule_jobs [show menu]' % (id, first_name, last_name))
                await show_paused_menu(id, first_name, last_name)

# BOT MESSAGES MECHANICS
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------   STARTING DIALOG   -----------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# WELCOME MESSAGE AND CHOICE GO TO REGISTRATION OR READ ABOUT PROJECT
@dp.message_handler(commands='start')
async def start(message: types.Message, state: FSMContext):
    r''' conn
    Connecting to database and schedule jobs
    '''
    st = state.get_state()
    logger.info('[%s@%s_%s] Подключился к боту' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await state.reset_state()
    logger.info('[%s@%s_%s] Подключился к базе данных' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.table_ini()
    await db.create_new_user(message.from_user.id)
    await db.set_subscription_begin_date(message.from_user.id, datetime.date.today() + datetime.timedelta(days=10))
    await db.set_subscription_end_date(message.from_user.id, datetime.date.today() + datetime.timedelta(days=10))
    await db.set_algorithm_steps(message.from_user.id, 30)
    await db.set_likes(message.from_user.id, 7)
    await db.set_superlikes(message.from_user.id, 5)
    logger.info('[%s@%s_%s] Переведен на Начальное меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await show_starting_menu(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    #await schedule_jobs(message.from_user.id, state=state)

async def show_unpaused_no_match_menu(id: int, first_name: str, last_name: str, edit=False, query=None):
    r'''
    Showing unpaused menu when server find matches
    If edit = False - menu will be send by separate message and query wil be None
    if edit = True - menu will edit message will be in query argument(MUST BE types.CallbackQuery)
    '''
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(id):
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

async def show_paused_menu(id: int, first_name: str, last_name: str, edit=False, query=None):
    r'''
    Showing paused menu when server find matches
    If edit = False - menu will be send by separate message and query wil be None
    if edit = True - menu will edit message will be in query argument(MUST BE types.CallbackQuery)
    '''
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(id):
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

async def show_starting_menu(id: int, first_name: str, last_name: str):
    photo = open(Path('pic/start.jpg'), 'rb')
    starting_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    about_project_button = types.InlineKeyboardButton(buttons_texts.INFO_ABOUT_PROJECT, callback_data='back')
    starting_inline_keyboard.add(about_project_button)
    starting_inline_keyboard.add(registration_button)
    await bot.send_photo(id, photo)
    logger.info('[%s@%s_%s] Показано стартовое меню' % (id, first_name, last_name))
    await bot.send_message(id, text=texts.WELCOME, reply_markup=starting_inline_keyboard)

# MESSAGE ABOUT PROJECT
@dp.callback_query_handler(text='about')
async def show_about_text(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [about]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    about_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='registr')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    about_keyboard.row( back_button, registration_button)
    await query.message.edit_text(text=texts.ABOUT, reply_markup=about_keyboard)

# MESSAGE ABOUT UNIQUENESS OF PROJECT
@dp.callback_query_handler(text='uniqueness')
async def show_uniqueness(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [uniqueness]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    uniqueness_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    uniqueness_inline_keyboard.add(back_button, registration_button)
    await query.message.edit_text(text=texts.UNIQUENESS, reply_markup=uniqueness_inline_keyboard)

# MESSAGE ABOUT WHAT IS IMPRINTING
@dp.callback_query_handler(text='imprint')
async def show_imprint(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [imprint]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    imprint_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='back')
    imprint_inline_keyboard.add(registration_button)
    imprint_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.IMPRINT, reply_markup=imprint_inline_keyboard)
            
# FIRST OF THREE MESSAGE WITH USER AGREEMENT
@dp.callback_query_handler(text='user_agreement_1')
async def show_user_agreement(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [user_agreement_1]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] В меню [user_agreement_2]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] В меню [user_agreement_3]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] В меню [faq]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] В меню [back]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] В меню [concept]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    back_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    back_inline_keyboard.add(registration_button)
    back_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.CONCEPT, reply_markup=back_inline_keyboard)

# MESSAGE ABOUT USAGE OF USER PHOTO
@dp.callback_query_handler(text='photo')
async def show_photo(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [photo]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    photo_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    photo_inline_keyboard.add(registration_button)
    photo_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.PHOTO, reply_markup=photo_inline_keyboard)

# MESSAGE ABOUT PAYING FOR SUBSCRIBE
@dp.callback_query_handler(text='find')
async def show_find(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [find]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    find_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    find_inline_keyboard.add(registration_button)
    find_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.FIND, reply_markup=find_inline_keyboard)

# MESSAGE FOR INVESTORS
@dp.callback_query_handler(text='investors')
async def show_investors(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [investors]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    investors_inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    registration_button = types.InlineKeyboardButton(buttons_texts.BEGIN_REGISTRATION, callback_data='begin')
    back_button = types.InlineKeyboardButton(buttons_texts.BACK, callback_data='faq')
    investors_inline_keyboard.add(registration_button)
    investors_inline_keyboard.add(back_button)
    await query.message.edit_text(text=texts.INVESTORS, reply_markup=investors_inline_keyboard)

# MESSAGE FOR JOURNALISTS
@dp.callback_query_handler(text='journalists')
async def show_journalists(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] В меню [journalists]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] начальный шаг регистрации' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    # logger.warning('[%s@%s_%s] Начальный шаг регистрации' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    reg_button = types.InlineKeyboardButton(buttons_texts.BEGIN_BUTTON, callback_data='begin_registration')
    keyboard.add(reg_button)
    async with aiofiles.open(Path('pic/letsgo.jpg'), 'rb') as photo:
        await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text= texts.LETS_GO, reply_markup=keyboard)


# REGISTRATION RULES
@dp.callback_query_handler(text='begin_registration')
async def begin_registration(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] регистрация начата' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] регистрация начата' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    lets_go_button = types.InlineKeyboardButton(buttons_texts.START_REGISTRATION_BUTTON, callback_data='start_step')
    keyboard.add(lets_go_button)
    await query.message.edit_text(text=texts.REGISTRATION_RULES, reply_markup=keyboard)

# SET name STATE in STATE MACHINE as ACTIVE
@dp.callback_query_handler(text='start_step')
async def show_registration_start_step(query: types.CallbackQuery, state: FSMContext):
    await query.message.edit_text(text=texts.NAME)
    logger.warning('[%s@%s_%s] FSM state name ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await Form.name.set()
# SET profile NAME and FINISH NAME STATE in STATE MACHINE
@dp.message_handler(state=Form.name, content_types=types.ContentTypes.ANY)
async def set_profile_name(message: types.Message, state: FSMContext):
    if message.content_type=='text':
        logger.info('[%s@%s_%s] ввели имя' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        if any(map(str.isdigit, message.text)): # check if name is "correct"
            await message.reply(texts.NAME)
            logger.warning('[%s@%s_%s] введенное имя не подходит' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return 
        await db.set_name(message.from_user.id, message.text) # set the profile name 
        logger.warning('[%s@%s_%s] введенное имя [%s] заносится в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text))
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
        logger.warning('[%s@%s_%s] FSM state name OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        logger.info('[%s@%s_%s] выбор пола пользователем' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await bot.send_message(message.from_user.id, text=texts.INPUT_ERROR)
        logger.info('[%s@%s_%s] попытка отправить не ТЕКСТ' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return


# SET profile GENDER to MALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='male')
async def show_male_menu(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] пол внесен в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_gender(query.from_user.id, buttons_texts.GENDER_MALE[1])
    logger.warning('[%s@%s_%s] пол [Мужской] внесен в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.warning('[%s@%s_%s] FSM birthday state ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    logger.info('[%s@%s_%s] Проверка даты рождения и выбор города' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    # check birthday string in format DD.MM.YYYY
    if not re.match(pattern=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', string=message.text):
        logger.warning('[%s@%s_%s] Ошибка ввода дня рождения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        logger.warning('[%s@%s_%s] Провалена проверка дня рождения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.reset_state()
    logger.warning('[%s@%s_%s] FSM birthday state OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    logger.info('[%s@%s_%s] Конвертирование даты для записи в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_birthday(message.from_user.id, date)
    logger.warning('[%s@%s_%s] запись даты рождения [%s] в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, date))
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
    logger.info('[%s@%s_%s] Вывод меню выбора города' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

# SET profile GENDER to FEMALE and ACTIVATE BIRTHDAY STATE
@dp.callback_query_handler(text='female')
async def show_female_menu(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] пол внесен в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_gender(query.from_user.id,  buttons_texts.GENDER_FEMALE[1])
    logger.warning('[%s@%s_%s] пол [Женский] внесен в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    await query.message.edit_text(texts.BIRTHDATE)
    logger.warning('[%s@%s_%s] FSM birthday state ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await Form.birthdate.set()
# SET birthday finish the STATE and let the user choose a city
@dp.message_handler(state=Form.birthdate)
async def check_date(message: types.Message, state:FSMContext):
    logger.info('[%s@%s_%s] Проверка даты рождения и выбор города' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    if not re.match(pattern=r'^\s*(3[01]|[12][0-9]|0?[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})\s*$', string=message.text).span == (0, 10):
        logger.warning('[%s@%s_%s] ошибка ввода дня рождения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        logger.warning('[%s@%s_%s] провалена проверка дня рождения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.reply(texts.WRONG_BIRTHDATE)
        return
    await state.reset_state()
    logger.warning('[%s@%s_%s] FSM birthday state OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    date = datetime.datetime.strptime(message.text, "%d.%m.%Y").date()
    logger.info('[%s@%s_%s] Конвертирование даты и запись в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_birthday(message.from_user.id, date)
    logger.warning('[%s@%s_%s] запись даты рождения [%s] в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, date))
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
    await bot.send_message(message.from_user.id, text=texts.CITY_CHOOSE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] Вывод меню выбора города' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))


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
    logger.info('[%s@%s_%s] подписался на канал' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] подписался на канал' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))


@dp.callback_query_handler(text='other_city')
async def show_under_construction(query: types.CallbackQuery, state: FSMContext):
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
    logger.info('[%s@%s_%s] выбрал город который еще не поддерживается' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] выбрал город который еще не поддерживается' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)


@dp.callback_query_handler(text='other_gender')
async def show_under_construction(query: types.CallbackQuery, state: FSMContext):
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
    logger.info('[%s@%s_%s] выбрал не традиционные отношения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] выбрал не традиционные отношения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='friends')
async def show_under_construction(query: types.CallbackQuery, state: FSMContext):
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
    logger.info('[%s@%s_%s] выбрал причину поиска отношений "Дружба" ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] выбрал причину поиска отношений "Дружба" ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)

@dp.callback_query_handler(text='no_duty')
async def show_under_construction(query: types.CallbackQuery, state: FSMContext):
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
    logger.info('[%s@%s_%s] выбрал причину поиска отношений "Без обязательств" ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] выбрал причину поиска отношений "Без обязательств" ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin_registration')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)


@dp.callback_query_handler(text='reason_again')
async def reason_again(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] вывод меню выбора причины' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] выбрал причину поиска отношений [Другое]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] выбрал причину поиска отношений [Другое] ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.InlineKeyboardButton(buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='subscribe')
    again_button = types.InlineKeyboardButton(buttons_texts.CHANGE_REASON, callback_data='reason_again')
    keyboard.row(subscribe_button, again_button)
    await query.message.edit_text(text=texts.UNDER_CONSTRUCTION, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод сообщения об ошибке' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# SET city as Moscow and ASK about goal of the relationship
@dp.callback_query_handler(text='moscow')
async def add_moscow(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] выбрал город Москва ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_city(query.from_user.id, texts.MOSCOW)
    logger.warning('[%s@%s_%s] занес информацию о городе в БД [Москва]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # -----------------------------------------------------------------------------
    # --------------------    POST request for some STATISTIC    ------------------
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
    # -----------------------------------------------------------------------------
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
    logger.info('[%s@%s_%s] вывод меню выбора причины' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# SET city as SAINT-PETERSBURG and ASK about goal of the relationship
@dp.callback_query_handler(text='saint-p')
async def add_saintp(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] выбрал город Санкт-Петерубрг' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_city(query.from_user.id, texts.SAINT_PETERSBURG)
    logger.warning('[%s@%s_%s] занес информацию о городе в БД [Санкт-Петербург]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] вывод меню выбора причины' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# SET city as SAMARA and ASK about goal of the relationship
@dp.callback_query_handler(text='samara')
async def add_samara(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] выбрал город Самара' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_city(query.from_user.id, texts.SAMARA)
    logger.warning('[%s@%s_%s] занес информацию о городе в БД [Самара]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] вывод меню выбора причины' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# IF u change cities very often than we SET ur city as a nomad and ASK about goal of the relationship
@dp.callback_query_handler(text='nomad')
async def add_nomad(query: types.CallbackQuery, state= FSMContext):
    logger.info('[%s@%s_%s] выбрал город Кочевник' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_city(query.from_user.id, texts.NOMAD)
    logger.warning('[%s@%s_%s] занес иноформацию о городе в БД [Кочевник]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] вывод меню выбора причины' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await query.message.edit_text(texts.CHOSE_GOAL, reply_markup=keyboard)

# SET ur relationship goal as SERIOUS RELATIONSHIP and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='srsly')
async def add_reason_srsly(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] выбрал причину поиска [Серьезные отношения]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_reason(query.from_user.id, texts.SERIOUS_REL)
    logger.warning('[%s@%s_%s] занес причину поиска отношений  в БД [Серьезные отношения]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] выведено меню загрузки основной фотографии профиля' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# SET ur relationship goal as MAKING FAMILY and starting the process of uploading photos to ur profile
@dp.callback_query_handler(text='family')
async def add_reason_family(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] выбрал причину поиска "Создание семьи"' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_reason(query.from_user.id, texts.FAMILY)
    logger.warning('[%s@%s_%s] занес в БД причину поиска отношений [Создание семьи]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    logger.info('[%s@%s_%s] выведено меню загрузки основной фотографии профиля' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# user uploads MAIN PHOTO of his profile. Activate the MAIN PHOTO STATE OF STATE MACHINE. CONFIRMING THE PHOTO
@dp.callback_query_handler(text='upload_main_photo')
async def ad_photo(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] начало загрузки основной фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    error_flag = await db.get_error_status(query.from_user.id)
    logger.warning('[%s@%s_%s] получили из бд флаг ошибки [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, error_flag))
    if error_flag:
        error_flag = await db.set_error_status(query.from_user.id, False)
    await query.message.edit_text(texts.UPLOAD_PHOTO)
    await Form.profile_photo.set()
    logger.warning('[%s@%s_%s] FSM state profile_photo ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
# DOWNLOADING MAIN PHOTO OF PROFILE. BECOURSE WE NEED TO FORWARD IT TO MODERATION CHAT
@dp.message_handler(state=Form.profile_photo, content_types=types.ContentTypes.ANY)
async def download_photo(message: types.Message, state: FSMContext):
    error_status = await db.get_error_status(message.from_user.id)
    logger.warning('[%s@%s_%s] получили из бд флаг ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
    if message.content_type == 'photo':
        if message.media_group_id:
            logger.warning('[%s@%s_%s] загрузка больше 1 фотографии' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.info('[%s@%s_%s] выведено сообщение об ошибке' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                logger.warning('[%s@%s_%s] выведено сообщение об ошибке' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        img = message.photo[-1].file_id
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] загружена фотография в profiles/%s/profile_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        await db.set_profile_photo(message.from_user.id, img)
        logger.warning('[%s@%s_%s] занес в БД telegram id фотографии профиля' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state profile_photo OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        # await bot.send_photo(message.from_user.id, photo=await db.get_profile_photo(message.from_user.id))
        await bot.send_message(message.from_user.id, text=texts.CONFIRMING_PHOTO, reply_markup=keyboard)
        logger.info('[%s@%s_%s] вывод меню подтверждения загрузки фотографии профиля' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        logger.info('[%s@%s_%s] попытка отправить фотографию как документ или не фотографию' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.answer(text=texts.OOPS_PHOTO)
        return


# User MAKE the BASIC ACCOUNT. He can choose to check if nothing wrong or move to uploading extra photos
@dp.callback_query_handler(text='confirm_photo')
async def end_basic_registration(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    watch_profile_button = types.InlineKeyboardButton(buttons_texts.WATCH_PROFILE, callback_data='show_base_profile')
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    keyboard.row(watch_profile_button, next_button)
    await query.message.edit_text(texts.BASE_PROFILE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню подтверждения загрузки фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))


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
    logger.info('[%s@%s_%s] вывод рекомендации загрузки фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))


# SHOWING base profile of user
@dp.callback_query_handler(text='show_base_profile')
async def show_base_profile(message: types.CallbackQuery):
    logger.info('[%s@%s_%s] вывод базового профиля' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    text = '%s: %s\n%s: %s\n%s: %s\n%s: %s\n%s: %s' % (texts.FIRST_NAME ,await db.get_name(message.from_user.id),
                                                              texts.BIRTHDAY, await db.get_birthday(message.from_user.id),
                                                              texts.GENDER, await db.get_gender(message.from_user.id), \
                                                              texts.CITY,
                                                              await db.get_city(message.from_user.id),
                                                              texts.REASON,
                                                              await db.get_reason(message.from_user.id))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    next_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='upload_extra_photo')
    reg_button = types.InlineKeyboardButton(buttons_texts.RESTART_REGISTRATION, callback_data='begin')
    keyboard.row(reg_button, next_button)
    img = await db.get_profile_photo(message.from_user.id)
    logger.warning('[%s@%s_%s] загружен telegram id фотографии профиля' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await bot.send_photo(message.from_user.id, photo=img, caption=text, reply_markup=keyboard)


# We need 3 photos from different sides of your face. UPLOADING FIRST and GIVING INFO about PHOTOS that service needs
@dp.callback_query_handler(text='upload_extra_photo')
async def upload_three_photo(message: types.Message):
    logger.info('[%s@%s_%s] загрузка фотографий ракурса' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    error_flag = await db.get_error_status(message.from_user.id)
    logger.warning('[%s@%s_%s] получил флаг ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_flag))
    if error_flag:
        error_flag = await db.set_error_status(message.from_user.id, False)
    photo = open(Path('pic/3photos.png'), 'rb')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_message(message.from_user.id, text=texts.EXTRA_PHOTOS)
    logger.warning('[%s@%s_%s] FSM state first_side_photo ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await Form.first_side_photo.set()
# IF ANSWER OF USER IS PHOTO and STATE first_side_photo is ACTIVE = UPLOAD 1st PHOTO TO SERVER and FINISH THE first side photo STATE IN STATE MACHINE and ACTIVATE second_side_photo STATE
@dp.message_handler(state=Form.first_side_photo, content_types=types.ContentTypes.ANY)
async def upload_first_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        logger.info('[%s@%s_%s] загрузка первой фотографии ракурсов' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получил тег ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if message.media_group_id:
            logger.warning('[%s@%s_%s] загрузка больше 1 фотографии' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.info('[%s@%s_%s] выведено сообщение об ошибке' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                logger.warning('[%s@%s_%s] выведено сообщение об ошибке' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        img = message.photo[-1].file_id
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/first_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] загрузка фотографии в profiles/%s/first_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        await db.set_1st_extra_photo(message.from_user.id, img)
        logger.warning('[%s@%s_%s] занесение telegram id фотографии в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state first_side_photo OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await bot.send_message(message.from_user.id, text=texts.SECOND_PHOTO)
        logger.warning('[%s@%s_%s] FSM state second_side_photo ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await Form.second_side_photo.set() # also we can use "state.next()"
    else:
        logger.info('[%s@%s_%s] попытка отправить что то что не является фотографией' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.answer(text=texts.OOPS_PHOTO)
        return
# IF ANSWER OF USER IS PHOTO and STATE second_side_photo is ACTIVE = UPLOAD 2nd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.second_side_photo, content_types=types.ContentTypes.ANY)
async def upload_second_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получил флаг ошибки [%s] из БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if message.media_group_id:
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.warning('[%s@%s_%s] попытка отправить не 1 фотографию, а медиа группу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        img = message.photo[-1].file_id
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/second_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] скачан файл в profiles/%s/second_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        await db.set_2nd_extra_photo(message.from_user.id, img)
        logger.warning('[%s@%s_%s] занесение telegram id фотографии в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state second_side_photo OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await bot.send_message(message.from_user.id, text=texts.THIRD_PHOTO)
        await Form.third_side_photo.set() # also we can use "state.next()"
        logger.warning('[%s@%s_%s] FSM state third_extra_photo ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await message.answer(text=texts.OOPS_PHOTO)
        return
# IF ANSWER OF USER IS PHOTO and STATE third_side_photo is ACTIVE = UPLOAD 3rd PHOTO TO SERVER and FINISH THE STATE IN STATE MACHINE
@dp.message_handler(state=Form.third_side_photo, content_types=types.ContentTypes.ANY)
async def upload_third_photo(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        error_status = await db.get_error_status(message.from_user.id)
        if message.media_group_id:
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
            return
        img = message.photo[-1].file_id
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/third_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] скачан файл в profiles/%s/third_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        await db.set_3rd_extra_photo(message.from_user.id, img)
        logger.warning('[%s@%s_%s] занесение telegram id фотографии в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state third_extra_photo OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        inline_keyboard = types.InlineKeyboardMarkup(resize_true = True)
        chek_button = types.InlineKeyboardButton(buttons_texts.CHECK_EXTRA_PHOTOS, callback_data='show_extra_photos')
        next_step_button = types.InlineKeyboardButton(buttons_texts.NEXT_STEP, callback_data='start_alogrithm_educating')
        inline_keyboard.row(chek_button, next_step_button)
        await bot.send_message(message.from_user.id, text=texts.ALL_PHOTOS, reply_markup=inline_keyboard)
        logger.info('[%s@%s_%s] вывод сообщения о завершении составления базового фронта' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        async with aiofiles.open(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id), 'rb') as profile:
            async with aiofiles.open(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id), 'rb') as first:
                async with aiofiles.open(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id), 'rb') as second:
                    async with aiofiles.open(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id), 'rb') as third:
                        b64_profile = base64.b64encode(await profile.read())
                        b64_first = base64.b64encode(await first.read())
                        b64_second = base64.b64encode(await second.read())
                        b64_third = base64.b64encode(await third.read())
                        await db.set_b64_profile_photo(message.from_user.id, b64_profile)
                        logger.warning('[%s@%s_%s] отправка в БД base64 string фотографии профиля' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                        await db.set_b64_1st_photo(message.from_user.id, b64_first)
                        logger.warning('[%s@%s_%s] отправка в БД base64 string первой фотографии ракурса' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                        await db.set_b64_2nd_photo(message.from_user.id, b64_second)
                        logger.warning('[%s@%s_%s] отправка в БД base64 string второй фотографии ракурса' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                        await db.set_b64_3rd_photo(message.from_user.id, b64_third)
                        logger.warning('[%s@%s_%s] отправка в БД base64 string третьей фотографии ракурса' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                        #-------------------------------------------------------------------------------
                        #--------------    POST request to send profile to moderation    ---------------
        # async with aiofiles.open(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id), 'rb') as profile:
        #     async with aiofiles.open(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id), 'rb') as first:
        #         async with aiofiles.open(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id), 'rb') as second:
        #             async with aiofiles.open(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id), 'rb') as third:
        #                 if await db.is_moderated(message.from_user.id):
        #                     if not await db.is_photo_ok(message.from_user.id) or not await db.is_info_ok(message.from_user.id):
        #                         await moderator_bot.send_message(-1001693622168, text=texts.REMODERATION % (message.from_user.id,
        #                                                         await db.get_name(message.from_user.id),
        #                                                         await db.get_gender(message.from_user.id),
        #                                                         await db.get_birthday(message.from_user.id),
        #                                                         await db.get_city(message.from_user.id),
        #                                                         await db.get_reason(message.from_user.id)))
        #                   else:
        #                       await moderator_bot.send_message(-1001693622168, text=texts.NEW_MODERATION % (message.from_user.id,
        #                                                         await db.get_name(message.from_user.id),
        #                                                         await db.get_gender(message.from_user.id),
        #                                                         await db.get_birthday(message.from_user.id),
        #                                                         await db.get_city(message.from_user.id),
        #                                                         await db.get_reason(message.from_user.id)))
        #                 #-------------------------------------------------------------------------------
        #                 #------   POST request to send profile main photo   ----------------------------
        #                 img = await db.get_profile_photo(message.from_user.id)
        #                 await moderator_bot.send_photo(-1001693622168, profile, caption=texts.PROFILE_PHOTO)
        #                 #-------------------------------------------------------------------------------
        #                 #-------------------------------------------------------------------------------
        #                 #------------------POST request to upload photos to profile on server-----------
        #                 # async with aiohttp.ClientSession() as session:
        #                 #   async with session.post(url='https://server.unison.dating/user/add_photos/self?user_id=%s' % message.from_user.id, json={
        #                 #       "main_photo": await db.get_profile_photo(message.from_user.id),#str(b64_profile),
        #                 #       "other_photos": [
        #                 #         await db.get_1st_extra_photo(message.from_user.id),#str(b64_first),
        #                 #         await db.get_2nd_extra_photo(message.from_user.id),#str(b64_second),
        #                 #         await db.get_3rd_extra_photo(message.from_user.id)#str(b64_third)
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
        try:
            os.remove(Path(r'profiles/%s/profile_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/profile_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл profile_photo.jpg не найден.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл profile_photo.jpg найден. Но что то пошло не так' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        try:
            os.remove(Path(r'profiles/%s/first_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/first_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл first_photo.jpg не найден. Создан новый файл' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл first_photo.jpg найден. Но что то пошло не так' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        try:
            os.remove(Path(r'profiles/%s/second_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/second_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл second_photo.jpg не найден. Создан новый файл' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл second_photo.jpg найден. Но что то пошло не так' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        try:
            os.remove(Path(r'profiles/%s/third_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/third_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл third_photo.jpg не найден. Создан новый файл' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл third_photo.jpg найден. Но что то пошло не так' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
    else:
        await message.answer(text=texts.OOPS_PHOTO)
        logger.info('[%s@%s_%s] попытка загрузить фото как документ или что то что не является фото' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return
      

# CONFIRMING EXTRA PHOTOS BEFORE UPLOADING
@dp.callback_query_handler(text='show_extra_photos')
async def show_extra_photos(message: types.Message):
    logger.info('[%s@%s_%s] загрузка первой фотографии ракурсов' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    #1
    img1 = await db.get_1st_extra_photo(message.from_user.id)
    logger.warning('[%s@%s_%s] получение telegram id первой фотографии ракурсов' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    #2
    img2 = await db.get_2nd_extra_photo(message.from_user.id)
    logger.warning('[%s@%s_%s] загрузка telegram id второй фотографии ракурсов' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    #3
    img3 = await db.get_3rd_extra_photo(message.from_user.id)
    logger.warning('[%s@%s_%s] загрузка telegram id третьей фотографии ракурсов' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] вывод меню проверки дополнительных фото' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))


# UPLOADING PHOTOS TO SERVER
@dp.callback_query_handler(text='start_alogrithm_educating')
async def add_other_photos(query: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    letsgo_button = types.InlineKeyboardButton(buttons_texts.LETS_GO, callback_data='rules_of_studing')
    inline_keyboard.add(letsgo_button)
    await query.message.edit_text(text=texts.START_EDUCATION, reply_markup=inline_keyboard)
    logger.info('[%s@%s_%s] старт обучения алгоритма' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# ---------- EDUCATING ALGORITHM -----------------------------------------------------------------------
@dp.callback_query_handler(text='rules_of_studing')
async def show_rules_of_studing(query: types.CallbackQuery):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    begin_button = types.InlineKeyboardButton(text=buttons_texts.BEGIN_BUTTON, callback_data='first_educational_photo')
    inline_keyboard.add(begin_button)
    await query.message.edit_text(text=texts.RULE_STUDING, reply_markup=inline_keyboard)
    logger.info('[%s@%s_%s] старт обучения алгоритма' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='first_educational_photo')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/init?user_id=%s'%query.from_user.id, json={
    #       "next_id": await db.get_algorithm_steps(query.from_user.id) - 30
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
    steps = await db.get_algorithm_steps(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество шагов [%s] из БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, steps))
    likes = await db.get_likes(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество лайков [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, likes))
    super_likes = await  db.get_super_likes(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество суперлайков [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, super_likes))
    super_like_button = types.InlineKeyboardButton(buttons_texts.SUPER_LIKE, callback_data='superlike_educate_algorithm')
    likes_button = types.InlineKeyboardButton(buttons_texts.LIKE, callback_data='like_educate_algorithm')
    inline_keyboard.row(likes_button, super_like_button)
    inline_keyboard.add(unlike_button)
    await query.answer(text=buttons_texts.ANSWER_STUDY % (31-steps, likes, super_likes), show_alert=True)
    logger.info('[%s@%s_%s] вывод окна с информацией о количестве шагов и лайков и супер лайков' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    async with aiofiles.open('pic/testing_thirty/%s.jpg'% (31 - steps), 'rb') as img:
      await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)
    logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, (31-steps)))

@dp.callback_query_handler(text='unlike_educate_algorithm')
async def alogrithm_education(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка не нравится' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    await db.set_algorithm_steps(query.from_user.id, await db.get_algorithm_steps(query.from_user.id)-1)
    logger.warning('[%s@%s_%s] уменьшение количества шагов на 1' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество шагов [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, steps))
    likes = await db.get_likes(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество лайков [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, likes))
    super_likes = await  db.get_super_likes(query.from_user.id)
    logger.warning('[%s@%s_%s] получил количество суперлайков [%s]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, super_likes))
    if likes == 0 and super_likes == 0:
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
        skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
        keyboard.add(extra_photo)
        keyboard.add(skip)
        await bot.send_message(query.chat.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, 30))
    else:
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
        #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id),
        #     "answer": {
        #       30-steps: "0"
        #     }
        #   }) as resp: 
        #       response = json.loads(await resp.text()) 
        #       #print(await resp.text())
        await query.message.delete()
        #await bot.send_photo(query.from_user.id, photo=response['url'], reply_markup=inline_keyboard)
        async with aiofiles.open('pic/testing_thirty/%s.jpg'%(31-steps), 'rb') as img:
          await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, (31-steps)))

@dp.callback_query_handler(text='like_educate_algorithm')
async def second_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка лайк' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    await db.set_likes(query.from_user.id, await db.get_likes(query.from_user.id)-1)
    await db.set_algorithm_steps(query.from_user.id, await db.get_algorithm_steps(query.from_user.id)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id)
    likes = await db.get_likes(query.from_user.id)
    super_likes = await  db.get_super_likes(query.from_user.id)
    if likes == 0 and super_likes == 0:
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
        skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
        keyboard.add(extra_photo)
        keyboard.add(skip)
        await bot.send_message(query.chat.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, 30))
    else:
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
        #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id),
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
        async with aiofiles.open('pic/testing_thirty/%s.jpg' % (31-steps), 'rb') as img:
          await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, (31-steps)))

@dp.callback_query_handler(text='superlike_educate_algorithm')
async def third_algorithm_education(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка суперлайк' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
    await db.set_superlikes(query.from_user.id, await db.get_super_likes(query.from_user.id)-1)
    await db.set_algorithm_steps(query.from_user.id, await db.get_algorithm_steps(query.from_user.id)-1)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    steps = await db.get_algorithm_steps(query.from_user.id)
    likes = await db.get_likes(query.from_user.id)
    super_likes = await  db.get_super_likes(query.from_user.id)
    if likes == 0 and super_likes == 0:
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        extra_photo = types.InlineKeyboardButton(buttons_texts.UPLOAD_EX_PHOTO, callback_data='likes_photo')
        skip = types.InlineKeyboardButton(buttons_texts.SKIP, callback_data='skip')
        keyboard.add(extra_photo)
        keyboard.add(skip)
        await bot.send_message(query.chat.id, text=texts.FINAL_MESSAGE, reply_markup=keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, 30))
    else:
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
        #     "next_id": 31-await db.get_algorithm_steps(query.from_user.id),
        #     "answer": {
        #       30-await db.get_algorithm_steps(query.from_user.id): "2"
        #     }
        #   }) as resp: 
        #        request = json.loads(await resp.text())
        #        print(await resp.text())
        # _____________________________________________________________________________________________________________________________________________________
    
        await query.message.delete()
        #await bot.send_photo(query.from_user.id, photo=request['url'], reply_markup=inline_keyboard)
        async with aiofiles.open('pic/testing_thirty/%s.jpg'%(31-steps), 'rb') as img:
          await bot.send_photo(query.from_user.id, photo=img, reply_markup=inline_keyboard)
        logger.info('[%s@%s_%s] отображение фотографии' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
        logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, (31-steps)))

@dp.callback_query_handler(text='final_like')
async def registration_final(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка лайк' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] отображение фотографии' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, 30))

@dp.callback_query_handler(text='final_super_like')
async def registration_final(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка суперлайк' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] отображение фотографии' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, 30))

@dp.callback_query_handler(text='final_unlike')
async def registration_final(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] нажата кнопка лайк' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] отображение фотографии' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.warning('[%s@%s_%s] получение и загрузка [%s] фотографии для обучения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, 30))

@dp.callback_query_handler(text='no_superlikes')
async def no_superlikes(query: types.CallbackQuery):
    await query.answer(text=texts.NO_SUPERLIKES)

@dp.callback_query_handler(text='no_likes')
async def no_likes(query: types.CallbackQuery):
    await query.answer(text=texts.NO_LIKES)

@dp.callback_query_handler(text='skip')
async def skip(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] переход к состоянию ожидания пары' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] вывод меню фотографий бывших' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='upload_extra')
async def upload_extra(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] переход к загрузке первой фотографии бывших' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await query.message.edit_text(text=texts.FIRST_EX_PHOTOS)
    await Form.extra_photo_1.set()
    logger.warning('[%s@%s_%s] FSM state extra_photo_1 ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
@dp.message_handler(state=Form.extra_photo_1, content_types=types.ContentTypes.ANY)
async def extra_photo_1(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        logger.info('[%s@%s_%s] загрузка первой фотографии бывших' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получение статуса ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if error_status:
            await db.set_error_status(message.from_user.id, False)
        if message.media_group_id:
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.warning('[%s@%s_%s] попытка отправить не 1 фотографию, а медиа группу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] скачивание фотографии в profiles/%s/first_ex_photo' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        async with aiofiles.open(Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
            b64_str = base64.b64encode(await photo.read())
            await db.set_b64_likes_photo_1(message.from_user.id, b64_str)
            logger.warning('[%s@%s_%s] загрузка первой фотографии в формате base64 string в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        try:
            os.remove(Path(r'profiles/%s/first_ex_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/first_ex_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл first_ex_photo.jpg не найден.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл first_ex_photo.jpg найден, но что то пошло не так.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(message.from_user.id, text=texts.SMTHNG_GOES_WRONG)
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state extra_photo_1 OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        next_photo = types.InlineKeyboardButton(text=buttons_texts.SECOND_EXTRA, callback_data='second_extra')
        end_photo = types.InlineKeyboardButton(text=buttons_texts.STOP_UPLOADING, callback_data='stop_uploading')
        keyboard.add(next_photo)
        keyboard.add(end_photo)
        await bot.send_message(message.from_user.id, text=texts.SECOND_EXTRA_PHOTO, reply_markup=keyboard)
        logger.info('[%s@%s_%s] отображение меню "продолжить загрузку или завершить"' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await message.answer(text=texts.OOPS_PHOTO)
        logger.info('[%s@%s_%s] попытка загрузить фотографию как документ или что то другое' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return

@dp.callback_query_handler(text='second_extra')
async def second_extra(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] загрузка второй фотографии бывших' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await bot.send_message(message.from_user.id, text=texts.SECOND_EX_PHOTO)
    await Form.extra_photo_2.set()
    logger.warning('[%s@%s_%s] FSM state extra_photo_2 ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
@dp.message_handler(state=Form.extra_photo_2, content_types=types.ContentTypes.ANY)
async def extra_photo_second(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        logger.info('[%s@%s_%s] загрузка второй фотографии бывших' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получение статуса ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if message.media_group_id:
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.warning('[%s@%s_%s] попытка отправить не 1 фотографию, а медиа группу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        img = message.photo[-1].file_id
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] скачивание фотографии в profiles/%s/second_ex_photo' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        async with aiofiles.open(Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
            b64_str = base64.b64encode(await photo.read())
            await db.set_b64_likes_photo_2(message.from_user.id, b64_str)
            logger.warning('[%s@%s_%s] загрузка второй фотографии в формате base64 string в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        try:
            os.remove(Path(r'profiles/%s/second_ex_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/second_ex_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл second_ex_photo.jpg не найден.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл second_ex_photo.jpg найден, но что то пошло не так.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(message.from_user.id, text=texts.SMTHNG_GOES_WRONG)
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state extra_photo_2 OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        next_photo = types.InlineKeyboardButton(text=buttons_texts.THIRD_EXTRA, callback_data='third_extra')
        end_photo = types.InlineKeyboardButton(text=buttons_texts.STOP_UPLOADING, callback_data='stop_uploading')
        keyboard.add(next_photo)
        keyboard.add(end_photo)
        await bot.send_message(message.from_user.id, text=texts.THIRD_EXTRA_PHOTO, reply_markup=keyboard)
        logger.info('[%s@%s_%s] отображение меню "продолжить загрузку или завершить"' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await message.answer(text=texts.OOPS_PHOTO)
        logger.info('[%s@%s_%s] попытка загрузить фотографию как документ или что то другое' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return

@dp.callback_query_handler(text='third_extra')
async def third_extra(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] переход к загрузке третьей фотографии бывших' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await bot.send_message(message.from_user.id, text=texts.THIRD_EX_PHOTOS)
    await Form.extra_photo_3.set()
    logger.warning('[%s@%s_%s] FSM state extra_photo_3 ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
@dp.message_handler(state=Form.extra_photo_3, content_types=types.ContentTypes.ANY)
async def extra_photo_third(message: types.Message, state: FSMContext):
    if message.content_type == 'photo':
        logger.info('[%s@%s_%s] загрузка третьей фотографии бывших' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получение статуса ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if message.media_group_id:
            if not error_status:
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
                logger.warning('[%s@%s_%s] попытка отправить не 1 фотографию, а медиа группу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            return
        await message.photo[-1].download(destination_file=Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id))
        logger.warning('[%s@%s_%s] скачивание фотографии в profiles/%s/third_ex_photo' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        try:
            async with aiofiles.open(Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id), 'rb') as photo:
                b64_str = base64.b64encode(await photo.read())
                await db.set_b64_likes_photo_3(message.from_user.id, b64_str)
                logger.warning('[%s@%s_%s] загрузка третьей фотографии в формате base64 string в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        except:
            logger.warning('[%s@%s_%s] ошибка во время открытия third_ex_photo.jpg.' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        try:
            os.remove(Path(r'profiles/%s/third_ex_photo.jpg' % message.from_user.id))
            logger.warning('[%s@%s_%s] удаление фотографии profiles/%s/third_ex_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        except(FileNotFoundError):
            logger.warning('[%s@%s_%s] файл third_ex_photo.jpg не найден.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
        except:
            logger.warning('[%s@%s_%s] файл third_ex_photo.jpg найден, но что то пошло не так.' % (id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(message.from_user.id, text=texts.SMTHNG_GOES_WRONG)
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state extra_photo_3 OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        logger.info('[%s@%s_%s] переход к состоянию ожидания пары' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await schedule_jobs(message.from_user.id, state)
    else:
        await message.answer(text=texts.OOPS_PHOTO)
        logger.info('[%s@%s_%s] попытка загрузить фотографию как документ или что то другое' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return

@dp.callback_query_handler(text='stop_uploading')
async def stop_uploading(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] переход к состоянию ожидания пары' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] отображение рекомендаций по загрузке доп фотографий' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
# _____________________________________________________________________________________________________________________________________________________________________________
#+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#|                               WAITING FOR MATCH                                                                                                                            |
#L____________________________________________________________________________________________________________________________________________________________________________l
# IF sheduler set state no_match as active 
@dp.message_handler(state=Form.no_match)
async def messaging_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(message.from_user.id):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscription')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscriptions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not await db.is_paused(message.from_user.id): 
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    if not await db.is_matching(message.from_user.id):
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    if not await db.is_paused(message.from_user.id):
      await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=keyboard)
    else:
      await bot.send_message(message.from_user.id, text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentTypes.ANY, state=Form.no_match)
async def message_reaction_if_text(message: types.Message):
    if message.content_type == 'text':
        if message.text == buttons_texts.MAIN_MENU and not await db.is_matching(message.from_user.id):
          if await db.is_paused(message.from_user.id):
              await show_paused_menu(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
              logger.info('[%s@%s_%s] отображение меню паузы в поиске мэтча' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
          else:
              await show_unpaused_no_match_menu(message.from_user.id, message.from_user.first_name, message.from_user.last_name)
              logger.info('[%s@%s_%s] отображение меню поиска мэтча' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='main_menu')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    if not await db.is_paused(query.from_user.id):
      await show_unpaused_no_match_menu(query.from_user.id, query.from_user.first_name, query.from_user.last_name, edit=True, query=query)
      logger.info('[%s@%s_%s] отображение меню паузы в поиске мэтча' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    else:
      await show_paused_menu(query.from_user.id, query.from_user.first_name, query.from_user.last_name, edit=True, query=query)
      logger.info('[%s@%s_%s] отображение меню поиска мэтча' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

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
    await query.message.edit_text(text=texts.WHAT_TO_DO, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню получения подписки при условии что нет подписки' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  

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
    await query.message.edit_text(text=texts.SUBSCRIBE_INFO, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню получения подписки при условии что нет подписки' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))


# Get subscription
@dp.callback_query_handler(text='subscribe')
async def pay_subscribe(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] вывод меню оплаты подписки' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    #--------------------------------------------------------------------------------------
    #----------------------POST request for getting payment url----------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/payment/request?user_id=%s' % query.from_user.id, json={
    #     "amount": "870"
    #   }) as resp:
    #     payment = json.loads(await resp.text())
    #     await db.set_payment_url(query.from_user.id, payment['url'])
    #--------------------------------------------------------------------------------------   
    
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
    await bot.send_invoice(
        query.from_user.id,
        title=buttons_texts.GET_SUBSC,
        description=texts.SUBSCRIBE_INFO,
        provider_token=PAY_TOKEN,
        currency='rub',
        photo_url='https://cdn.pixabay.com/photo/2017/06/10/06/41/credit-2389154_960_720.png',
        photo_height=360,
        photo_width=360,
        photo_size=360,
        prices=PRICES,
        start_parameter='one-month-subscription',
        payload='test-invoice-payload'
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True, error_message=texts.PAYMENT_FAIL)

@dp.message_handler(content_types=types.ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    today = datetime.date.today()
    end_date = datetime.date.today()+relativedelta(months=1)
    await db.set_subscription_begin_date(message.from_user.id, today)
    await db.set_subscription_end_date(message.from_user.id, end_date)


@dp.callback_query_handler(text='deny_subscribtion')
async def abbandon_subscribe(query: types.CallbackQuery):
    logger.info('[%s@%s_%s] отказаться от подписки' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    new_date = datetime.date.today() - datetime.timedelta(days=1)
    await db.set_subscription_end_date(query.from_user.id, new_date)
    logger.warning('[%s@%s_%s] отправил статус подписки [%s] ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, False))
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
    await query.message.edit_text(text=texts.PAYMENT_CANCEL, reply_markup=keyboard)

# ===========================================================================================================================================================================+
# |                        HELP USER                                                                                                                                         |
# L__________________________________________________________________________________________________________________________________________________________________________l
@dp.callback_query_handler(text='help')
async def get_help(query: types.CallbackQuery, state: FSMContext):
  logger.info('[%s@%s_%s] обратится за помощью' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  await db.set_help_status(query.from_user.id, True)
  logger.warning('[%s@%s_%s] отправил статус обратился за помощью [%s] ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, True))
  await state.reset_state()
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
  logger.warning('[%s@%s_%s] FSM state help ON ' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
@dp.message_handler(state=Form.help, content_types=types.ContentTypes.ANY)
async def help_message(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        # ------------------------------------------------------------------------
        # -----------------   FORWARDING HELP   ----------------------------------
        async with aiohttp.ClientSession() as session:
          async with session.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
            "chat_id": "-776565232",
            "text": texts.HELP_MESSAGE % (message.from_user.id, 
                                          await db.get_name(message.from_user.id), 
                                          message.text, 
                                          '[Profile ](tg://user?id=%s)' % message.from_user.id)
          }) as resp: pass
        # ________________________________________________________________________
        await db.set_help_status(message.from_user.id, False)
        logger.warning('[%s@%s_%s] отправил статус обратился за помощью [%s] ' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, True))
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state help OFF ' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
        back = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
        keyboard.add(back)
        await bot.send_message(message.from_user.id, text=texts.AFTER_HELP, reply_markup=keyboard)
        logger.info('[%s@%s_%s] запрос помощи отправлен' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
         await bot.send_message(message.from_user.id, text=texts.NOT_TEXT_MESSAGE)
         logger.info('[%s@%s_%s] запрос помощи отправлен' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
         return

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
    logger.info('[%s@%s_%s] вывод ссылки на телеграм' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
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
  await db.set_matching_pause_status(query.from_user.id, True)
  logger.warning('[%s@%s_%s] отправить значение паузы [%s] в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, True))
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
  # STOP finding match
  logger.info('[%s@%s_%s] вызов scheduler"а из paused' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  await schedule_jobs(query.from_user.id, state, query.from_user.first_name, query.from_user.last_name, need_edit=True, query=query)


# Main menu when user in proces of finding his match
@dp.callback_query_handler(text='unpaused_main_menu')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    await db.set_matching_pause_status(query.from_user.id, False)
    logger.warning('[%s@%s_%s] отправить значение паузы [%s] в БД' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name, False))
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
    logger.info('[%s@%s_%s] вызов scheduler"а из unpaused' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(query.from_user.id, state=state, first_name=query.from_user.first_name, last_name=query.from_user.last_name, need_edit=True, query=query)


# +==========================================================================================================================================================================+
# |**************************************************************************************************************************************************************************|
# |----------------------   MATHCING AND MESSAGING   ------------------------------------------------------------------------------------------------------------------------|
# |**************************************************************************************************************************************************************************|
# L__________________________________________________________________________________________________________________________________________________________________________l
# FORCE HAS_MATCH
# @dp.message_handler(commands = 'has_match')
# async def start_communicating(message: types.Message, state: FSMContext):
#     logger.info('[%s@%s_%s] принудительный запуск состояние has_match' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     await Form.has_match.set()
#     logger.warning('[%s@%s_%s] FSM state has_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     global conn
#     conn = await asyncpg.connect('postgresql://%s:%s@%s/bot_db' % (DB_USER, DB_PASSWORD, DB_ADRESS))
#     # await db.set_first_time_status(message.from_user.id, True)
#     await bot.send_message(message.from_user.id, text=texts.NEW_MATCH)
#     logger.info('[%s@%s_%s] запуск сообщения о том что найден новый мэтч' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     #--------------------------------------------------------------------------------------
#     #--------------POST reuqest to get photo of match--------------------------------------
#     match_id = await db.get_match_id(message.from_user.id)
#     logger.warning('[%s@%s_%s] получл match_id [%s] из БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, match_id))
#     b64_str = await db.get_b64_profile_photo(match_id)
#     logger.warning('[%s@%s_%s] получл фотографию в формате base64 из БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     try:
#         async with aiofiles.open(Path(r'profiles/%s/match_photo.jpg' % message.from_user.id), 'wb') as match_photo:
#             await match_photo.write(base64.b64decode(b64_str[1:]))
#             logger.warning('[%s@%s_%s] раскодировал фотографию из base64 и сохранил в profiles/%s/match_photo.jpg' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
#     except:
#         logger.warning('[%s@%s_%s] ошибка во время открытия match_photo.jpg и записи в него строки base64.' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#         await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)
#   #--------------------------------------------------------------------------------------
#     try:
#         async with aiofiles.open(Path(r'./pic/find_match.png'), 'rb') as img:
#             await bot.send_photo(message.from_user.id, photo=img)
#     except:
#         logger.warning('[%s@%s_%s] не смог открыть find_match.png' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET)
#     send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO)
#     send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST)
#     end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG)
#     keyboard.row(wanna_meet_button, send_photo_button)
#     keyboard.row(send_request, end_dialog)
#     try:
#       async with aiofiles.open(Path(r'profiles/%s/match_photo.jpg' % message.from_user.id), 'rb') as match_photo:
#             await bot.send_photo(message.from_user.id, photo=match_photo, caption=texts.MATCH_INFO % (await db.get_name(match_id), await db.get_city(match_id), await db.get_reason(match_id)))
#             logger.warning('[%s@%s_%s] открыл фотографию мэтча' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
#             await bot.send_message(message.from_user.id, text=texts.FIND_MATCH, reply_markup= keyboard)
#             logger.info('[%s@%s_%s] отправил информацию о том что пара найдена' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#     except:
#             logger.warning('[%s@%s_%s] ошибка во время открытия match_photo.jpg.' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
#             await bot.send_message(id, text=texts.SMTHNG_GOES_WRONG)

# COMMANDS WHILE COMUNICATION
@dp.message_handler(state=Form.has_match, content_types=types.ContentTypes.TEXT)
async def forwarding_messages(message: types.Message, state: FSMContext):
        # Sending meeting request
        if message.text == buttons_texts.WANNA_MEET:
            #logger.info('[%s@%s_%s] запуск события "Хочу встретится"' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            # -------------------------------------------------------
            # -----POST request for UNISON THAT USER WANNA MEET------
            # async with aiohttp.ClientSession() as session:
            #   async with session.post(url='https://server.unison.dating/user/wanna_meet?user_id=%s'%data['user_id'], json={
            #     "match_id": await db.get_match_id(message.from_user.id)
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
            confirm_button = types.InlineKeyboardButton(text=buttons_texts.NORMAL_YES, callback_data='confirm_meeting')
            deny_button = types.InlineKeyboardButton(text=buttons_texts.NORMAL_NO, callback_data='are_u_deny_meeting')
            keyboard.row(confirm_button, deny_button)
            #sending message to match person
            await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.COFIRM_MEET % await db.get_name(message.from_user.id), reply_markup=keyboard)
        # Sending photo   
        elif message.text == buttons_texts.SEND_PHOTO:
            #logger.info('[%s@%s_%s] отправка фотографии мэтчу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await state.reset_state()
            #logger.warning('[%s@%s_%s] FSM state has_match OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
            await bot.send_message(message.from_user.id ,text=texts.UPLOAD_PHOTO_TO_MATCH)
            await Form.upload_photo_to_match.set()
            #logger.warning('[%s@%s_%s] FSM state upload_photo_to_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
        # Ending dialog
        elif message.text == buttons_texts.END_DIALOG:
            #logger.info('[%s@%s_%s] завершение общения' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await state.reset_state()
            #logger.warning('[%s@%s_%s] FSM state has_match OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
            confirm = types.InlineKeyboardButton(text=buttons_texts.NORMAL_YES, callback_data='confirm_leaving')
            deny = types.InlineKeyboardButton(text=buttons_texts.NORMAL_NO, callback_data='deny_leaving')
            keyboard.row(confirm, deny)
            await bot.send_message(message.from_user.id, text=texts.CONFIRMING_LEAVING_CHAT, reply_markup=keyboard)
        # Ask for help or report smthng
        elif message.text == buttons_texts.SEND_REQUEST:
            #logger.info('[%s@%s_%s] обращение к модерации' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await bot.send_message(message.from_user.id, text=texts.COMUNICATION_HELP)
            #logger.warning('[%s@%s_%s] FSM state has_match OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await state.reset_state()
            #logger.warning('[%s@%s_%s] FSM state get_help_message ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
            await Form.get_help_message.set()
        # Send message to ur match
        else:
            await bot.send_message(await db.get_match_id(message.from_user.id), text = '%s пишет: \n%s' % (await db.get_name(message.from_user.id), message.text))
    # If user try send smthng other than text
    # else:
    #   await bot.send_message(message.from_user.id, text=texts.COMMUNICATION_WARNING)
    #   logger.info('[%s@%s_%s] попытка отправить что то кроме текста мэтчу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

# IF U RECIVE MEETING MESSAGE AND AGREE TO IT
@dp.callback_query_handler(text='confirm_meeting', state=Form.has_match)
async def congirm_meeting_message(message: types.Message, state: FSMContext):
    logger.warning('[%s@%s_%s] отправил значение была ли встреча [True]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id))
    logger.warning('[%s@%s_%s] получил значение mathc_id из БД [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id, await db.get_match_id(message.from_user.id)))
    logger.warning('[%s@%s_%s] получил значение name из БД [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id, await db.get_name(message.from_user.id)))
    logger.warning('[%s@%s_%s] получил значение mathc_name из БД [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.id, await db.get_name(await db.get_match_id(message.from_user.id))))
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
    #   async with session.post(url='https://server.unison.dating/user/meet_confirm?user_id=%s' % message.from_user.id, json={ "match_id": await db.get_match_id(message.from_user.id) }) as resp: pass
    # ----------------------------------------------------------------
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
    if await db.get_city(message.from_user.id) == texts.SAINT_PETERSBURG:
      await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.MATCH_AGREE_SPBMSC % await db.get_name(message.from_user.id))
      logger.info('[%s@%s_%s] отправлено сообщение о согласии о свидании' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
      await bot.send_message(message.from_user.id, text=texts.GREETING_MENU_SPB_PLACE % await db.get_name(await db.get_match_id(message.from_user.id)))
      logger.info('[%s@%s_%s] отправлено сообщение от помошника с выбором места' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
      keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
      smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
      mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
      jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
      keyboard.add(smena_menu_button)
      keyboard.add(mickey_monkeys_button)
      keyboard.add(jack_chan_button)
      await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
      logger.info('[%s@%s_%s] вывод меню встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    elif db.get_city(message.from_user.id) == texts.MOSCOW_HELLO:
      await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.MATCH_AGREE_SPBMSC % await db.get_name(message.from_user.id))
      logger.info('[%s@%s_%s] отправлено сообщение о согласии о свидании' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
      await bot.send_message(message.from_user.id, text=texts.MOSCOW_HELLO % await db.get_name(message.from_user.id))
      logger.info('[%s@%s_%s] отправлено сообщение от помошника с выбором места' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
      keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
      double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
      propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
      she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
      keyboard.add(double_b)
      keyboard.add(propoganda)
      keyboard.add(she)
      await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
      logger.info('[%s@%s_%s] вывод меню встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await bot.send_message(message.from_user.id, text=texts.MATCH_AGREE_OTHER % await db.get_name(message.from_user.id))
        logger.info('[%s@%s_%s] вывод меню встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='are_u_deny_meeting', state=Form.has_match)
async def are_u_deny_meeting(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    yes = types.InlineKeyboardButton(text=buttons_texts.NORMAL_YES, callback_data='deny_meeting')
    no = types.InlineKeyboardButton(text=buttons_texts.NORMAL_NO, callback_data='confirm_meeting')
    keyboard.row(yes, no)
    await query.message.edit_text(text=texts.ARE_U_SURE_END, reply_markup=keyboard)
    logger.info('[%s@%s_%s] подтверждение или согласие на отказ от встречи' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='deny_meeting', state=Form.has_match)
async def deny_meeting(message: types.Message, state: FSMContext):
    await state.reset_state()
    logger.warning('[%s@%s_%s] FSM state has_match OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    #         "user_id": message.from_user.id,
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
    logger.info('[%s@%s_%s] отказ от встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))


# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |           TIME TO END COMUNICATING                                                                                                                                        |
# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.callback_query_handler(text='callback_look')
async def dont_like_look(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] причина выхода из диалога [не понравился внешне]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    await db.set_reason_to_stop(message.from_user.id, 'не понравился внешне')
    logger.warning('[%s@%s_%s] отослал причину в остановке общения [не понравился внешне]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
    unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
    keyboard.add(ok_meeting_button)
    keyboard.add(unlike_meeting_button)
    await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id)), reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню о том состоялась ли встреча' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='callback_comunication')
async def dont_like_comunication(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] причина выхода из диалога [не понравилось общение]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    await db.set_reason_to_stop(message.from_user.id, 'не понравилось общение')
    logger.warning('[%s@%s_%s] причина выхода из диалога [не понравилось общение]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
    unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
    keyboard.add(ok_meeting_button)
    keyboard.add(unlike_meeting_button)
    await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id)), reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню о состоянии встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))


@dp.callback_query_handler(text='callback_like')
async def everything_ok(message: types.Message, state: FSMContext):
    logger.info('[%s@%s_%s] причина выхода из диалога [понравился, но время общения истекло]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    await db.set_reason_to_stop(message.from_user.id, 'Понравился, но время общения истекло')
    logger.warning('[%s@%s_%s] причина выхода из диалога [понравился, но время общения истекло]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
    unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
    keyboard.add(ok_meeting_button)
    keyboard.add(unlike_meeting_button)
    await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id)), reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню о состоянии встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

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
    await state.reset_state()
    await bot.send_message(message.from_user.id, text=texts.CALLBACK_REASON)
    logger.info('[%s@%s_%s] другая причина отказа' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await Form.callback_other.set()
    logger.warning('[%s@%s_%s] FSM state callback_other ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
@dp.message_handler(state=Form.callback_other, content_types= types.ContentTypes.ANY)
async def set_message_other(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await db.set_reason_to_stop(message.from_user.id, message.text)
        logger.warning('[%s@%s_%s] установить причину отказа "%s"' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text))
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state callback_other OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
        unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
        keyboard.add(ok_meeting_button)
        keyboard.add(unlike_meeting_button)
        await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id)), reply_markup=keyboard)
        logger.info('[%s@%s_%s] вывод меню о состоянии встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
         await bot.send_message(message.from_user.id, text=texts.NOT_TEXT_MESSAGE)
         logger.info('[%s@%s_%s] попытка отправить что то кроме текста' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
         return


@dp.callback_query_handler(text='unlike_meeting')
async def set_was_meeting_no(message: types.Message, state: FSMContext):
    await db.set_meeting_status(message.from_user.id, False)
    logger.warning('[%s@%s_%s] отправить статус стречи [False]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
    logger.info('[%s@%s_%s] не понравилась встреча' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await Form.unlike_meeting.set()
    logger.warning('[%s@%s_%s] FSM state unlike_meeting ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
@dp.message_handler(state=Form.unlike_meeting, content_types= types.ContentTypes.ANY)
async def set_meeting_reaction(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        await db.set_meeting_reaction(message.from_user.id, message.text)
        logger.warning('[%s@%s_%s] занесение отзыва о встрече [%s] в БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text))
        state.reset_state()
        logger.warning('[%s@%s_%s] FSM state unlike_meeting OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
        dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
        dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
        dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
        keyboard.add(dont_like_look_button)
        keyboard.add(dont_like_behavior_button)
        keyboard.add(dont_like_place_button)
        await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)
        logger.info('[%s@%s_%s] вывод просьбы оставить фидбек когда встреча не понравилась' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        await bot.send_message(message.from_user.id, text=texts.NOT_TEXT_MESSAGE)
        logger.info('[%s@%s_%s] попытка отправить то что не является текстом' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        return


@dp.callback_query_handler(text='ok_meeting')
async def set_was_meeting_yes(message: types.Message, state: FSMContext):
  await db.set_meeting_status(message.from_user.id, True)
  logger.warning('[%s@%s_%s] отправил статус была ли встреча [True]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
  logger.info('[%s@%s_%s] вывод меню оценки встречи' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='all_like')
async def set_meeting_reaction_ok(message: types.Message, state: FSMContext):
    await db.set_meeting_reaction(message.from_user.id, 'Встреча понравилась')
    logger.warning('[%s@%s_%s] установлена Реакция на встречу [Встреча понравилась]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
    await db.set_match_id_manualy(message.from_user.id, 0)
    logger.warning('[%s@%s_%s] сброшен match_id' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_reason_to_stop(message.from_user.id, 'Вышло время')
    logger.warning('[%s@%s_%s] установлена причина выхода из диалога [Время вышло]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await schedule_jobs(message.from_user.id, state, message.from_user.first_name, message.from_user.last_name)

@dp.callback_query_handler(text='neutral_meeting')
async def set_meeting_reaction_neutral(message: types.Message, state: FSMContext):
    await db.set_meeting_reaction(message.from_user.id, 'Ничего особенного')
    logger.warning('[%s@%s_%s] установлена Реакция на встречу [Ничего особенного]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
    dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
    dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
    keyboard.add(dont_like_look_button)
    keyboard.add(dont_like_behavior_button)
    keyboard.add(dont_like_place_button)
    await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню того что не понравилось при встрече' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='dont_like_meeting')
async def set_meeting_reaction_negative(message: types.Message, state: FSMContext):
    await db.set_meeting_reaction(message.from_user.id, 'Не понравилась')
    logger.warning('[%s@%s_%s] установлена Реакция на встречу [Не понравилась]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
    dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
    dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
    keyboard.add(dont_like_look_button)
    keyboard.add(dont_like_behavior_button)
    keyboard.add(dont_like_place_button)
    await bot.send_message(message.from_user.id, text=texts.ABOUT_MEETING, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню того что не понравилось при встрече' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))

@dp.callback_query_handler(text='meeting_look')
async def set_why_meeting_bad_look(message: types.Message, state: FSMContext):
  await db.set_why_meeting_bad(message.from_user.id, 'Не понравился внешне')
  logger.warning('[%s@%s_%s] установлена Реакция на встречу [Не понравился внешне]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
  # --------------POST request to END MATCHING--------------
  # async with aiohttp.ClientSession() as session:
  #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
  #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id),
  #     "was_meeting": await db.is_meeting(message.from_user.id),
  #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id),
  #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id)
  #   }) as resp: pass
  # --------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
  await db.set_match_id_manualy(message.from_user.id, 0)
  logger.warning('[%s@%s_%s] сброшен match id' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
  await db.set_reason_to_stop(message.from_user.id, 'Время вышло')
  logger.warning('[%s@%s_%s] сброшен match id' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
  logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
  await schedule_jobs(message.from_user.id, state, message.from_user.first_name, message.from_user.last_name)

@dp.callback_query_handler(text='meeting_behavior')
async def set_why_meeting_bad_behavior(message: types.Message, state: FSMContext):
    await db.set_why_meeting_bad(message.from_user.id, 'Не понравилось поведение')
    logger.warning('[%s@%s_%s] установлена Реакция на встречу [Не понравилось поведение]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    # --------------POST request to END MATCHING--------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
    #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id),
    #     "was_meeting": await db.is_meeting(message.from_user.id),
    #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id),
    #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id)
    #   }) as resp: pass
    # --------------------------------------------------------
    await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
    await db.set_match_id_manualy(message.from_user.id, 0)
    logger.warning('[%s@%s_%s] сброшен match id' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_reason_to_stop(message.from_user.id, 'Время вышло')
    logger.warning('[%s@%s_%s] установлена причина остановки общения [Время вышло]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await schedule_jobs(message.from_user.id, state, message.from_user.first_name, message.from_user.last_name)

@dp.callback_query_handler(text='meeting_place')
async def set_why_meeting_bad_place(message: types.Message, state: FSMContext):
    await db.set_why_meeting_bad(message.from_user.id, 'Не понравился внешне')
    logger.warning('[%s@%s_%s] установлена реакция на встречу [Не понравился внешне]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await state.reset_state()
    # --------------POST request to END MATCHING--------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
    #     "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id),
    #     "was_meeting": await db.is_meeting(message.from_user.id),
    #     "meeting_reaction": await db.get_meeting_reaction(message.from_user.id),
    #     "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id)
    #   }) as resp: pass
    # --------------------------------------------------------
    await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
    await db.set_match_id_manualy(message.from_user.id, 0)
    logger.warning('[%s@%s_%s] сброшен match_id' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_reason_to_stop(message.from_user.id, 'Время вышло')
    logger.warning('[%s@%s_%s] установлена причина остановки общения [Время вышло]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await schedule_jobs(message.from_user.id, state, message.from_user.first_name, message.from_user.last_name)

# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                               MEETING PLACE                                                                                                                               |
# +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

# ____________SPB_______________________
@dp.callback_query_handler(text='smena', state=Form.has_match)
async def show_smena(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_smena')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  logger.info('[%s@%s_%s] показано описание кафе Смена' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  await query.message.edit_text(text=texts.SMENA_COFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_smena', state=Form.has_match)
async def choose_smena(query: types.CallbackQuery, state: FSMContext):
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
  logger.info('[%s@%s_%s] выбрано кафе Смена' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.SMENA_MEET_PLACE)

@dp.callback_query_handler(text='mickey', state=Form.has_match)
async def show_mickey(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_mickey')
    other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
    keyboard.add(this_place)
    keyboard.add(other_place)
    logger.info('[%s@%s_%s] показано описание кафе Mickey & Monkeys' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await query.message.edit_text(text=texts.MICKEY_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_mickey', state=Form.has_match)
async def choose_mickey(query: types.CallbackQuery, state: FSMContext):
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
    await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
    await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.MICKEY_MEET_PLACE)
    logger.info('[%s@%s_%s] выбрано кафе Mickey & Monkeys' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='jack_and_chan', state=Form.has_match)
async def show_jack(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_jack')
    other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
    keyboard.add(this_place)
    keyboard.add(other_place)
    await query.message.edit_text(text=texts.JACK_CAFE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] показано описание кафе Jack & Chan' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='choose_jack', state=Form.has_match)
async def choose_jack(query: types.CallbackQuery, state: FSMContext):
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
    await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
    await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.JACK_MEET_PLACE)
    logger.info('[%s@%s_%s] выбрано кафе Jack & Chan' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# ____________MSC_______________________
@dp.callback_query_handler(text='double_b', state=Form.has_match)
async def doube_b(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_double_b')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await query.message.edit_text(text=texts.DOUBLE_B_CAFE, reply_markup=keyboard)
  logger.info('[%s@%s_%s] показано описание кафе Double B' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='choose_double_b', state=Form.has_match)
async def choose_double_b(query:types.CallbackQuery, state: FSMContext):
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
  await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.DOUBLE_B_PLACE)
  logger.info('[%s@%s_%s] выбрано кафе Double B' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='propoganda', state=Form.has_match)
async def propoganda(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_propoganda')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await query.message.edit_text(text=texts.PROPOGANDA_CAFE, reply_markup=keyboard)
  logger.info('[%s@%s_%s] показано описание кафе Propoganda' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='choose_propoganda', state=Form.has_match)
async def choose_propoganda(query: types.CallbackQuery, state: FSMContext):
  await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
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
  await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.PROPOGANDA_PLACE)
  logger.info('[%s@%s_%s] выбрано кафе Propoganda' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='she', state=Form.has_match)
async def she(query: types.CallbackQuery, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_she')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await query.message.edit_text(text=texts.SHE_CAFE, reply_markup=keyboard)
  logger.info('[%s@%s_%s] показано описание кафе She' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='choose_she', state=Form.has_match)
async def choose_she(query: types.CallbackQuery, state: FSMContext):
  await query.message.edit_text(text=texts.FIN_MEET_MESSAGE)
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
  await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.SHE_PLACE)
  logger.info('[%s@%s_%s] выбрано кафе She' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='spb_menu', state=Form.has_match)
async def spb_menu(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
    mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
    jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
    keyboard.add(smena_menu_button)
    keyboard.add(mickey_monkeys_button)
    keyboard.add(jack_chan_button)
    await query.message.edit_text(text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню с выбором места в СПб' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

@dp.callback_query_handler(text='msc_menu', state=Form.has_match)
async def msc_menu(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
    propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
    she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
    keyboard.add(double_b)
    keyboard.add(propoganda)
    keyboard.add(she)
    await query.message.edit_text(text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню с выбором места в МСК' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

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
                                                                          await db.get_name(message.from_user.id),
                                                                          message.from_user.id), parse_mode='markdown')
  # ----------------------------------------------------
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ends)
async def payment_ends(message: types.Message, state: FSMContext):
  await db.set_subscribtion_status(message.from_user.id, False)
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
  if await db.is_subscribed(message.from_user.id):
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
  logger.info('[%s@%s_%s] отмена выхода по кнопке [❌ Завершить диалог]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
  await query.message.delete()
  await Form.has_match.set()
  logger.warning('[%s@%s_%s] FSM state has_match ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))

# LEAVE THE CHAT
@dp.callback_query_handler(text='confirm_leaving')
async def delete_match_info(query: types.CallbackQuery, state: FSMContext):
    logger.info('[%s@%s_%s] выход из диалога по кнопке [❌ Завершить диалог]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await state.reset_state()
    logger.warning('[%s@%s_%s] FSM state has_match OFF' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
    comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
    ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
    other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
    keyboard.add(look_button, comunication_button)
    keyboard.add(ignore_button, other_button)
    await query.message.edit_text(text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод меню прекращения общения' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))


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
    #       "user_id": await db.get_match_id(query.from_user.id),
    #         "event_type": "bot_chating_partner_end_reason_ugly"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    await db.set_reason_to_stop(query.from_user.id, 'Не понравился внешне')
    logger.warning('[%s@%s_%s] отправлено значение причины остановки общения [Не понравился внешне]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to stop MATCH----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % query.from_user.id, json={
    #     "reason": await db.get_reason_to_stop(query.from_user.id)
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": await db.get_match_id(query.from_user.id),
    #         "event_type": "bot_chating_ended_partner_choosing"
    #       }
    #     ]
    #   }) as resp: pass
    # -------------------------------------------------------------------------------------
    keyboard = types.ReplyKeyboardRemove()
    logger.warning('[%s@%s_%s] вытащен из БД match id' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # sending MATCH USER message about leaving the chat-----------------
    await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)
    logger.info('[%s@%s_%s] вывод сообщения о том что пользователь покинул чат' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # __________________________________________________________________
    if scheduler.get_job('unmatch_%s' % query.from_user.id, 'default'):
        scheduler.remove_job('unmatch_%s' % query.from_user.id, 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для пользователя' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    if scheduler.get_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default'):
        scheduler.remove_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для его пары' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # DELETE MATCH INFO --------------------------------------------------------------------------------------------
    await db.set_match_status(query.from_user.id, False)
    logger.warning('[%s@%s_%s] статус пользователя "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_match_status(await db.get_match_id(query.from_user.id), False)
    logger.warning('[%s@%s_%s] статус его пары "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(query.from_user.id, state)
    state = dp.current_state(chat=await db.get_match_id(query.from_user.id), user=await db.get_match_id(query.from_user.id))
    logger.warning('[%s@%s_%s] FSM get state of match' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await state.set_state(None)
    logger.warning('[%s@%s_%s] FSM state no_match ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] вывод пары в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(await db.get_match_id(query.from_user.id), state)



@dp.callback_query_handler(text='ignore')
async def show_ignore(query: types.CallbackQuery, state: FSMContext):
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
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_self_end_reason_noreply"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    await db.set_reason_to_stop(query.from_user.id, 'собеседник не отвечает')
    logger.warning('[%s@%s_%s] установка причины окончания остановки [собеседник не отвечает]' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to stop MATCH----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
    #     "reason": await db.get_reason_to_stop(message.from_user.id)
    #     }) as resp: pass
    keyboard = types.ReplyKeyboardRemove()

    #--------------------------------------------------------------------------------------
    #----------------POST for some STATISTICS----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_ended_partner_choosing"
    #       }
    #     ]
    #   }) as resp: pass
    await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] вывод сообщения о том что пользователь покинул чат' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # __________________________________________________________________
    if scheduler.get_job('unmatch_%s' % query.from_user.id, 'default'):
        scheduler.remove_job('unmatch_%s' % query.from_user.id, 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для пользователя' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    if scheduler.get_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default'):
        scheduler.remove_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для его пары' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # DELETE MATCH INFO --------------------------------------------------------------------------------------------
    await db.set_match_status(query.from_user.id, False)
    logger.warning('[%s@%s_%s] статус пользователя "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_match_status(await db.get_match_id(query.from_user.id), False)
    logger.warning('[%s@%s_%s] статус его пары "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(query.from_user.id, state, query.from_user.first_name, query.from_user.last_name, True, query=query)
    state = dp.current_state(chat=await db.get_match_id(query.from_user.id), user=await db.get_match_id(query.from_user.id))
    logger.warning('[%s@%s_%s] FSM get state of match' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await state.set_state(None)
    logger.warning('[%s@%s_%s] FSM state no_match ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] вывод пары в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(await db.get_match_id(query.from_user.id), state)

@dp.callback_query_handler(text='dont_like_comunication')
async def dont_like_comunication(query: types.CallbackQuery, state: FSMContext):
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
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_partner_end_reason_stupid"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    await db.set_reason_to_stop(query.from_user.id, "не понравилось общение")
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to stop MATCH----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
    #     "reason": await db.get_reason_to_stop(message.from_user.id)
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    #---------------STOP MATCH USER-------------------------------------------------------------
    keyboard = types.ReplyKeyboardMarkup()
    #--------------------------------------------------------------------------------------
    #----------------POST for some STATISTICS----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_ended_partner_choosing"
    #       }
    #     ]
    #   }) as resp: pass
    await bot.send_message(await db.get_match_id(query.from_user.id), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] вывод сообщения о том что пользователь покинул чат' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # __________________________________________________________________
    if scheduler.get_job('unmatch_%s' % query.from_user.id, 'default'):
        scheduler.remove_job('unmatch_%s' % query.from_user.id, 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для пользователя' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    if scheduler.get_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default'):
        scheduler.remove_job('unmatch_%s' % await db.get_match_id(query.from_user.id), 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для его пары' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    # DELETE MATCH INFO --------------------------------------------------------------------------------------------
    await db.set_match_status(query.from_user.id, False)
    logger.warning('[%s@%s_%s] статус пользователя "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await db.set_match_status(await db.get_match_id(query.from_user.id), False)
    logger.warning('[%s@%s_%s] статус его пары "есть пара" - False' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(query.from_user.id, state, query.from_user.first_name, query.from_user.last_name, True, query=query)
    state = dp.current_state(chat=await db.get_match_id(query.from_user.id), user=await db.get_match_id(query.from_user.id))
    logger.warning('[%s@%s_%s] FSM get state of match' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await state.set_state(None)
    logger.warning('[%s@%s_%s] FSM state no_match ON' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    logger.info('[%s@%s_%s] вывод пары в планировщик и вывод нужного меню' % (query.from_user.id, query.from_user.first_name, query.from_user.last_name))
    await schedule_jobs(await db.get_match_id(query.from_user.id), state)

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
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_partner_end_reason_else"
    #       }
    #     ]
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    await Form.why_dont_like.set()
@dp.message_handler(state=Form.why_dont_like, content_types=types.ContentTypes.TEXT)
async def set_reason(message: types.Message, state: FSMContext):
    await db.set_reason_to_stop(message.from_user.id, message.text)
    await state.reset_state(with_data=False)
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to stop MATCH----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={
    #     "reason": await db.get_reason_to_stop(message.from_user.id)
    #   }) as resp: pass
    #--------------------------------------------------------------------------------------
    #---------------STOP MATCH USER-------------------------------------------------------------
    keyboard = types.ReplyKeyboardMarkup()
    #--------------------------------------------------------------------------------------
    #----------------POST for some STATISTICS----------------------------------------------
    # async with aiohttp.ClientSession() as session:
    #   async with session.post(url='https://api.amplitude.com/2/httpapi', json={
    #     "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
    #     "events": [
    #       {
    #         "user_id": await db.get_match_id(message.from_user.id),
    #         "event_type": "bot_chating_ended_partner_choosing"
    #       }
    #     ]
    #   }) as resp: pass
    await bot.send_message(await db.get_match_id(message.from_user.id), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] вывод сообщения о том что пользователь покинул чат' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    # __________________________________________________________________
    if scheduler.get_job('unmatch_%s' % message.from_user.id, 'default'):
        scheduler.remove_job('unmatch_%s' % message.from_user.id, 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для пользователя' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    if scheduler.get_job('unmatch_%s' % await db.get_match_id(message.from_user.id), 'default'):
        scheduler.remove_job('unmatch_%s' % await db.get_match_id(message.from_user.id), 'default')
    logger.warning('[%s@%s_%s] удаление задачи unmatch для его пары' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    # DELETE MATCH INFO --------------------------------------------------------------------------------------------
    await db.set_match_status(message.from_user.id, False)
    logger.warning('[%s@%s_%s] статус пользователя "есть пара" - False' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await db.set_match_status(await db.get_match_id(message.from_user.id), False)
    logger.warning('[%s@%s_%s] статус его пары "есть пара" - False' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] выход в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await schedule_jobs(message.from_user.id, state, message.from_user.first_name, message.from_user.last_name)
    state = dp.current_state(chat=await db.get_match_id(message.from_user.id), user=await db.get_match_id(message.from_user.id))
    logger.warning('[%s@%s_%s] FSM get state of match' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await state.set_state(None)
    logger.warning('[%s@%s_%s] FSM state no_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    logger.info('[%s@%s_%s] вывод пары в планировщик и вывод нужного меню' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    await schedule_jobs(await db.get_match_id(message.from_user.id), state)

# +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                   FORWARDING PHOTOS                                                                                                                                     |
# +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.message_handler(state=Form.upload_photo_to_match, content_types=types.ContentTypes.ANY)
async def upload_photo_to_match(message: types.Message, state: FSMContext):
    if message.content_type=='photo':
        logger.info('[%s@%s_%s] загрузка фотки для отправки' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        error_status = await db.get_error_status(message.from_user.id)
        logger.warning('[%s@%s_%s] получение статуса ошибки [%s]' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name, error_status))
        if message.media_group_id:
            if not error_status:
                logger.warning('[%s@%s_%s] попытка отправить не 1 фотографию, а медиа группу' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
                await db.set_error_status(message.from_user.id, True)
                await message.answer(text=texts.MEDIA_GROUP_ERROR)
                await db.set_error_status(message.from_user.id, False)
            return
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
        logger.warning('[%s@%s_%s] получение match id из БД' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await bot.send_photo(await db.get_match_id(message.from_user.id), photo=photo_id)
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state upload_photo_to_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await Form.has_match.set()
        logger.warning('[%s@%s_%s] FSM state has_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        logger.info('[%s@%s_%s] попытка залить фотографию как документ или что то что не является фотографией' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.answer(text=texts.OOPS_PHOTO)
        return


# +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
# |                 COMLAIN WHILE COMUNICATION                                                                                                                            |
# +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+
@dp.message_handler(state=Form.get_help_message, content_types=types.ContentTypes.ANY)
async def get_comunication_help_message(message: types.Message, state: FSMContext):
    if message.content_type == 'text':
        help_message = '\n\n' + message.text
        await state.reset_state()
        logger.warning('[%s@%s_%s] FSM state get_help_message OFF' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await bot.send_message(-776565232, text=texts.COMPLAIN_MODERATION % (message.from_user.id,
                                                                            await db.get_name(message.from_user.id),
                                                                            message.from_user.id,
                                                                            help_message), parse_mode='Markdown')
        logger.info('[%s@%s_%s] отправлено сообщение в чат модерации' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
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
        logger.warning('[%s@%s_%s] FSM state has_match ON' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
    else:
        logger.info('[%s@%s_%s] попытка отправить в сообщении что то кроме текста' % (message.from_user.id, message.from_user.first_name, message.from_user.last_name))
        await message.answer(text=texts.INPUT_ERROR)
        return
  

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=scheduler.start())    
