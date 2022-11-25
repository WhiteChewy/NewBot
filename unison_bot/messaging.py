import os
import aioschedule
import logging
import datetime
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json
import asyncio
import base64
import random

from aiogram.dispatcher.filters import Filter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN) 
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()


# STATES FOR STATE MACHINE
class Form(StatesGroup):
  help = State()
  why_dont_like=State()
  upload_photo_to_match = State()
  get_help_message = State()
  callback_other = State()
  unlike_meeting = State()
  
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


async def get_match_id(message: types.Message):
  if message.from_user.id == 5951187826:
    return 877505237
  else:
    return 5951187826


#ASK server if has match or not
async def is_match():
  # GET INFO ABOUT MATCH IF THERE IT MATCH RETURN TRUE
  # CHECK SERVER IF THERE IS MATCHES
  #
  #---------------------------------
  return data['has_match']

# CHECK USER ABOUT SUBSCRIBE
async def is_premium(state: FSMContext):
  #data = await state.get_data()
  return data['subscribtion']

# CHECK IF TODAY MONDAY
async def is_monday():
  if not datetime.date.today().weekday():
    return True
  else:
    return False

# SET STATE UNMATCHED
async def set_state_unmatch(state: FSMContext):
  #await state.reset_state(with_data=False)
  #await state.update_data(has_match = False)
  data['has_match'] = False
  #await state.update_data(match_id = 0)
  #data['match_id'] = 0
  # --------------------------------------------------------
  # -------------POST request for some statistics-----------
  #requests.post(url='https://api.amplitude.com/2/httpapi', json={
  #"api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #"events": [
  #  {
  #    "user_id": data['user_id'],
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
  await bot.send_message(data['user_id'], text=texts.CALLBACK, reply_markup=keyboard)
  

# SET STATE ONE_DAY_TO_UNMATCH
async def set_state_one_day_to_unmatch(state: FSMContext):
  #data = await state.get
  await state.reset_state(with_data=False)
  #scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=1), args=(state,))
  scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(state,))
  await Form.has_match.set()
  await bot.send_message(data['user_id'], text=texts.ONE_DAY_TO_UNMATCH % data['match_name'])
  await state.reset_state(with_data=False)
  

# SET STATE TO HAS_MATCH
async def set_state_has_match(state: FSMContext):
  await state.update_data(has_match=True)
  data['has_match'] = True
  #new_date = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=6), datetime.time(hour=9, minute=0))
  new_date = datetime.datetime.now() + datetime.timedelta(minutes=30)
  scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=new_date, args=(state,))
  #await state.update_data(tag_begin_comunocation = True)
  data['tag_begin_comunication'] = True
  #await state.update_data(has_match = 0)
  data['has_match'] = True
  #await state.update_data(tag_first_time = False)
  data['tag_first_time'] = False
  await bot.send_message(data['user_id'], text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  
  #--------------------------------------------------------------------------------------
  await Form.has_match.set()
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(data['user_id'], photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET) #, callback_data='wanna_meet')
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO) #, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST) #, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG) #, callback_data='end_dialog')
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  with open(data_match['profile_photo'], 'rb') as profile_pic:
    await bot.send_photo(data['user_id'], photo=profile_pic, caption=texts.MATCH_INFO % (data_match['name'], data_match['city'], data_match['reason']))
  await bot.send_message(data['user_id'], text=texts.FIND_MATCH, reply_markup= keyboard)
  await get_advice(state)
  

async def schedule_jobs(state: FSMContext):
  date_today = datetime.date.today()
  # IF USER NOT SUBSCRIBED
  if not await is_premium(state):
    # IF TODAY IS MONDAY
    if await is_monday():
      if await is_match():
        # IF THERE IS MATCH GET INFO ABOUT

        scheduler.add_job(set_state_one_day_to_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=6), args=(state, ))
      else:
        scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=30), args=(state,))
    # IF TODAY IS NOT MONDAY
    else:
      # IF NOT MONDAY - REPEAT AFTER days_till_monday DAYS
      days_till_monday = 7 - datetime.date.today().weekday()
      new_date = datetime.date.today() + datetime.timedelta(days=days_till_monday)
      run_date = datetime.datetime.combine(new_date, datetime.time(hour=9, minute=0))
      scheduler.add_job(schedule_jobs, 'date', run_date=run_date, args=(state,)) # add job to scheduler
  # IF USER SUBSCRIBED
  else:
    if await is_match():
      # IF THERE IS MATCH GET INFO ABOUT
      
      await set_state_has_match(state=state)
    # IF THERE IS NO MATCH REPEAT AFTER 10 MINUTES
    else:
      scheduler.add_job(schedule_jobs, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=10), args=(state,))
      #data = await state.get_data()
      query = types.CallbackQuery
      await state.reset_state(with_data=False)
      keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
      if data['subscribtion']:
          subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
      else:
          subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
      write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
      were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
      if not data['matching_pause']:
        pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
      else:
        pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
      keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
      with open('./pic/main_photo.png', 'rb') as img_file:
        await bot.send_photo(data['user_id'], photo=img_file)
      if not data['has_match']:
        await Form.no_match.set()
      else:
        await Form.has_match.set()
      if not data['matching_pause']:
        await bot.send_message(data['user_id'], text=texts.MAIN_MENU, reply_markup=keyboard)
      else:
        await bot.send_message(data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)
      
      

@dp.message_handler(commands='start')
async def messaging_start(message: types.Message, state: FSMContext):
    #data = await state.get_data()
    
    # if message.from_user.id == 877505237:
    #   await state.update_data(user_id = 877505237)
    #   await state.update_data(match_id= 891872881)
    #   await state.update_data(match_photo= './pic/Head.png')
    #   await state.update_data(match_city = 'Санкт-Петербург')
    #   await state.update_data(match_name = 'Илья')
    #   await state.update_data(match_reason = 'Серьезные отношения')
    #   await state.update_data(match_wanna_meet = False)
    # else:
    #   data['user_id'] = 891872881
    #   data['match_id']= 877505237
    #   data['name'] = 'Илья'
    #   data['match_photo']= './pic/profiles/877505237/main_profile_photo.jpg'
    #   data['match_city'] = 'Санкт-Петербург'
    #   data['match_name'] = 'Никита'
    #   data['match_reason'] = 'Серьезные отношения'
    #   data['match_wanna_meet'] = False
    await state.reset_state(with_data=False)
    await schedule_jobs(state=state)
    scheduler.start()

@dp.message_handler(commands='start_nomatch')
async def start_nomatch(message: types.Message, state: FSMContext):
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
       subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
       subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU, )
    reply_keyboard.add(main_menu)
    await Form.no_match.set()
    with open('./pic/main_photo.png', 'rb') as img_file:
     await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
    
    


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=Form.no_match)
async def message_reaction_if_text(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  if message.text == buttons_texts.MAIN_MENU and not data['has_match']:
    await state.reset_state(with_data=False)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not data['matching_pause']:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
    reply_keyboard.add(main_menu)
    with open('./pic/main_photo.png', 'rb') as img_file:
      await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
    if not data['matching_pause']:
      await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
    else:
      await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
  elif data['has_match']:
    await bot.send_message(data_match['user_id'], text=message.text)

@dp.message_handler(commands='start_match', state=Form.has_match)
async def set_has_macth(message: types.message, state: FSMContext):
  data['has_match'] = True

@dp.callback_query_handler(text='main_menu', state=Form.no_match)
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not data['matching_pause']:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    if not data['matching_pause']:
      await query.message.edit_text(text=texts.MAIN_MENU)
      await query.message.edit_reply_markup(reply_markup=keyboard)
    else:
      await query.message.edit_text(text=texts.PAUSE_MAIN_MENU)
      await query.message.edit_reply_markup(reply_markup=keyboard)
    
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------CHECKING, GETTING AND CANCEL SUBSCRIBTION----------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='have_subscribtion', state=Form.no_match)
async def abandon_subsribtion(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    #requests.post(url='https://api.amplitude.com/2/httpapi', json={
  #"api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  #"events": [
  #  {
  #    "user_id": data['user_id'],
  #    "event_type": "bot_menu_subscribe_btn"
  #  }
  #]
#})
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    abandon_button = types.InlineKeyboardButton(text=buttons_texts.DENY, callback_data='deny_subscribtion')
    back_button = types.InlineKeyboardButton(text=buttons_texts.BACK, callback_data='main_menu')
    keyboard.add(abandon_button, back_button)
    await query.message.edit_text(text=texts.WHAT_TO_DO)
    await query.message.edit_reply_markup(reply_markup=keyboard)

@dp.callback_query_handler(text='doesnt_have_subscribtions', state=Form.no_match)
async def subscribe(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    await state.reset_state(with_data=False)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_menu_subscribe_btn"
#     }
#   ]
# })
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        get_subscribe = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSCRIBE, callback_data='u_have_subscription')
    else:
        get_subscribe = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSCRIBE, callback_data='subscribe')
    keyboard.add(get_subscribe)
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    await query.message.edit_text(text=texts.SUBSCRIBE_INFO)
    await query.message.edit_reply_markup(reply_markup=keyboard)
    

@dp.callback_query_handler(text='u_have_subscription', state=Form.no_match)
async def error_u_have_subscribtion(query: types.CallbackQuery, state: FSMContext):
    # data = await state.get_data()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_subscribe_btn"
#     }
#   ]
# })
    #--------------------------------------------------------------------------------------   
    await query.message.edit_text(text=texts.SUBSCRIBE_ERROR_HAD)

@dp.callback_query_handler(text='subscribe', state=Form.no_match)
async def pay_subscribe(query:types.CallbackQuery, state: FSMContext):
    #data = await state.get_date()
    await state.reset_state(with_data=False)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for getting payment url----------------------------
#     request = requests.post(url='https://server.unison.dating/user/payment/request?user_id=%s' % data['user_id'], json={
#     "amount": "870"
# })
    #--------------------------------------------------------------------------------------   
    #await state.update_data(payment_url=request.text['payment_url'])
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    main_menu_button = types.InlineKeyboardButton(text=buttons_texts.BACK_TO_THE_MENU, callback_data='main_menu')
  
    keyboard.add(main_menu_button)
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    #await query.message.edit_text(text=texts.PAY_URL % request.text['payment_url'], reply_markup=keyboard)
    await query.message.edit_text(text=texts.PAY_URL % data['payment_url'], reply_markup=keyboard)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_subscribe_pay_btn"
#     }
#   ]
# })
    

@dp.callback_query_handler(text='deny_subscribtion', state=Form.no_match)
async def abbandon_subscribe(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_date()
    #await state.update_data(subscribtion=False)
    data['subscribtion'] = False
    await query.answer(texts.SUCCESS_UNSUBSCRIBE)
    await query.message.delete()
    with open('./pic/where_menu.png', 'rb') as file_img:
      await bot.send_photo(data['user_id'], photo=file_img)
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_subscribe_cancel"
#     }
#   ]
# })
    #--------------------------------------------------------------------------------------   
    #----------------------POST request for some statistics--------------------------------
    req = requests.post(url='https://server.unison.dating/user/payment/cancel?user_id%s' % data['user_id'], json={})
    #-------------------------------------------------------------------------------------- 
    if data['has_match']:
      await Form.has_match.set()
    else:
      await Form.no_match.set()
    await bot.send_message(data['user_id'], text=texts.PAYMENT_CANCEL)
    
  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ********************************GAME SECTION******************************************************************************************************************************************************
@dp.callback_query_handler(state = Form.game1)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_ONE)
  await bot.send_message(data_match['user_id'], text=texts.GAME_ONE)
@dp.callback_query_handler(state = Form.game2)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_TWO)
  await bot.send_message(data_match['user_id'], text=texts.GAME_TWO)
  
@dp.callback_query_handler(state = Form.game3)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_THREE)
  await bot.send_message(data_match['user_id'], text=texts.GAME_THREE)
  
@dp.callback_query_handler(state = Form.game4)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_FOUR)
  await bot.send_message(data_match['user_id'], text=texts.GAME_FOUR)
  
@dp.callback_query_handler(state = Form.game5)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_FIVE)
  await bot.send_message(data_match['user_id'], text=texts.GAME_FIVE)
  
@dp.callback_query_handler(state = Form.game6)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_SIX)
  await bot.send_message(data_match['user_id'], text=texts.GAME_SIX)
  
@dp.callback_query_handler(state = Form.game7)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_SEVEN)
  await bot.send_message(data_match['user_id'], text=texts.GAME_SEVEN)
  
@dp.callback_query_handler(state = Form.game8)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_EIGHT)
  await bot.send_message(data_match['user_id'], text=texts.GAME_EIGHT)
  
@dp.callback_query_handler(state = Form.game9)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_NINE)
  await bot.send_message(data_match['user_id'], text=texts.GAME_NINE)
  
@dp.callback_query_handler(state = Form.game10)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_TEN)
  await bot.send_message(data_match['user_id'], text=texts.GAME_TEN)
  
@dp.callback_query_handler(state = Form.game11)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_ELEVEN)
  await bot.send_message(data_match['user_id'], text=texts.GAME_ELEVEN)
  
@dp.callback_query_handler(state=Form.game12)
async def game_one(state: FSMContext):
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match()
  await bot.send_message(data['user_id'], text=texts.GAME_TWELVE)
  await bot.send_message(data_match['user_id'], text=texts.GAME_TWELVE)
  
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------HELP SECTION--------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='help', state=Form.no_match)
async def get_help(query: types.CallbackQuery, state: FSMContext):
  #state.update_data(help=True)
  data['help']=True
  await state.reset_state(with_data=False)
    #data = await stet.get_data()
  #-------------------------------------------------------------------------
  #----------------------POST request for some STATISTICS-------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_menu_support_btn"
#     }
#   ]
# })
  #-------------------------------------------------------------------------
  
  #-------------------------------------------------------------------------
  #-------------------INSTUCTIONS ABOUT GETTING HELPED----------------------
  await query.message.edit_text(text=texts.GET_HELP)
  await Form.help.set()
  #-------------------------------------------------------------------------
  
  #state.update_data(help=False)
  #state.reset_state(with_data=False)
  

@dp.message_handler(state=Form.help, content_types=types.ContentTypes.TEXT)
async def help_message(message: types.Message, state: FSMContext):
    #-------------------------------------------------------------------------
    #---------------------FORWARDING HELP------------------------------------
  #   requests.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
  # "chat_id": "-776565232",
  # "text": texts.HELP_MESSAGE % (data['user_id'], data['name'], message.text, data['user_id'])
  # })
    await state.reset_state(with_data=False)
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    data['help']=False
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ***********************TELEGRAM CONTACTS**********************************************************************************************************************************************************
@dp.callback_query_handler(text='our_telegram', state=Form.no_match)
async def send_telegram_url(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  if not data['has_match']:
    await Form.no_match.set()
  else:
    await Form.has_match.set()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  subscribe_button = types.InlineKeyboardButton(text=buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='user_pressed_tg')
  keyboard.add(subscribe_button)
  await query.message.edit_text(text=texts.OUR_TG, reply_markup=keyboard)
  

@dp.callback_query_handler(text='user_pressed_tg')
async def request_when_tg_pressed(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  #-------------------------------------------------------------------------
  #-------------POST request for some STATISTICS-----------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_our_telegram_subscribe_btn"
    }
  ]
})
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------PAUSE MATCHING--------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='paused_main_menu', state=Form.no_match)
async def pause_menu(query: types.CallbackQuery,state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  #await state.update_data(matching_pause=True)
  data['matching_pause'] = True
  #-------------------------------------------------------------------------
  #---------------------POST request for STATISTIC--------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi',json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_menu_pause_btn"
#     }
#   ]
# })
  #-------------------------------------------------------------------------
  #---------------------POST request to END finding match-------------------
  requests.post(url='https://server.unison.dating/user/pause?user_id=%s' % data['user_id'], json={"pause": "true"})
  #-------------------------------------------------------------------------
  #-------------------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  if not data['has_match']:
    await Form.no_match.set()
  else:
    await Form.has_match.set()
  await query.message.edit_text(text=texts.PAUSE_MAIN_MENU, reply_markup= keyboard)
  
@dp.callback_query_handler(text='unpaused_main_menu', state=Form.no_match)
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    await state.reset_state(with_data=False)
    #await state.update_data(matching_pause=False)
    data['matching_pause'] = False
    #-------------------------------------------------------------------------
    #---------------------POST request for STATISTIC--------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_menu_resume_btn"
#     }
#   ]
# })
    #-------------------------------------------------------------------------
    #---------------------POST request to UNPAUSE finding---------------------
    # requests.post(url='https://server.unison.dating/user/pause?user_id=%s' % data['user_id'], json={"pause": "false"})
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    #--------------------set all data about match person zero----------------
    #await state.update_data(match_id=0)
    data_match['user_id'] = 0
    #await state.update_data(tag_begin_comunication=False)
    data['tag_begin_comunication'] = False
    #------------------------------------------------------------------------
    if not data['has_match']:
      await Form.no_match.set()
    else:
      await Form.has_match.set()
    await query.message.edit_text(text=texts.MAIN_MENU, reply_markup=keyboard)


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ************************************MATCHING MENU*************************************************************************************************************************************************
@dp.message_handler(commands = 'start_has_match', state=Form.has_match)
async def start_communicating(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(tag_begin_comunocation = True)
  data['tag_begin_comunication'] = True
  #await state.update_data(has_match = 0)
  data['has_match'] = True
  #await state.update_data(tag_first_time = False)
  data['tag_first_time'] = True
  await bot.send_message(data['user_id'], text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  
  #--------------------------------------------------------------------------------------
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(data['user_id'], photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET) #, callback_data='wanna_meet')
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO) #, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST) #, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG) #, callback_data='end_dialog')
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  with open(data['match_photo'], 'rb') as profile_pic:
    await bot.send_photo(data['user_id'], photo=profile_pic, caption=texts.MATCH_INFO % (data_match['name'], data_match['city'], data_match['reason']))
  await bot.send_message(data['user_id'], text=texts.FIND_MATCH, reply_markup= keyboard)

# FORWARDING MESSAGES TO MATCH PERSON
@dp.message_handler(state=Form.has_match, content_types=types.ContentTypes.TEXT)
async def forwarding_messages(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  if message.text == buttons_texts.WANNA_MEET:
    #await state.reset_state(with_data=False)
    #data = await state.get_data()
    # -------------------------------------------------------
    # -----POST request for UNISON THAT USER WANNA MEET------
#     requests.post(url='https://server.unison.dating/user/wanna_meet?user_id=%s'%data['user_id'], json={
#   "match_id": data_match['user_id']
# })
    # -------------------------------------------------------
    # -------------POST request for some STATISTICS----------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "bot_meeting_ask"
#    }
#   ]
# })
    # -------------------------------------------------------
    await bot.send_message(data['user_id'], text=texts.WANNA_MEET)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_meeting')
    deny_button = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='are_u_deny_meeting')
    keyboard.row(confirm_button, deny_button)
    await Form.has_match.set()
    #sending message to match person
    await bot.send_message(await get_match_id(message), text=texts.COFIRM_MEET % data['name'], reply_markup=keyboard)
  # SENDING PHOTO   
  elif message.text == buttons_texts.SEND_PHOTO:
    await state.reset_state(with_data=False)
    await bot.send_message(data['user_id'],text=texts.UPLOAD_PHOTO_TO_MATCH)
    await state.reset_state(with_data=False)
    await Form.upload_photo_to_match.set()
  elif message.text == buttons_texts.END_DIALOG:
    await state.reset_state(with_data=False)
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to some STATISTIC--------------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
# "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
# "events":[{
# "user_id": data['user_id'],
# "event_type": "bot_chating_end_btn"
# }]
# })
    #--------------------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
    comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
    ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
    other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
    keyboard.add(look_button, comunication_button)
    keyboard.add(ignore_button, other_button)
    await bot.send_message(data['user_id'], text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)
    await Form.has_match.set()
  elif message.text == buttons_texts.SEND_REQUEST:
    #data = await state.get_data()
    await bot.send_message(data['user_id'], text=texts.COMUNICATION_HELP)
    await state.reset_state(with_data=False)
    await Form.get_help_message.set()
  else:
      await bot.send_message(data_match['user_id'], text = message.text)

# IF U RECIVE MEETING MESSAGE AND AGREE TO IT
@dp.callback_query_handler(text='confirm_meeting', state=Form.has_match)
async def congirm_meeting_message(message: types.Message, state: FSMContext):
  #state.update_data(match_wanna_meet = True)
  await state.reset_state(with_data=False)
  data['match_wanna_meet'] = True
  #data = await state.get_data()
  # --------POST request for STATISTICS ----------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_meeting_approve"
#     }
#   ]
# })
  # ----------------------------------------------------------------
  # --------POST request for STATISTICS ----------------------------
  # requests.post(url='https://server.unison.dating/user/meet_confirm?user_id=%s' % data['user_id'], json={ "match_id": data_match["user_id"] })
  # ----------------------------------------------------------------
  await bot.send_message(await get_match_id(message), text=texts.MATCH_AGREE % data_match['name'])
  #await asyncio.sleep(3600)
  #await asyncio.sleep(60)
  #game = random.randint(1, 12)
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
  if data['city'] == texts.SAINT_PETERSBURG:
    #await state.reset_state(with_data=False)
    #data = await state.get_data()
    await bot.send_message(data['user_id'], text=texts.GREETING_MENU_SPB_PLACE % data_match['name'])
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
    mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
    jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
    keyboard.add(smena_menu_button)
    keyboard.add(mickey_monkeys_button)
    keyboard.add(jack_chan_button)
    await bot.send_message(data['user_id'], text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
    #await Form.spb_meeting.set()
  elif data['match_city'] == texts.MOSCOW_HELLO:
    await bot.send_message(data['user_id'], text=texts.MOSCOW_HELLO% data_match['name'])
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
    propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
    she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
    keyboard.add(double_b)
    keyboard.add(propoganda)
    keyboard.add(she)
    await bot.send_message(data['user_id'], text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
    #await Form.msc_meeting.set()

@dp.callback_query_handler(text='spb_menu')
async def spb_menu(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
  mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
  jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
  keyboard.add(smena_menu_button)
  keyboard.add(mickey_monkeys_button)
  keyboard.add(jack_chan_button)
  await query.message.edit_text(text=texts.MENU_SPB_PLACE)
  await query.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(text='are_u_deny_meeting', state=Form.has_match)
async def are_u_deny_meeting(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  yes = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='deny_meeting')
  no = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='confirm_meeting')
  keyboard.row(yes, no)
  await query.message.edit_text(text=texts.ARE_U_SURE_END)
  await query.message.edit_reply_markup(reply_markup=keyboard)
  await Form.has_match.set()

@dp.callback_query_handler(text='deny_meeting')
async def deny_meeting(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  #----------------------------------------------------------------------------------
  #---------------POST request to STOP MATCHING on SERVER----------------------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
#   "reason": "no interest"
# })
  #----------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC--------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_reject"
#    }
#   ]
# })
  #--------------------------------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
  comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
  ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
  other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
  keyboard.add(look_button, comunication_button)
  keyboard.add(ignore_button, other_button)
  await bot.send_message(data['user_id'], text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)
  await Form.has_match.set()

# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------ENDING COMUNICATION------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(state=Form.has_match, text='dont_like_look')
async def dont_like_look(query: types.CallbackQuery, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "bot_chating_self_end_reason_ugly"
#    }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data_match["user_id"],
#      "event_type": "bot_chating_partner_end_reason_ugly"
#    }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #data = await state.update_data(reason_to_stop='Не понравился внешне')
  data['reason_to_stop'] = 'Не понравился внешне'
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(data_match['user_id'], text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.callback_query_handler(text='confirm_leaving', state=Form.has_match)
async def delete_match_info(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(match_id = 0)
  data['match_id'] = 0
  #await state.update_data(has_match = False)
  data['has_match'] = False
  await Form.no_match.set()
  await state.reset_state(with_data=False)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not data['matching_pause']:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
  if not data['matching_pause']:
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  if not data['has_match']:
    await Form.no_match.set()
  else:
    await Form.has_match.set()

@dp.message_handler(state=Form.has_match, text='ignore')
async def show_ignore(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_chating_self_end_reason_noreply"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_self_end_reason_noreply"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #data = await state.update_data(reason_to_stop='собеседник не отвечает')
  data['reason_stop'] = 'собеседник не отвечает'
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  #requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(data_match['user_id'], text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.message_handler(state=Form.has_match, text='dont_like_comunication')
async def dont_like_comunication(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_chating_partner_end_reason_stupid"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_partner_end_reason_stupid"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #await state.update_data(reason_to_stop="не понравилось общение")
  data['reason_to_stop'] = "не понравилось общение"
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  #requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(data_match['user_id'], text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.message_handler(state=Form.has_match, text='dont_like_other')
async def dont_like_other(query: types.CallbackQuery, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_chating_self_end_reason_else"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_partner_end_reason_else"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  await state.reset_state(with_data=False)
  await Form.why_dont_like.set()
@dp.message_handler(state=Form.why_dont_like, content_types=types.ContentTypes.TEXT)
async def set_reason(message: types.Message, state: FSMContext):
  #data = await state.update_data(reason_to_stop=message.text)
  data['reason_to_stop']=message.text
  await state.reset_state(with_data=False)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard.add(confirm_leaving_button)
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data_match['user_id'],
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(data_match['user_id'], text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# **********************************FORWARDIN PHOTO TO MATCH****************************************************************************************************************************************
@dp.message_handler(state=Form.upload_photo_to_match, content_types=types.ContentType.PHOTO)
async def upload_photo_to_match(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  photo_id = message.photo[-1].file_id
  #-----------------------------------------------------------------
  #----------------POST request for some statistics-----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_send_photo_to_user"
#     }
#   ]
# })
  #-----------------------------------------------------------------
  # WE FORWARDING PHOTO SO IT CAN BE DONE WITH ID OF IMAGE
  await state.reset_state(with_data=False) 
  await Form.has_match.set()
  await bot.send_photo(data_match['user_id'], photo=photo_id)
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------REQUEST HELP WITH COMUNICATION--------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(state=Form.get_help_message, content_types=types.ContentTypes.TEXT)
async def get_comunication_help_message(message: types.Message, state: FSMContext):
  help_message = message.text
  await state.reset_state(with_data=False)
#   requests.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
#   "chat_id": "-776565232",
#   "text": "Пользователь отправил жалобу во время общения: \n UserID: %s; \n Имя: %s; \n Текст жалобы: \n %s\nПользователь:\n %s" % (data['user_id'], data['name'], help_message, data['user_id'])
# })
  #----------------------------------------------------------------------------------
  #---------------------POST request for some STATISTIC------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "bot_chating_send_petition"
#    }
#   ]
# })
  #----------------------------------------------------------------------------------
  await Form.has_match.set()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------TIME TO END COMUNICATING----------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='callback_look',state=Form.ending_match)
async def dont_like_look(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "reason_stop_don't_like"
#     }
#   ]
# })
  # ----------------------------------------------------------------
  #await state.update_data(reason_to_stop='не понравился внешне')
  data['reason_to_stop'] = 'не понравился внешне'
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(data['user_id'], text=texts.CALLBACK_MEETING % data['match_name'], reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='callback_comunication',state=Form.ending_match)
async def dont_like_comunication(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "reason_stop_don't_like_messaging"
#     }
#   ]
# })
  # ----------------------------------------------------------------
  #await state.update_data(reason_to_stop='не понравилось общение')
  data['reason_to_stop'] = 'не понравилось общение'
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(data['user_id'], text=texts.CALLBACK_MEETING % data['match_name'], reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='callback_like',state=Form.ending_match)
async def everything_ok(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "reason_stop_like_but_time_gone"
#    }
#   ]
# })
  # ----------------------------------------------------------------
  #await state.update_data(reason_to_stop='Понравился, но время общения истекло')
  data['reason_to_stop']='Понравился, но время общения истекло'
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(data['user_id'], text=texts.CALLBACK_MEETING % data['match_name'], reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='callback_other',state=Form.ending_match)
async def callback_other(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "reason_stop_other"
#    }
#   ]
# })
  # ----------------------------------------------------------------
  await state.reset_state(with_data=False)
  await bot.send_message(data['user_id'], text=texts.CALLBACK_REASON)
  await Form.callback_other.set()
@dp.message_handler(state=Form.callback_other, content_types= types.ContentTypes.TEXT)
async def set_message_other(message: types.Message, state: FSMContext):
  #await state.update_data(reason_to_stop = message.text)
  data['reason_to_stop'] = message.text
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  ok_meeting_button = types.InlineKeyboardButton(text=buttons_texts.OK_MEET, callback_data='ok_meeting')
  unlike_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NOT_OK_MEET, callback_data='unlike_meeting')
  keyboard.add(ok_meeting_button)
  keyboard.add(unlike_meeting_button)
  await bot.send_message(data['user_id'], text=texts.CALLBACK_MEETING % data['match_name'], reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='unlike_meeting',state=Form.ending_match)
async def set_was_meeting_no(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(was_meeting='Встреча не состоялась')
  data['was_meeting']='Встреча не состоялась'
  await state.reset_state(with_data=False)
  #------------------------------------------------------------------
  #-----------------POST requset for some STATISTICS-----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "meeting_not_happens"
#    }
#   ]
# })
  #------------------------------------------------------------------
  #data = await state.get_data()
  await query.message.edit_text(text=texts.REASON_MEETING)
  await Form.unlike_meeting.set()
@dp.message_handler(state=Form.unlike_meeting, content_types= types.ContentTypes.TEXT)
async def set_meeting_reaction(message: types.Message, state: FSMContext):
  #await state.update_data(meeting_reaction = message.text)
  data['meeting_reaction'] = message.text
  state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(data['user_id'], text=texts.ABOUT_MEETING, reply_markup=keyboard)
  await Form.ending_match.set()


@dp.callback_query_handler(text='ok_meeting',state=Form.ending_match)
async def set_was_meeting_yes(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(was_meeting='Встреча состоялась')
  data['was_meeting'] = 'Встреча состоялась'
  await state.reset_state(with_data=False)
  #------------------------------------------------------------------
  #-----------------POST requset for some STATISTICS-----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "meeting_happens"
#    }
#   ]
# })
  #------------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  like_meeting_button = types.InlineKeyboardButton(text=buttons_texts.LIKE_MEETING, callback_data='all_like')
  neutral_meeting_button = types.InlineKeyboardButton(text=buttons_texts.NEUTRAL_MEETING, callback_data='neutral_meeting')
  dont_like_button = types.InlineKeyboardButton(text=buttons_texts.DONT_LIKE_MEETING, callback_data='dont_like_meeting')
  keyboard.add(like_meeting_button)
  keyboard.add(neutral_meeting_button)
  keyboard.add(dont_like_button)
  await query.message.edit_text(text=texts.LIKE_ABOT_MEETING, reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='all_like',state=Form.ending_match)
async def set_meeting_reaction_ok(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(meeting_reaction='Встреча понравилась')
  data['meeting_reaction'] = 'Встреча понравилась'
  await query.message.edit_text(text=texts.END_CALLBACK)
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if data['subscribtion']:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(data['user_id'], text=texts.END_DIALOG % data['match_name'], reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not data['matching_pause']:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  await Form.no_match.set()
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
  if not data['matching_pause']:
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  #await state.update_data(match_id = 0)
  data['match_id'] = 0
  #await state.update_data(reason_to_stop = 'time_gone')
  data['reason_to_stop'] = 'time_gone'
  


@dp.callback_query_handler(text='neutral_meeting',state=Form.ending_match)
async def set_meeting_reaction_neutral(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(meeting_reaction = 'Ничего особенного')
  data['meeting_reaction'] = 'Ничего особенного'
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(data['user_id'], text=texts.ABOUT_MEETING, reply_markup=keyboard)
  await Form.ending_match.set()

@dp.callback_query_handler(text='dont_like_meeting',state=Form.ending_match)
async def set_meeting_reaction_negative(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(meeting_reaction = 'Не понравилась')
  data['meeting_reaction'] = 'Не понравилась'
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  dont_like_look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='meeting_look')
  dont_like_behavior_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_BEHAVIOR, callback_data='meeting_behavior')
  dont_like_place_button = types.InlineKeyboardButton(text=buttons_texts.MEETING_PLACE, callback_data='meeting_place')
  keyboard.add(dont_like_look_button)
  keyboard.add(dont_like_behavior_button)
  keyboard.add(dont_like_place_button)
  await bot.send_message(data['user_id'], text=texts.ABOUT_MEETING, reply_markup=keyboard)
  await Form.ending_match.set()
  

@dp.callback_query_handler(text='meeting_look',state=Form.ending_match)
async def set_why_meeting_bad_look(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(why_meeting_bad='Не понравился внешне')
  #data = await state.get_data()
  data['why_meeting_bad']='Не понравился внешне'
  await state.reset_state(with_data=False)
  # --------------POST request to END MATCHING--------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
#   "reason": "Время истекло и %s" % data['reason_to_stop'],
#   "was_meeting": data["was_meeting"],
#   "meeting_reaction": data["meeting_reaction"],
#   "why_meeting_bad": data["why_meeting_bad"]
# })
  # --------------------------------------------------------
  await query.message.edit_text(text=texts.END_CALLBACK)
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if data['subscribtion']:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(data['user_id'], text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not data['matching_pause']:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
  if not data['matching_pause']:
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  #await state.update_data(match_id = 0)
  data['match_id'] = 0
  #await state.update_data(reason_to_stop = 'time_gone')
  data['reason_to_stop'] = 'time_gone'
  await Form.no_match.set()

@dp.callback_query_handler(text='meeting_behavior',state=Form.ending_match)
async def set_why_meeting_bad_behavior(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(why_meeting_bad='Не понравился внешне')
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  data['why_meeting_bad'] = 'Не понравился внешне'
  # --------------POST request to END MATCHING--------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
#   "reason": "Время истекло и %s" % data['reason_to_stop'],
#   "was_meeting": data["was_meeting"],
#   "meeting_reaction": data["meeting_reaction"],
#   "why_meeting_bad": data["why_meeting_bad"]
# })
  # --------------------------------------------------------
  await query.message.edit_text(text=texts.END_CALLBACK)
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if data['subscribtion']:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(data['user_id'], text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not data['matching_pause']:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
  if not data['matching_pause']:
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  #await state.update_data(match_id = 0)
  data['match_id'] = 0
  #await state.update_data(reason_to_stop = 'time_gone')
  data['reason_to_stop'] = 'time_gone'
  await Form.no_match.set()

@dp.callback_query_handler(text='meeting_place',state=Form.ending_match)
async def set_why_meeting_bad_place(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(why_meeting_bad='Не понравился внешне')
  data['why_meeting_bad'] = 'Не понравился внешне'
  await state.reset_state(with_data=False)
  #data = await state.get_data()
  # --------------POST request to END MATCHING--------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
#   "reason": "Время истекло и %s" % data['reason_to_stop'],
#   "was_meeting": data["was_meeting"],
#   "meeting_reaction": data["meeting_reaction"],
#   "why_meeting_bad": data["why_meeting_bad"]
# })
  # --------------------------------------------------------
  await query.message.edit_text(text=texts.END_CALLBACK)
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if data['subscribtion']:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  keyboard.add(subscribes_button)
  await bot.send_message(data['user_id'], text=texts.END_DIALOG, reply_markup=keyboard)
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  if not data['matching_pause']:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
  else:
    pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
  if not data['matching_pause']:
    await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  else:
    await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
  #await state.update_data(match_id = 0)
  data['match_id'] = 0
  #await state.update_data(reason_to_stop = 'time_gone')
  data['reason_to_stop'] = 'time_gone'
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.stop_match)
async def stoping_match(message: types.Message, state: FSMContext):
    #data = await state.get_data()
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    keyboard.add(subscribes_button)
    await bot.send_message(data['user_id'], text=texts.END_DIALOG, reply_markup=keyboard)
    inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    if not data['matching_pause']:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    else:
      pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
    inline_keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
    reply_keyboard.add(main_menu)
    with open('./pic/main_photo.png', 'rb') as img_file:
      await bot.send_photo(chat_id=data['user_id'], photo=img_file ,reply_markup=reply_keyboard)
    if not data['matching_pause']:
      await bot.send_message(chat_id=data['user_id'], text=texts.MAIN_MENU, reply_markup=inline_keyboard)
    else:
      await bot.send_message(chat_id=data['user_id'], text=texts.PAUSE_MAIN_MENU, reply_markup=inline_keyboard)
    #await state.update_data(match_id = 0)
    data['match_id'] = 0
    #await state.update_data(reason_to_stop = 'time_gone')
    data['reason_to_stop'] = 'time_gone'
    await Form.no_match.set()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#***************************************************************************************************************************************************************************************************
#***************************************************************************MEETING PLACE***********************************************************************************************************

# ____________SPB_______________________
@dp.callback_query_handler(text='smena')
async def show_smena(message: types.Message, state:FSMContext):
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_smena')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.SMENA_COFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_smena')
async def choose_smena(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.SMENA_MEET_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": data['user_id'],
#      "event_type": "bot_meeting_place_smena"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()

@dp.callback_query_handler(text='mickey')
async def show_mickey(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_mickey')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.MICKEY_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_mickey')
async def choose_mickey(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.MICKEY_MEET_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_place_mickey_monkey"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()

@dp.callback_query_handler(text='jack_and_chan')
async def show_jack(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_jack')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.JACK_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_jack')
async def choose_jack(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state()
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.JACK_MEET_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_place_lack_chan"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()

# ____________MSC_______________________
@dp.callback_query_handler(text='msc_menu')
async def msc_menu(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  #await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
  propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
  she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
  keyboard.add(double_b)
  keyboard.add(propoganda)
  keyboard.add(she)
  await bot.send_message(data['user_id'], text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='double_b')
async def doube_b(messaage: types.Message, state: FSMContext):
  #await state.reset_state(with_data=False)
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_double_b')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.DOUBLE_B_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_double_b')
async def choose_double_b(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.DOUBLE_B_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_place_dabl_be"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()

@dp.callback_query_handler(text='propoganda')
async def propoganda(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_propoganda')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.PROPOGANDA_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_propoganda')
async def choose_propoganda(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.PROPOGANDA_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_place_propoganda"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()

@dp.callback_query_handler(text='she')
async def she(message: types.Message, state: FSMContext):
  #await state.reset_state(with_data=False)
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_she')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(data['user_id'], text=texts.SHE_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_she')
async def choose_she(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  await bot.send_message(data['user_id'], text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(data_match['user_id'], text=texts.SHE_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": "userId",
#      "event_type": "bot_meeting_place_she"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()

#***************************************************************************************************************************************************************************************************
#***************************************************************************************************************************************************************************************************

#===================================================================================================================================================================================================
#===============================================================    PAYMENTS STATUS    =============================================================================================================

@dp.callback_query_handler(state=Form.payment_renew_fail)
async def payment_renew_fail(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  if data['subscribtion']:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='have_subscribtion')
  else:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(data['user_id'], text=texts.PAYMENT_RENEWAL_FAIL, reply_markup=keyboard)
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_renew_success)
async def payment_renew_success(message: types.Message, state: FSMContext):
  #data = await state.get_data()
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_payment_renew_success"
#     }
#   ]
# })
  await bot.send_message(data['user_id'], text=texts.PAYMENT_RENEWAL_SUC)
  if data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ok)
async def payment_ok(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
  # requests.post(url='https://server.unison.dating/user/payment?user_id=%s' % data['user_id'], json={"status_payment": "pass"})
  # ----------------------------------------------------
  await bot.send_message(data['user_id'], text=texts.PAYMENT_NEW_SUC)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_subscribe_pay_success"
#     }
#   ]
# })
  # ----------------------------------------------------
  # ---------SENDING INFO to MODERATION CHAT------------
#   requests.post(url='', json={
# "chat_id":"-776565232",
# "text": "Пользователь оплатил подписку \n UserID: #id%s; \n Имя: %s " % (data['user_id'], data['user_name'])

# })
  # ----------------------------------------------------
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ends)
async def payment_ends(message: types.Message, state: FSMContext):
  #await state.update_data(subscribtion = False)
  data['subscribtion'] = False
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  # ----------------------------------------------------------------
  # ----------------POST request for some STATISTICS----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
# "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
# "events":[{
# "user_id": data['user_id'],
# "event_type": "bot_subscribe_pay_ended"
# }]
# })
  # ----------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if data['subscribtion']:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='have_subscribtion')
  else:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(data['user_id'], text=texts.PAYMENT_ENDS, reply_markup=keyboard)
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_fail)
async def payment_fail(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  #data = await state.get_data()
  # ---------------------------------------------------------------
  # ---------------POST request for some STATISTICS----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": data['user_id'],
#       "event_type": "bot_subscribe_pay_reject"
#     }
#   ]
# })
  # ---------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  again = types.InlineKeyboardButton(text=buttons_texts.TRY_AGAIN, callback_data='doesnt_have_subscribtions')
  keyboard.add(again)
  bot.send_message(data['user_id'], text=texts.PAYMENT_FAIL, reply_markup=keyboard)
  await Form.no_match.set()

#===================================================================================================================================================================================================
#===================================================================================================================================================================================================

async def get_advice(state: FSMContext):
  #data = state.get_data
  random.shuffle(data['first_day_hints'])
  random.shuffle(data['hints'])
  if data['first_day_hints']:
    if data['has_match']:
      await bot.send_message(data['user_id'], text=data['first_day_hints'].pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(state, ))
  elif data['hints']:
    if data['has_match']:
      await bot.send_message(data['user_id'], text=data['hints'].pop(0))
      scheduler.add_job(get_advice, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=15), args=(state, ))
  

async def payments_scheduler(state: FSMContext):
  #data = await state.get_data()
  if data['subscribtion']:
    
    pass
  else:

    pass
  pass

async def on_startup():
  schedule_jobs()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)