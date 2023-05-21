from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from database import database
from aiogram.filters import CommandStart
from lexicon.lexicon_ru import LEXICON_RU

# ------- Начальное меню -------

button_hello: KeyboardButton = KeyboardButton(text=LEXICON_RU['hello_button']) #Поздороваться
button_selection: KeyboardButton = KeyboardButton(text=LEXICON_RU['sel_button']) #Начать выбор
button_question: KeyboardButton = KeyboardButton(text=LEXICON_RU['ques_button']) #Что ты умеешь?

# Инициализируем билдер для клавиатуры меню
menu_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
menu_builder.row(button_hello, button_selection, button_question, width=2)


# Создаем клавиатуру
menu = menu_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)




button_menu: KeyboardButton = KeyboardButton(text=LEXICON_RU['menu']) #В меню

# Инициализируем билдер для клавиатуры меню
cancel_menu_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
cancel_menu_builder.row(button_menu, width=2)


# Создаем клавиатуру
cancel_menu = cancel_menu_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)



# ------- Клавиатура после "Готов к выбору?" -------

# Создаем кнопки с ответами согласия и отказа
button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])

# Инициализируем билдер для клавиатуры с кнопками "Да!" и "Не"
yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
yes_no_kb_builder.row(button_yes, button_no, width=2)

# Создаем клавиатуру с кнопками "Да!" и "Не"
yes_no_kb = yes_no_kb_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)


# ------- Клавиатура после "Оставить прошлый выбор?" -------

# Создаем кнопки с ответами согласия и отказа
button_yes_choice: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_choice'])
button_no_choice: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_choice'])

# Инициализируем билдер для клавиатуры с кнопками "Давай!" и "Не хочу"
yes_no_choice_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

yes_no_choice_builder.row(button_yes_choice, button_no_choice, width=2)

yes_no_choice = yes_no_choice_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)



# ------- Создаем игровую клавиатуру без использования билдера -------

# Создаем кнопки клавиатуры типов
button_book: KeyboardButton = KeyboardButton(text=LEXICON_RU['book'])
button_film: KeyboardButton = KeyboardButton(text=LEXICON_RU['film'])
button_tv_show: KeyboardButton = KeyboardButton(text=LEXICON_RU['tv_show'])

# Создаем клавиатуру типов
type_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_book],
                                              [button_film],
                                              [button_tv_show]],
                                    one_time_keyboard=True,
                                    resize_keyboard=True)




# Кнопки жанра
fantastic_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['fantastic'])
comedy_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['comedy'])
detective_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['detective'])
adventures_button: KeyboardButton = KeyboardButton(text=LEXICON_RU['adventures'])


genres_builder = ReplyKeyboardBuilder()
genres_builder.row(fantastic_button, comedy_button, width=2)
genres_builder.row(detective_button, adventures_button, width=2)


# Создаем клавиатуру "
genres = genres_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)



# ------- Клавиатура во время поиска -------

# Создаем кнопки Другое и Закончить поиск
button_other: KeyboardButton = KeyboardButton(text=LEXICON_RU['other'])
button_rate: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating'])
button_end: KeyboardButton = KeyboardButton(text=LEXICON_RU['end'])


find_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

find_builder.row(button_rate,button_end, width=2)
find_builder.row( button_other , width=1)

find_kb = find_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)


# Создаем кнопки с ответами согласия и отказа
button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_1'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_2'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_3'])
button_4: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_4'])
button_5: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_5'])

# Инициализируем билдер для клавиатуры с кнопками "Да!" и "Не"
rate_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с параметром width=2
rate_builder.row(button_1, button_2, button_3, width=3)
rate_builder.row(button_4, button_5, width=2)

# Создаем клавиатуру с кнопками "Да!" и "Не"
rate_kb = rate_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)



#НАЙТИ, КАК ВСТАВИТЬ В СООБЩЕНИЕ ОТ БОТА





