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
import asyncpg

from aiogram.dispatcher.filters import Filter
from User import User
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN

