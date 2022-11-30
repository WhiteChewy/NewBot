import logging
import datetime
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import base64
import random
import db_interface as db
import asyncpg

from aiogram.dispatcher.filters import Filter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, DB_PASSWORD, DB_USER


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN) 
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
conn = None

# STATES FOR STATE MACHINE
class Form(StatesGroup):
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


#ASK server if has match or not
async def is_match(id: int):
  # GET INFO ABOUT MATCH IF THERE IT MATCH RETURN TRUE
  # CHECK SERVER IF THERE IS MATCHES
  #
  #---------------------------------
  return await db.is_matching(id, conn)

# CHECK USER ABOUT SUBSCRIBE
async def is_premium(id: int):
  #data = await state.get_data()
  return await db.is_subscribed(id, conn)

# CHECK IF TODAY MONDAY
async def is_monday():
  if not datetime.date.today().weekday():
    return True
  else:
    return False

# SET STATE UNMATCHED
async def set_state_unmatch(id: int, state: FSMContext):
  #await state.reset_state(with_data=False)
  #await state.update_data(has_match = False)
  await db.set_match_status(id, conn, False)
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
  await bot.send_message(id, text=texts.CALLBACK, reply_markup=keyboard)
  

# SET STATE ONE_DAY_TO_UNMATCH
async def set_state_one_day_to_unmatch(id: int, state: FSMContext):
  #data = await state.get
  await state.reset_state(with_data=False)
  #scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.date.today()+datetime.timedelta(days=1), args=(state,))
  scheduler.add_job(set_state_unmatch, 'date', run_date=datetime.datetime.now()+datetime.timedelta(minutes=1), args=(id, state,))
  await Form.has_match.set()
  await bot.send_message(id, text=texts.ONE_DAY_TO_UNMATCH % await db.get_name(await db.get_match_id(id, conn), conn))
  

# SET STATE TO HAS_MATCH
async def set_state_has_match(id: int, state: FSMContext):
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
  with open('./pic/find_match.png', 'rb') as img:
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
  date_today = datetime.date.today()
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
      #data = await state.get_data()
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
      with open('./pic/main_photo.png', 'rb') as img_file:
        await bot.send_photo(id, photo=img_file)
      if not await db.is_matching(id, conn):
        await Form.no_match.set()
      else:
        await Form.has_match.set()
      if not await db.is_paused(id, conn):
        await bot.send_message(id, text=texts.MAIN_MENU, reply_markup=keyboard)
      else:
        await bot.send_message(id, text=texts.PAUSE_MAIN_MENU, reply_markup=keyboard)


@dp.callback_query_handler(text='main_menu')
async def messaging_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if await db.is_subscribed(message.from_user.id, conn):
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
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


# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# **************************************************************************************************************************************************************************************************
# ************************************MATCHING MENU*************************************************************************************************************************************************
@dp.message_handler(commands = 'start_has_match')
async def start_communicating(message: types.Message, state: FSMContext):
  await db.set_first_time_status(message.from_user.id, conn, True)
  await bot.send_message(message.from_user.id, text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  
  #--------------------------------------------------------------------------------------
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(message.from_user.id, photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET) #, callback_data='wanna_meet')
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO) #, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST) #, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG) #, callback_data='end_dialog')
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  #data['match_photo']
  with open(await db.get_profile_photo(await db.get_match_id(id, conn), conn), 'rb') as profile_pic:
    await bot.send_photo(message.from_user.id, photo=profile_pic, caption=texts.MATCH_INFO % (await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), await db.get_city(await db.get_match_id(message.from_user.id, conn), conn), await db.get_reason(await db.get_match_id(message.from_user.id, conn), conn)))
  await bot.send_message(message.from_user.id, text=texts.FIND_MATCH, reply_markup= keyboard)

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
#   "match_id": await db.get_match_id(message.from_user.id, conn)
# })
    # -------------------------------------------------------
    # -------------POST request for some STATISTICS----------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_ask"
#    }
#   ]
# })
    # -------------------------------------------------------
    await bot.send_message(message.from_user.id, text=texts.WANNA_MEET)
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    confirm_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_meeting')
    deny_button = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='are_u_deny_meeting')
    keyboard.row(confirm_button, deny_button)
    await Form.has_match.set()
    #sending message to match person
    await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.COFIRM_MEET % await db.get_name(message.from_user.id, conn), reply_markup=keyboard)
  # SENDING PHOTO   
  elif message.text == buttons_texts.SEND_PHOTO:
    await state.reset_state(with_data=False)
    await bot.send_message(message.from_user.id ,text=texts.UPLOAD_PHOTO_TO_MATCH)
    await state.reset_state(with_data=False)
    await Form.upload_photo_to_match.set()
  elif message.text == buttons_texts.END_DIALOG:
    await state.reset_state(with_data=False)
    #--------------------------------------------------------------------------------------
    #--------------POST reuqest to some STATISTIC--------------------------------------
#     requests.post(url='https://api.amplitude.com/2/httpapi', json={
# "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
# "events":[{
# "user_id": message.from_user.id,
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
    await bot.send_message(message.from_user.id, text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)
  elif message.text == buttons_texts.SEND_REQUEST:
    #data = await state.get_data()
    await bot.send_message(message.from_user.id, text=texts.COMUNICATION_HELP)
    await state.reset_state(with_data=False)
    await Form.get_help_message.set()
  else:
      await bot.send_message(await db.get_match_id(message.from_user.id, conn), text = message.text)

# IF U RECIVE MEETING MESSAGE AND AGREE TO IT
@dp.callback_query_handler(text='confirm_meeting', state=Form.has_match)
async def congirm_meeting_message(message: types.Message, state: FSMContext):
  #state.update_data(match_wanna_meet = True)
  await state.reset_state(with_data=False)
  await db.set_meeting_status(message.from_user.id, conn, True)
  #data = await state.get_data()
  # --------POST request for STATISTICS ----------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "bot_meeting_approve"
#     }
#   ]
# })
  # ----------------------------------------------------------------
  # --------POST request for STATISTICS ----------------------------
  # requests.post(url='https://server.unison.dating/user/meet_confirm?user_id=%s' % message.from_user.id, json={ "match_id": await db.get_match_id(message.from_user.id, conn) })
  # ----------------------------------------------------------------
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.MATCH_AGREE % await db.get_name(message.from_user.id, conn))
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
  if await db.get_city(message.from_user.id, conn) == texts.SAINT_PETERSBURG:
    #await state.reset_state(with_data=False)
    #data = await state.get_data()
    await bot.send_message(message.from_user.id, text=texts.GREETING_MENU_SPB_PLACE % await db.get_city(await db.get_match_id(message.from_user.id, conn), conn))
    keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
    smena_menu_button = types.InlineKeyboardButton(text=buttons_texts.SMENA_BUTTON, callback_data='smena')
    mickey_monkeys_button = types.InlineKeyboardButton(text=buttons_texts.MICKEY_MONKEY_BUTTON, callback_data='mickey')
    jack_chan_button = types.InlineKeyboardButton(text=buttons_texts.JACK_AND_CHAN_BUTTON, callback_data='jack_and_chan')
    keyboard.add(smena_menu_button)
    keyboard.add(mickey_monkeys_button)
    keyboard.add(jack_chan_button)
    await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
    #await Form.spb_meeting.set()
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
  await Form.has_match.set()

@dp.callback_query_handler(text='deny_meeting')
async def deny_meeting(message: types.Message, state: FSMContext):
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
  await bot.send_message(message.from_user.id, text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)

# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------ENDING COMUNICATION------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='dont_like_look')
async def dont_like_look(message: types.Message, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
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
#      "user_id": await db.get_match_id(message.from_user.id, conn),
#      "event_type": "bot_chating_partner_end_reason_ugly"
#    }
#   ]
# })
  #--------------------------------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'Не понравился внешне')
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # requests.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  keyboard = types.InlineKeyboardMarkup(resize_keyboadr=True)
  yes = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  no = types.InlineKeyboardButton(text=buttons_texts.NO, callback_data='deny_leaving')
  keyboard.add(yes, no)
  await bot.send_message(message.from_user.id, text=texts.CONFIRMING_LEAVING_CHAT, reply_markup=keyboard)

@dp.callback_query_handler(text='deny_leaving')
async def deny_leavint(message: types.Message, state: FSMContext):
  await Form.has_match.set()
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(message.from_user.id, photo=img)
  keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.KeyboardButton(text=buttons_texts.WANNA_MEET) #, callback_data='wanna_meet')
  send_photo_button = types.KeyboardButton(text=buttons_texts.SEND_PHOTO) #, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST) #, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG) #, callback_data='end_dialog')
  keyboard.row(wanna_meet_button, send_photo_button)
  keyboard.row(send_request, end_dialog)
  with open(await db.get_profile_photo(await db.get_match_id(message.from_user.id, conn), conn), 'rb') as profile_pic:
    await bot.send_photo(message.from_user.id, photo=profile_pic, caption=texts.MATCH_INFO % (await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), await db.get_city(await db.get_match_id(message.from_user.id, conn), conn), await db.get_reason(await db.get_match_id(message.from_user.id, conn), conn)))
  await bot.send_message(message.from_user.id, text=texts.FIND_MATCH, reply_markup= keyboard)

@dp.callback_query_handler(text='confirm_leaving')
async def delete_match_info(message: types.Message, state: FSMContext):
  await state.reset_state()
  keyboard1 = types.InlineKeyboardMarkup(resize_keyboard = True)
  confirm_leaving_button = types.InlineKeyboardButton(text=buttons_texts.YES, callback_data='confirm_leaving')
  keyboard1.add(confirm_leaving_button)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard1)
  # ACTIVATE ON CLIENT SIDE ---------------------------------------------------------------------------------------
  inline_keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user, conn):
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
  # ACTIVATE ON MATCH SIDE ----------------------------------------------------------------------------------------
  inline_keyboard2 = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(await db.get_match_id(message.from_user, conn), conn):
      subscribes_button = types.KeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
  else:
      subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
  write_help = types.InlineKeyboardButton(text=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  inline_keyboard2.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  reply_keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
  main_menu = types.KeyboardButton(text=buttons_texts.MAIN_MENU)
  reply_keyboard2.add(main_menu)
  with open('./pic/main_photo.png', 'rb') as img_file:
    await bot.send_photo(await db.get_match_id(message.from_user, conn), photo=img_file ,reply_markup=reply_keyboard2)
  # --------------------------------------------------------------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.MAIN_MENU, reply_markup=inline_keyboard)
  await bot.send_message(await db.get_match_id(message.from_user, conn), text=texts.MAIN_MENU, reply_markup=inline_keyboard2)
  
  await db.set_match_id_manualy(await db.get_match_id(message.from_user.id, conn), conn, 0)
  await db.set_match_id_manualy(message.from_user.id, conn, 0)
  
  await db.set_match_status(message.from_user.id, conn, False)
  await db.set_match_status(await db.get_match_id(message.from_user, conn), conn, False)

@dp.message_handler(text='ignore')
async def show_ignore(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_self_end_reason_noreply"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, 'собеседник не отвечает')
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  #requests.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={"reason": await db.get_reason_to_stop(message.from_user.id, conn)})
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.message_handler(text='dont_like_comunication')
async def dont_like_comunication(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_partner_end_reason_stupid"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  await db.set_reason_to_stop(message.from_user.id, conn, "не понравилось общение")
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(message.from_user.id, text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

@dp.message_handler(text='dont_like_other')
async def dont_like_other(message: types.Message, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_partner_end_reason_else"
#     }
#   ]
# })
  #--------------------------------------------------------------------------------------
  await state.reset_state(with_data=False)
  await Form.why_dont_like.set()
@dp.message_handler(state=Form.why_dont_like, content_types=types.ContentTypes.TEXT)
async def set_reason(message: types.Message, state: FSMContext):
  await db.set_reason_to_stop(message.from_user.id, conn, message.text)
  await state.reset_state(with_data=False)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  # requests.post(url='https://server.unison.dating/user/stop_match?%s' % message.from_user.id, json={"reason": await db.get_reason_to_stop(message.from_user.id, conn)})
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
#       "user_id": await db.get_match_id(message.from_user.id, conn),
#       "event_type": "bot_chating_ended_partner_choosing"
#     }
#   ]
# })
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.USER_LEAVE_CAHT, reply_markup=keyboard)

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
  await bot.send_photo(await db.get_match_id(message.from_user.id, conn), photo=photo_id)
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
#   "text": "Пользователь отправил жалобу во время общения: \n UserID: %s; \n Имя: %s; \n Текст жалобы: \n %s\nПользователь:\n %s" % (message.from_user.id, conn, await db.get_name(message.from_user.id, conn), help_message, message.from_user.id)
# })
  #----------------------------------------------------------------------------------
  #---------------------POST request for some STATISTIC------------------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
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
@dp.callback_query_handler(text='callback_look')
async def dont_like_look(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "reason_stop_don't_like"
#     }
#   ]
# })
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
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "reason_stop_don't_like_messaging"
#     }
#   ]
# })
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
  #data = await state.get_data()
  # ----------------------------------------------------------------
  # -----------POST request for some STATISTICS---------------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "reason_stop_other"
#    }
#   ]
# })
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
  await bot.send_message(message.from_user.id, text=texts.CALLBACK_MEETING % await db.get_name(await db.get_match_id(message.from_user.id, conn), conn), reply_markup=keyboard)


@dp.callback_query_handler(text='unlike_meeting')
async def set_was_meeting_no(message: types.Message, state: FSMContext):
  await db.set_meeting_status(message.from_user.id, conn, False)
  await state.reset_state(with_data=False)
  #------------------------------------------------------------------
  #-----------------POST requset for some STATISTICS-----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "meeting_not_happens"
#    }
#   ]
# })
  #------------------------------------------------------------------
  #data = await state.get_data()
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
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
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
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
#   "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id, conn),
#   "was_meeting": await db.is_meeting(message.from_user.id, conn),
#   "meeting_reaction": await db.get_meeting_reaction(message.from_user.id, conn),
#   "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id, conn)
# })
  # --------------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.END_CALLBACK)
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
  #await state.update_data(why_meeting_bad='Не понравился внешне')
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  await db.set_why_meeting_bad(message.from_user.id, conn, 'Не понравился внешне')
  # --------------POST request to END MATCHING--------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % message.from_user.id, json={
#   "reason": "Время истекло и %s" % await db.get_reason_to_stop(message.from_user.id, conn),
#   "was_meeting": await db.is_meeting(message.from_user.id, conn),
#   "meeting_reaction": await db.get_meeting_reaction(message.from_user.id, conn),
#   "why_meeting_bad": await db.get_why_meeting_bad(message.from_user.id, conn)
# })
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
  #data = await state.get_data()
  # --------------POST request to END MATCHING--------------
#   requests.post(url='https://server.unison.dating/user/stop_match?user_id=%s' % data['user_id'], json={
#   "reason": "Время истекло и %s" % data['reason_to_stop'],
#   "was_meeting": data["was_meeting"],
#   "meeting_reaction": data["meeting_reaction"],
#   "why_meeting_bad": data["why_meeting_bad"]
# })
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
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#***************************************************************************************************************************************************************************************************
#***************************************************************************MEETING PLACE***********************************************************************************************************

# ____________SPB_______________________
@dp.callback_query_handler(text='smena')
async def show_smena(message: types.Message, state:FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_smena')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.SMENA_COFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_smena')
async def choose_smena(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  if await db.is_matching(message.from_user.id, conn):
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.SMENA_MEET_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_place_smena"
#    }
#   ]
# })
  # -------------------------------------------

@dp.callback_query_handler(text='mickey')
async def show_mickey(message: types.Message, state: FSMContext):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_mickey')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.MICKEY_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_mickey')
async def choose_mickey(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  if await db.is_match(message.from_user.id, conn):
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.MICKEY_MEET_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_place_mickey_monkey"
#    }
#   ]
# })
  # -------------------------------------------

@dp.callback_query_handler(text='jack_and_chan')
async def show_jack(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_jack')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='spb_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.JACK_CAFE, reply_markup=keyboard)

@dp.callback_query_handler(text='choose_jack')
async def choose_jack(message: types.Message, state: FSMContext):
  await state.reset_state()
  if await db.is_matching(message.from_user.id, conn):
    await Form.has_match.set()
  else:
    await Form.no_match.set()
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.JACK_MEET_PLACE)
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
  #await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  double_b = types.InlineKeyboardButton(text=buttons_texts.DOUBLE_B, callback_data='double_b')
  propoganda = types.InlineKeyboardButton(text=buttons_texts.PROPOGANDA, callback_data='propoganda')
  she = types.InlineKeyboardButton(text=buttons_texts.SHE, callback_data='she')
  keyboard.add(double_b)
  keyboard.add(propoganda)
  keyboard.add(she)
  await bot.send_message(message.from_user.id, text=texts.MENU_SPB_PLACE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='double_b')
async def doube_b(message: types.Message, state: FSMContext):
  #await state.reset_state(with_data=False)
  #data = await state.get_data()
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_double_b')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.DOUBLE_B_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_double_b')
async def choose_double_b(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.DOUBLE_B_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_place_dabl_be"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()
  if await db.is_match(message.from_user.id, conn):#data['has_match']:
    await Form.has_match.set()
  else:
    await Form.no_match.set()

@dp.callback_query_handler(text='propoganda')
async def propoganda(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard = True)
  this_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_THIS, callback_data='choose_propoganda')
  other_place = types.InlineKeyboardButton(text=buttons_texts.CHOOSE_OTHER, callback_data='msc_menu')
  keyboard.add(this_place)
  keyboard.add(other_place)
  await bot.send_message(message.from_user.id, text=texts.PROPOGANDA_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_propoganda')
async def choose_propoganda(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.PROPOGANDA_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_place_propoganda"
#    }
#   ]
# })
  # -------------------------------------------
  #data = await state.get_data()
  if await db.is_match(message.from_user.id, conn):
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
  await bot.send_message(message.from_user.id, text=texts.SHE_CAFE, reply_markup=keyboard)
  #await Form.msc_meeting.set()

@dp.callback_query_handler(text='choose_she')
async def choose_she(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  await bot.send_message(message.from_user.id, text=texts.FIN_MEET_MESSAGE)
  await bot.send_message(await db.get_match_id(message.from_user.id, conn), text=texts.SHE_PLACE)
  # -------------------------------------------
  # --------POST reuqest for STATISTICS--------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#    {
#      "user_id": message.from_user.id,
#      "event_type": "bot_meeting_place_she"
#    }
#   ]
# })
  # -------------------------------------------
  if await db.is_match(message.from_user.id, conn):
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
  if await db.is_subscribed(message.from_user.id, conn):
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='have_subscribtion')
  else:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_RENEWAL_FAIL, reply_markup=keyboard)
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_renew_success)
async def payment_renew_success(message: types.Message, state: FSMContext):
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "bot_payment_renew_success"
#     }
#   ]
# })
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_RENEWAL_SUC)
  if await db.is_match(message.from_user.id, conn):
    await Form.has_match.set()
  else:
    await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ok)
async def payment_ok(message: types.Message, state: FSMContext):
  await state.reset_state(with_data=False)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
  # requests.post(url='https://server.unison.dating/user/payment?user_id=%s' % message.from_user.id, json={"status_payment": "pass"})
  # ----------------------------------------------------
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_NEW_SUC)
  # ----------------------------------------------------
  # ---------POST request for some STATISTICS-----------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
#   "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
#   "events": [
#     {
#       "user_id": message.from_user.id,
#       "event_type": "bot_subscribe_pay_success"
#     }
#   ]
# })
  # ----------------------------------------------------
  # ---------SENDING INFO to MODERATION CHAT------------
#   requests.post(url='', json={
# "chat_id":"-776565232",
# "text": "Пользователь оплатил подписку \n UserID: #id%s; \n Имя: %s " % (message.from_user.id, await db.get_name(message.from_user.id, conn))

# })
  # ----------------------------------------------------
  await Form.no_match.set()

@dp.callback_query_handler(state=Form.payment_ends)
async def payment_ends(message: types.Message, state: FSMContext):
  await db.set_subscribtion_status(message.from_user.id, conn, False)
  #data = await state.get_data()
  await state.reset_state(with_data=False)
  # ----------------------------------------------------------------
  # ----------------POST request for some STATISTICS----------------
#   requests.post(url='https://api.amplitude.com/2/httpapi', json={
# "api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
# "events":[{
# "user_id": message.from_user.id,
# "event_type": "bot_subscribe_pay_ended"
# }]
# })
  # ----------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  if await db.is_subscribed(message.from_user.id, conn):
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='have_subscribtion')
  else:
    get_subsc = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSC, callback_data='doesnt_have_subscribtions')
  keyboard.add(get_subsc)
  await bot.send_message(message.from_user.id, text=texts.PAYMENT_ENDS, reply_markup=keyboard)
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

#===================================================================================================================================================================================================
#===================================================================================================================================================================================================

async def get_advice(id: int, state: FSMContext):
  #data = state.get_data
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
  

async def payments_scheduler(message: types.Message, state: FSMContext):
  if await db.is_subscribed(message.from_user.id, conn):
    
    pass
  else:

    pass
  pass

async def on_startup():
  schedule_jobs()

if __name__ == '__main__':
    
    executor.start_polling(dp, skip_updates=True, on_startup=scheduler.start()) 