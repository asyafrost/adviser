from aiogram import Router, Bot
import asyncio
from aiogram.filters.state import StatesGroup, State
from typing import Optional
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove, URLInputFile
from keyboards.keyboards import *
from lexicon.lexicon_ru import LEXICON_RU
from database.database import *
from config_data.config import Config, load_config

config: Config = load_config("D:/Programms/XAMPP/htdocs/adviser/config_data/.env")

bot: Bot = Bot(token=config.tg_bot.token)
router: Router = Router()





    # Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(Text(text=[LEXICON_RU['fantastic'],
                           LEXICON_RU['comedy'],
                           LEXICON_RU['detective'],
                           LEXICON_RU['adventures']]))
async def choice_genre_button(message: Message):
   # bot_choice = get_bot_choice()
    genre: str
    if message.text == LEXICON_RU['fantastic']:
        genre = 'fantastic'
    if message.text == LEXICON_RU['comedy']:
        genre = 'comedy'
    if message.text == LEXICON_RU['detective']:
        genre = 'detective'
    if message.text == LEXICON_RU['adventures']:
        genre = 'adventures'


    

    await UpdateUser(message, genre=genre)
    await UpdateUser(message, in_find=True)
    await display_random(message)
    


async def display_random(message: Message):
    image, message_user = await display_random_atributs(message)
    try:
   
        await message.answer_photo(photo=image, caption=message_user, reply_markup=find_kb)
        print('Image sent successfully')
    except Exception as e:
        print('Error sending image:', e)
    




@router.message((Text(text=[LEXICON_RU['rating_1'],
                           LEXICON_RU['rating_2'],
                           LEXICON_RU['rating_3'],
                           LEXICON_RU['rating_4'],
                           LEXICON_RU['rating_5']])))
async def end_button(message: Message):
    await message.answer(text=f'{LEXICON_RU["save_rating"]} ', reply_markup=find_kb)
    rating = int(message.text)
    
    await UpdateRating(message, new_rating=rating)




# ------- ИЗМЕНИТЬ ФУНКЦИИ, ЧУЖИЕ!!!! -------

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=menu)
    await UpdateUser(message, in_find=False)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=cancel_menu)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['menu']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/menu'], reply_markup=menu)

# Этот хэндлер срабатывает на команду /help
@router.message(Text(text=LEXICON_RU['menu']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/menu'], reply_markup=menu)


@router.message(Text(text=LEXICON_RU['ques_button']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=cancel_menu)


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands=['authors']))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/authors'], reply_markup=cancel_menu)



@router.message(Text(text=LEXICON_RU['hello_button']))
async def process_help_command(message: Message):

    name = message.from_user.first_name
    
    answer_text = f"Привет {name}! {LEXICON_RU['start_find']}"
    await message.answer(text=answer_text, reply_markup=yes_no_kb)

    



# Этот хэндлер срабатывает на согласие пользователя пройти анкету
@router.message(Text(text=LEXICON_RU['yes_button']))
async def process_yes_answer(message: Message):
    if haveUser(message.from_user.id) == False:
        addUser(message)
        await message.answer(text=f"{LEXICON_RU['yes']}\n{LEXICON_RU['type']}", reply_markup=type_kb)
    else:
        await message.answer(text=LEXICON_RU['last_choice'], reply_markup=yes_no_choice)


# Этот хэндлер срабатывает на быстрое начатие анкеты
@router.message(Text(text=LEXICON_RU['sel_button']))
async def start_find(message: Message):
    if haveUser(message.from_user.id) == False:
        addUser(message)
        await message.answer(text=f"{LEXICON_RU['yes']}\n{LEXICON_RU['type']}", reply_markup=type_kb)
    else:
        await message.answer(text=LEXICON_RU['last_choice'], reply_markup=yes_no_choice)



# Этот хэндлер срабатывает на быстрое начатие анкеты
@router.message(Text(text=LEXICON_RU['yes_choice']))
async def start_anket(message: Message):
    await message.answer(text=LEXICON_RU['yes_last'], reply_markup=find_kb)
    await display_random(message)

    

# Этот хэндлер срабатывает на быстрое начатие анкеты
@router.message(Text(text=LEXICON_RU['no_choice']))
async def start_anket(message: Message):
    await message.answer(text=LEXICON_RU['no_last'], reply_markup=type_kb)


# Этот хэндлер срабатывает на отказ пользователя пройти анкету
@router.message(Text(text=LEXICON_RU['no_button']))
async def process_no_answer(message: Message):
    await message.answer(text=LEXICON_RU['no'])


    

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
    await UpdateUser(message, type=Type)
                                       #CHANGE
    await message.answer(text=f'{LEXICON_RU["age"]} ', reply_markup=ReplyKeyboardRemove())
   # winner = get_winner(message.text, bot_choice)
    #await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)




    
# Этот хэндлер срабатывает на любую из игровых кнопок
@router.message(lambda x: x.text.isdigit() and (1 <= int(x.text) <= 100))
async def find_out_age(message: Message):
   # bot_choice = get_bot_choice()
    age: int = int(message.text) 
    if 0 <= age <=100:
        await UpdateUser(message, age=age)
    else:
        await message.answer(text=f'{LEXICON_RU["false_age"]}{LEXICON_RU["age"]}')
        return find_out_age(message)
                                       
    await message.answer(text=f'{LEXICON_RU["genre"]}', reply_markup=genres)




    #await message.answer(text='Ищем дальше?', reply_markup=find_kb)

  
@router.message(Text(text=[LEXICON_RU['other']]))
async def other_button(message: Message):
    await display_random(message)


@router.message(Text(text=[LEXICON_RU['end']]))
async def end_button(message: Message):
    await UpdateUser(message, in_find=False)
    await message.answer(text=f'{LEXICON_RU["end_find"]} ', reply_markup=menu)

@router.message(Text(text=[LEXICON_RU['rating']]))
async def end_button(message: Message):
    await message.answer(text=f'{LEXICON_RU["rating_answer"]} ', reply_markup=rate_kb)





'''

@router.callback_query(display_random_atributs)
async def display_random(message: Message):
    type, age, genre = await display_random_atributs(message)
    print(type)
    con = connection(config)
    with con.cursor() as cursor:
        try:
            query = f"SELECT * FROM `{type}` WHERE age <= {age} AND genre = '{genre}' ORDER BY RAND() LIMIT 1"
            cursor.execute(query)
                    
            result = cursor.fetchone()
        except KeyError:
            print("The specified row does not exist.")


        
    
    title = result[0]
    year = result[1]
    description = result['description']
    link = result['link']

    image_bytes = result['picture']
    with io.BytesIO(image_bytes) as file:
        image = Image.open(file)

         # Send photo to user
        with io.BytesIO() as photo_file:
            image.save(photo_file, 'JPG')
            photo_file.seek(0)
            await bot.send_photo(chat_id=msg.from_user.id, photo=photo_file)

    #with open(cover, 'rb') as photo_file:
        #bot.send_photo(photo=photo_file)
    # Send the movie information

    message = f"{title} ({year})\n{description}"
    

    next =InlineKeyboardButton(text= 'Следующий',callback_data= 'next')
    back =InlineKeyboardButton(text= 'Предыдущий',callback_data= 'previous')
    add = InlineKeyboardButton(text= 'Добавить в корзину',callback_data= 'add')

    kb_result = InlineKeyboardMarkup(row_width=2)
    kb_result.add(next,back,add)
        
    await message.answer(text= message, reply_markup=kb_result)
    #await message.answer(text=f'{LEXICON_RU["age"]} ')'''