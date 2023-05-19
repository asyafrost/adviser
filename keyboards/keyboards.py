from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
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
button_book: KeyboardButton = KeyboardButton(text=LEXICON_RU['books'])
button_film: KeyboardButton = KeyboardButton(text=LEXICON_RU['films'])
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

# Создаем кнопки с ответами согласия и отказа
button_other: KeyboardButton = KeyboardButton(text=LEXICON_RU['other'])
button_end: KeyboardButton = KeyboardButton(text=LEXICON_RU['end'])

find_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

find_builder.row(button_other, button_end, width=2)

find_kb = find_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)

'''

# Кнопки жанра
button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_1'])
button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_2'])
button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_3'])
button_4: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_4'])
button_5: KeyboardButton = KeyboardButton(text=LEXICON_RU['rating_5'])

genres_builder = ReplyKeyboardBuilder()
genres_builder.row(button_1, button_2, button_3, width=2)
genres_builder.row(button_4, button_5, width=2)

'''

# Создаем клавиатуру "
genres = genres_builder.as_markup(
                                one_time_keyboard=True,
                                resize_keyboard=True)


#НАЙТИ, КАК ВСТАВИТЬ В СООБЩЕНИЕ ОТ БОТА


url_object = 'aiogram_stepik_course'
url_button_1: InlineKeyboardButton = InlineKeyboardButton(
                                    text='Открыть в источнике',
                                    url=f'{url_object}')

rating_button: InlineKeyboardButton = InlineKeyboardButton(
                                    text='Поставить оценку',
                                    callback_data='rating_button_pressed'
                                    #url=f'tg://user?id={user_id}'
                                    )


    



LEXICON: dict[str, str] = {
    'but_1': 'Оценка 1',
    'but_2': 'Оценка 2',
    'but_3': 'Оценка 3',
    'but_4': 'Оценка 4',
    'but_5': 'Оценка 5',
    'but_6': 'Оценка 6',
    'but_7': 'Оценка 7',
    'but_8': 'Оценка 8',
    'but_9': 'Оценка 9',
    'but_10': 'Оценка 10',}

BUTTONS: dict[str, str] = {
    'btn_1': '1',
    'btn_2': '2',
    'btn_3': '3',
    'btn_4': '4',
    'btn_5': '5',
    'btn_6': '6',
    'btn_7': '7',
    'btn_8': '8',
    'btn_9': '9',
    'btn_10': '10'}


# Функция для генерации инлайн-клавиатур "на лету"
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


rate_keyboard = create_inline_kb(4, **BUTTONS)
