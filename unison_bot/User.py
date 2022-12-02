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

from starting_menu import *
from pathlib import Path
from aiogram.dispatcher.filters import Filter
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, DB_PASSWORD, DB_USER, TESTING_TOKEN

bot = Bot(token=TESTING_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
scheduler = AsyncIOScheduler()
conn = None



text = '[User](tg://user?id=%s)'

@dp.message_handler(commands='start')
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, text=text % 1966031082, parse_mode='markdown')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=scheduler.start()) 
