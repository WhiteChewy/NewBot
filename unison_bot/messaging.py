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
user_form = User()
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
    'chat_id': 87750523,
    'status_match': 0,
    'subscribtion': False,
    'payment_url': ''
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
    were_in_telegram_button = types.InlineKeyboardButton(text=buttons_texts.TELEGRAM_BUTTON, callback_data='in_telegram')
    pause_button = types.InlineKeyboardButton(text=buttons_texts.PAUSE, callback_data='pause')
    keyboard.add(subscribes_button, write_help, were_in_telegram_button, pause_button)
    await bot.send_message(data['chat_id'], text='Ожидайте подбора партнера!', reply_markup=keyboard)

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
    #--------------------------------------------------------------------------------------   


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


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)