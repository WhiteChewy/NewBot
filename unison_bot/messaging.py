import os
import aioschedule
import logging
import requests
import ru_message_texts as texts
import ru_buttons_texts as buttons_texts
import json
import asyncio
import base64

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

# STATES FOR STATE MACHINE
class Form(StatesGroup):
  help = State()
  has_match=State()
  why_dont_like=State()
  upload_photo_to_match = State()
  get_help_message = State()
# profile for testing
data = {
    'name': 'Никита',
    'city': 'Санкт-Петербург',
    'gender': 'М',
    'birthday': '07.08.1996',
    'reason': 'Серьезные отношения',
    'profile_photo' : './pic/profiles/877505237/main_profile_photo.jpg',
    'first_photo': './pic/profiles/877505237/first_extra_photo.jpg',
    'second_photo': './pic/profiles/877505237/second_extra_photo.jpg',
    'third_photo': './pic/profiles/877505237/third_extra_photo.jpg',
    'user_id': 87750523,
    'chat_id': 87750523,
    'status_match': 0,
    'subscribtion': False,
    'payment_url': '',
    'help': False,
    'tag_first_time': True,
    'tag_button_press': False,
    'tag_comunication_help': False,
    'reason_to_stop': '',
    'match_id': 891872881 # ILYA SUK
}

@dp.message_handler(command='start')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(texts=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    await bot.send_message(data['chat_id'], text=texts.MAIN_MENU, reply_markup=keyboard)
    if data['status_match']:
      Form.has_match.set()
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------CHECKING, GETTING AND CANCEL SUBSCRIBTION----------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='have_subscribtion')
async def abandon_subsribtion(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_menu_subscribe_btn"
    }
  ]
})
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    abandon_button = types.InlineKeyboardButton(text=buttons_texts.DENY, callback_data='deny_subscribtion')
    back_button = types.InlineKeyboardButton(text=buttons_texts.BACK, callback_data='main_menu')
    keyboard.add(abandon_button, back_button)
    await query.message.edit_text(text=texts.WHAT_TO_DO, reply_markup=keyboard)

@dp.callback_query_handler(text='doesnt_have_subscribtions')
async def subscribe(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_menu_subscribe_btn"
    }
  ]
})
    #--------------------------------------------------------------------------------------   
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        get_subscribe = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSCRIBE, callback_data='u_have_subscription')
    else:
        get_subscribe = types.InlineKeyboardButton(text=buttons_texts.GET_SUBSCRIBE, callback_data='subscribe')
    keyboard.add(get_subscribe)
    await query.message.edit_text(text=texts.SUBSCRIBE_INFO, reply_markup=keyboard)

@dp.callback_query_handler(text='u_have_subscription')
async def error_u_have_subscribtion(query: types.CallbackQuery, state: FSMContext):
    # data = await state.get_data()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_subscribe_btn"
    }
  ]
})
    #--------------------------------------------------------------------------------------   
    await query.message.edit_text(text=texts.SUBSCRIBE_ERROR_HAD)

@dp.callback_query_handler(text='subscribe')
async def pay_subscribe(query:types.CallbackQuery, state: FSMContext):
    #data = await state.get_date()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for getting payment url----------------------------
    request = requests.post(url='https://server.unison.dating/user/payment/request', json={
    "amount": "870"
})
    #--------------------------------------------------------------------------------------   
    await state.update_data(payment_url=request.text['payment_url'])
    await state.reset_state(with_data=False)
    query.message.edit_text(text=texts.PAY_URL % request.text['payment_url'])
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    request = requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_subscribe_pay_btn"
    }
  ]
})

@dp.callback_query_handler(text='deny_subscribtion')
async def abbandon_subscribe(message: types.Message, state: FSMContext):
    #data = await state.get_date()
    #--------------------------------------------------------------------------------------
    #----------------------POST request for some statistics--------------------------------
    requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_subscribe_cancel"
    }
  ]
})
    #--------------------------------------------------------------------------------------   
    #----------------------POST request for some statistics--------------------------------
    requests.post(url='https://server.unison.dating/user/payment/cancel?user_id%s' % data['user_id'], json={})
    #-------------------------------------------------------------------------------------- 
    pass
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ********************************GAME SECTION******************************************************************************************************************************************************
@dp.callback_query_handler(text='game1')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_ONE)
@dp.callback_query_handler(text='game2')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_TWO)
@dp.callback_query_handler(text='game3')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_THREE)
@dp.callback_query_handler(text='game4')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_FOUR)
@dp.callback_query_handler(text='game5')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_FIVE)
@dp.callback_query_handler(text='game6')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_SIX)
@dp.callback_query_handler(text='game7')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_SEVEN)
@dp.callback_query_handler(text='game8')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_EIGHT)
@dp.callback_query_handler(text='game9')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_NINE)
@dp.callback_query_handler(text='game10')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_TEN)
@dp.callback_query_handler(text='game11')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_ELEVEN)
@dp.callback_query_handler(text='game12')
async def game_one():
    bot.send_message(data['chat_id'], text=texts.GAME_TWELVE)
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------HELP SECTION--------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='help')
async def get_help(query: types.CallbackQuery, state: FSMContext):
  #state.update_data(help=True)
  data['help']=True
  #data = await stet.get_data()
  #-------------------------------------------------------------------------
  #----------------------POST request for some STATISTICS-------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_menu_support_btn"
    }
  ]
})
  #-------------------------------------------------------------------------
  
  #-------------------------------------------------------------------------
  #-------------------INSTUCTIONS ABOUT GETTING HELPED----------------------
  await query.message.edit_text(text=texts.GET_HELP)
  Form.help.set()
  #-------------------------------------------------------------------------
  await asyncio.sleep(120)
  #state.update_data(help=False)
  #state.reset_state(with_data=False)
  data['help']=False

@dp.message_handler(state=Form.help, content_types=types.ContentTypes.TEXT)
async def help_message(message: types.Message, state: FSMContext):
    #-------------------------------------------------------------------------
    #---------------------FORWARDING HELP------------------------------------
    requests.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
  "chat_id": "-776565232",
  "text": texts.HELP_MESSAGE % (data['user_id'], data['name'], message.text, data['user_id'])
  })
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ***********************TELEGRAM CONTACTS**********************************************************************************************************************************************************
@dp.callback_query_handler(text='our_telegram')
async def send_telegram_url(query: types.CallbackQuery):
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  subscribe_button = types.InlineKeyboardButton(text=buttons_texts.SUBSCRIBE, url='https://t.me/UnisonDating', callback_data='user_pressed_tg')
  keyboard.add(subscribe_button)
  query.message.edit_text(text=texts.OUR_TG, reply_markup=keyboard)

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
# ----------------------PAUSE mating----------------------------------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='paused_main_menu')
async def pause_menu(query: types.CallbackQuery,state: FSMContext):
  #data = await state.get_data()
  #-------------------------------------------------------------------------
  #---------------------POST request for STATISTIC--------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi',json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_menu_pause_btn"
    }
  ]
})
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
  write_help = types.InlineKeyboardButton(texts=buttons_texts.HELP_BUTTON, callback_data='help')
  were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
  pause_button = types.InlineKeyboardButton(text=buttons_texts.UNPAUSE, callback_data='unpaused_main_menu')
  keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
  await query.message.edit_text(text=texts.PAUSE_MAIN_MENU, reply_markup= None)

@dp.callback_query_handler(text='unpaused_main_menu')
async def messaging_start(query: types.CallbackQuery, state: FSMContext):
    #data = await state.get_data()
    #-------------------------------------------------------------------------
    #---------------------POST request for STATISTIC--------------------------
    requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_menu_resume_btn"
    }
  ]
})
    #-------------------------------------------------------------------------
    #---------------------POST request to UNPAUSE finding---------------------
    requests.post(url='https://server.unison.dating/user/pause?user_id=%s' % data['user_id'], json={"pause": "false"})
    #-------------------------------------------------------------------------
    #-------------------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    if data['subscribtion']:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='have_subscribtion')
    else:
        subscribes_button = types.InlineKeyboardButton(text=buttons_texts.SUBSC_BUTTON, callback_data='doesnt_have_subscribtions')
    write_help = types.InlineKeyboardButton(texts=buttons_texts.HELP_BUTTON, callback_data='help')
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='our_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='paused_main_menu')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    #--------------------set all data about match person zero----------------
    #await state.update_data(match_id=0)
    data['match_id'] = 0
    #await state.update_data(match_photo='')
    data['match_photo'] = ''
    #await state.update_data(match_name='')
    data['match_name'] = ''
    #await state.update_data(match_city='')
    data['match_city'] = ''
    #await state.update_data(match_reason='')
    data['match_reason'] = ''
    #await state.update_data(reason_stop='')
    data['reason_stop'] = ''
    #await state.update_data(tag_begin_comunication=False)
    data['tag_begin_comunication'] = False
    #------------------------------------------------------------------------
    await query.message.edit_text(data['chat_id'], text=texts.MAIN_MENU, reply_markup=keyboard)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# ************************************MATCHING MENU*************************************************************************************************************************************************
@dp.message_handler(state=Form.has_match)
async def start_communicating(query: types.CallbackQuery, state: FSMContext):
  #await state.update_data(tag_begin_comunocation = True)
  data['tag_begin_comunication'] = True
  #await state.update_data(status_match = 0)
  data['status_match'] = 0
  #await state.update_data(tag_first_time = False)
  data['tag_first_time'] = False
  await bot.send_message(data['user_id'], text=texts.NEW_MATCH)
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to get photo of match--------------------------------------
  requests.post(url='https://api.smartsender.eu/v1/contacts/%s/send' % data['user_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
}, json={
"type":"picture",
"watermark":1,
"media": data['match_photo']
})
  #--------------------------------------------------------------------------------------
  #--------------POST request to get match INFO------------------------------------------
  requests.post(url='https://api.smartsender.eu/v1/contacts/%s/send' % data['user_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
}, json={
  "type": "text",
  "watermark": 1,
  "content": texts.MATCH_INFO % (data['name'], data['city'], data['reason'])
})
  #--------------------------------------------------------------------------------------
  with open('./pic/find_match.png', 'rb') as img:
    await bot.send_photo(data['chat_id'], photo=img)
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  wanna_meet_button = types.InlineKeyboardButton(text=buttons_texts.WANNA_MEET, callback_data='wanna_meet')
  send_photo_button = types.InlineKeyboardButton(text=buttons_texts.SEND_PHOTO, callback_data='send_photo')
  send_request = types.InlineKeyboardButton(text=buttons_texts.SEND_REQUEST, callback_data='help_request_comunication')
  end_dialog = types.InlineKeyboardButton(text=buttons_texts.END_DIALOG, callback_data='end_dialog')
  keyboard.add(wanna_meet_button)
  keyboard.add(send_photo_button)
  keyboard.add(send_request)
  keyboard.add(end_dialog)
  bot.send_message(data['chat_id'], text=texts.FIND_MATCH, reply_markup= keyboard)

# FORWARDING MESSAGES TO MATCH PERSON
@dp.message_handler(state=Form.has_match, content_types= types.ContentTypes.TEXT)
async def forwarding_messages(message: types.Message, state: FSMContext):
  #data = await state.get_data()
  await bot.send_message(data['match_id'], text = message.text)

  
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# -------------------------------------ENDING COMUNICATION------------------------------------------------------------------------------------------------------------------------------------------
@dp.message_handler(text='end_dialog', state=Form.has_match)
async def end_dialog(query: types.CallbackQuery, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC--------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
"api_key":"ae25dbb3d0221e54b7d20f3a51e08edc",
"events":[{
"user_id": data['user_id'],
"event_type": "bot_chating_end_btn"
}]
})
  #--------------------------------------------------------------------------------------
  keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
  look_button = types.InlineKeyboardButton(text=buttons_texts.LOOK, callback_data='dont_like_look')
  comunication_button = types.InlineKeyboardButton(text=buttons_texts.COMUNICATION, callback_data='dont_like_comunication')
  ignore_button = types.InlineKeyboardButton(text=buttons_texts.IGNORE, callback_data='ignore')
  other_button = types.InlineKeyboardButton(text=buttons_texts.OTHER, callback_data='dont_like_other')
  keyboard.add(look_button, comunication_button, ignore_button, other_button)
  query.message.edit_text(text=texts.END_COMMUNICATION_MESSAGE, reply_markup=keyboard)

@dp.message_handler(state=Form.has_match, text='dont_like_look')
async def dont_like_look(query: types.CallbackQuery, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_chating_self_end_reason_ugly"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to some STATISTIC------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data["match_id"],
      "event_type": "bot_chating_partner_end_reason_ugly"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #data = await state.update_data()
  data['reason_to_stop'] = 'Не понравился внешне'
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['user_id'], headers={
    'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={"name": "stop_match"})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH MATCHING----------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['match_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={
"name":"stop_match"
})
  #--------------------------------------------------------------------------------------
  #--------------------------------------------------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_ended_partner_choosing"
    }
  ]
})
  await state.reset_state(with_data=False)

@dp.message_handler(state=Form.has_match, text='ignore')
async def show_ignore(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_chating_self_end_reason_noreply"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_self_end_reason_noreply"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #data = await state.update_data(reason_to_stop='собеседник не отвечает')
  data['reason_stop'] = 'собеседник не отвечает'
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['user_id'], headers={
    'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={"name": "stop_match"})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH MATCHING----------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['match_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={
"name":"stop_match"
})
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_ended_partner_choosing"
    }
  ]
})
  await state.reset_state(with_data=False)

@dp.message_handler(state=Form.has_match, text='dont_like_comunication')
async def dont_like_comunication(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_chating_partner_end_reason_stupid"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_partner_end_reason_stupid"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #await state.update_data(reason_to_stop="не понравилось общение")
  data['reason_to_stop'] = "не понравилось общение"
  #--------------------------------------------------------------------------------------
  #--------------POST reuqest to stop MATCH----------------------------------------------
  requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['user_id'], headers={
    'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={"name": "stop_match"})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH MATCHING----------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['match_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={
"name":"stop_match"
})
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_ended_partner_choosing"
    }
  ]
})
  await state.reset_state(with_data=False)

@dp.message_handler(state=Form.has_match, text='dont_like_other')
async def dont_like_other(query: types.CallbackQuery, state: FSMContext):
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_chating_self_end_reason_else"
    }
  ]
})
  #--------------------------------------------------------------------------------------
  #------------------POST request for some STATISTICS------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_partner_end_reason_else"
    }
  ]
})
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
  requests.post(url='https://server.unison.dating/user/stop_match?%s' % data['user_id'], json={"reason": data['reason_to_stop']})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH USER-------------------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['user_id'], headers={
    'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={"name": "stop_match"})
  #--------------------------------------------------------------------------------------
  #---------------STOP MATCH MATCHING----------------------------------------------------
  requests.post(url='https://api.smartsender.com/v1/contacts/%s/fire' % data['match_id'], headers={
'Authorization': 'Bearer jc5u29SmevXUwVf2BX3tSyAuHEr4CGhNTwQVqcju4r6tTwelpTItann5Dfl8'
  }, json={
"name":"stop_match"
})
  #--------------------------------------------------------------------------------------
  #----------------POST for some STATISTICS----------------------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['match_id'],
      "event_type": "bot_chating_ended_partner_choosing"
    }
  ]
})
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# **************************************************************************************************************************************************************************************************
# **********************************FORWARDIN PHOTO TO MATCH****************************************************************************************************************************************
@dp.callback_query_handler(text='send_photo')
async def send_photo_to_match(query: types.CallbackQuery, state: FSMContext):
  await query.message.edit_text(text=texts.UPLOAD_PHOTO_TO_MATCH)
  await Form.upload_photo_to_match.set()
@dp.message_handler(state=Form.upload_photo_to_match, content_types=types.ContentType.PHOTO)
async def upload_photo_to_match(message: types.Message, state: FSMContext):
  photo_id = await message.photo[-1].file_id()
  #-----------------------------------------------------------------
  #----------------POST request for some statistics-----------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_send_photo_to_user"
    }
  ]
})
  #-----------------------------------------------------------------
  # WE FORWARDING PHOTO SO IT CAN BE DONE WITH ID OF IMAGE
  bot.send_photo(data['match_id'], photo=photo_id)
# **************************************************************************************************************************************************************************************************
# **************************************************************************************************************************************************************************************************

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------REQUEST HELP WITH COMUNICATION--------------------------------------------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text='help_request_comunication')
async def request_comunication_help(query: types.CallbackQuery, state: FSMContext):
  #data = await state.get_data()
  query.message.edit_text(text=texts.COMUNICATION_HELP)
  await state.reset_state(with_data=False)
  Form.get_help_message.set()
@dp.message_handler(state=Form.get_help_message, content_types= types.ContentTypes.TEXT)
async def get_comunication_help_message(message: types.Message, state: FSMContext):
  help_message = message.text
  await state.reset_state(with_data=False)
  requests.post(url='https://api.telegram.org/bot1966031082:AAFW5vy3QAbE46alW4dx8Zf_sDouLkJ3MFY/sendMessage', json={
  "chat_id": "-776565232",
  "text": "Пользователь отправил жалобу во время общения: \n UserID: %s; \n Имя: %s; \n Текст жалобы: \n %s\nПользователь:\n %s" % (data['user_id'], data['name'], help_message, data['user_id'])
})
  #----------------------------------------------------------------------------------
  #---------------------POST request for some STATISTIC------------------------------
  requests.post(url='https://api.amplitude.com/2/httpapi', json={
  "api_key": "ae25dbb3d0221e54b7d20f3a51e08edc",
  "events": [
    {
      "user_id": data['user_id'],
      "event_type": "bot_chating_send_petition"
    }
  ]
})
  
  pass
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)