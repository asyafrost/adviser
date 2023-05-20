from aiogram import Router, Bot
import asyncio
from aiogram.filters.state import StatesGroup, State
from typing import Optional
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, ContentType
from keyboards.keyboards import *
from lexicon.lexicon_ru import LEXICON_RU
from database.database import *
from config_data.config import Config, load_config

config: Config = load_config("D:/Programms/XAMPP/htdocs/adviser/config_data/.env")

bot: Bot = Bot(token=config.tg_bot.token)
router: Router = Router()
user_state = {}


class Mydialog(StatesGroup):
    otvet = State()   


# ------- ИЗМЕНИТЬ ФУНКЦИИ, ЧУЖИЕ!!!! -------

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']) or Text(text=LEXICON_RU['ques_button']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=button_menu)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['authors']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/authors'], reply_markup=button_menu)



@router.message(Text(text=LEXICON_RU['hello_button']))
async def process_help_command(message: Message):

    name = message.from_user.first_name
    if haveUser(message.from_user.id) == False:
        addUser(message)
    
    answer_text = f"Привет {name}! {LEXICON_RU['start_find']}"
    await message.answer(text=answer_text, reply_markup=yes_no_kb)

    



# Этот хэндлер срабатывает на согласие пользователя пройти анкету
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=type_kb)


# Этот хэндлер срабатывает на быстрое начатие анкеты
@router.message(Text(text=LEXICON_RU['sel_button']))
async def start_find(message: Message):
    if haveUser(message.from_user.id) == False:
        addUser(message)
    await message.answer(text=LEXICON_RU['yes'], reply_markup=type_kb)


# Этот хэндлер срабатывает на отказ пользователя пройти анкету
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])






# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_1_pressed'
@router.callback_query(Text(text=['big_button_1_pressed']))
async def process_button_1_press(callback: CallbackQuery):
    if callback.message.text != 'Нажать БОЛЬШАЯ КНОПКА 1':
        await callback.message.edit_text(
            text='Была нажата БОЛЬШАЯ КНОПКА 1',
            reply_markup=callback.message.reply_markup)
    await callback.answer(text='Ура! Нажата кнопка 1',
                          show_alert=True)


# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(Text(text=[LEXICON_RU['book'],
                           LEXICON_RU['film'],
                           LEXICON_RU['tv_show']]))
async def choice_type_button(message: Message):
   # bot_choice = get_bot_choice()
    Type: str
    if message.text == LEXICON_RU['book']:
        Type = 'book'
    if message.text == LEXICON_RU['film']:
        Type = 'movie'
    if message.text == LEXICON_RU['tv_show']:
        Type = 'tv_show'
    UpdateUser(message, type=Type)
                                       #CHANGE
    await message.answer(text=f'{LEXICON_RU["age"]} ')
   # winner = get_winner(message.text, bot_choice)
    #await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)