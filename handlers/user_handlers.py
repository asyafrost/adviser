from aiogram import Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery
from keyboards.keyboards import *
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_winner

router: Router = Router()


# ------- ИЗМЕНИТЬ ФУНКЦИИ, ЧУЖИЕ!!!! -------

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=button_menu)


# Этот хэндлер срабатывает на согласие пользователя пройти анкету
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    await message.answer(text=LEXICON_RU['yes'], reply_markup=type_kb)


# Этот хэндлер срабатывает на отказ пользователя играть в игру
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
    bot_choice = get_bot_choice()                                       #CHANGE
    await message.answer(text=f'{LEXICON_RU["age"]} ')
    winner = get_winner(message.text, bot_choice)
    await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)