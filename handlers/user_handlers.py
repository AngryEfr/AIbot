from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.filters import CommandStart, Command

from config_data.config import Config, load_config
from database.db_quick_commands import register_user, choice_character, get_message, get_content, save_answer, \
    save_message
from utils.api import fetch_completion

from json import loads
from openai import AsyncOpenAI


router = Router()
config: Config = load_config('.env')
client = AsyncOpenAI(
    api_key=config.tg_bot.ai_token,
)


# Обработка команды /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    register_user(message)
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Выбор персонажа',
                                                           web_app=WebAppInfo(
                                                               url='https://angryefr.github.io/testcharacter/',
                                                           ))]],
                                 resize_keyboard=True)
    await message.answer(text='Привет, для того чтобы выбрать персонажа, жми кнопку внизу.', reply_markup=markup)


# Обработка команды /menu
@router.message(Command(commands='menu'))
async def process_help_admin_command(message: Message):
    markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Выбор персонажа',
                                                           web_app=WebAppInfo(
                                                               url='https://angryefr.github.io/testcharacter/',
                                                           ))]],
                                 resize_keyboard=True)
    await message.answer(text='Чтобы изменить персонажа, жми кнопку внизу.', reply_markup=markup)


# Обработка web app
@router.message(F.content_type == 'web_app_data')
async def web_app(message: Message):
    res = loads(message.web_app_data.data)
    try:
        choice_character(message, res['name'])
    except Exception as Error:
        print(Error)
    else:
        meeting_message = get_message(res['name'])
        await message.answer(meeting_message)


# Обработка текстовых сообщений
@router.message(F.text)
async def process_messaged(message: Message):
    save_message(message)
    try:
        result = await fetch_completion(get_content(message), message)
    except Exception as error:
        print(error)
    else:
        save_answer(message, result['choices'][0]['message']['content'])
        await message.answer(result['choices'][0]['message']['content'])
