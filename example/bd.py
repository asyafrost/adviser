from telebot.async_telebot import AsyncTeleBot
from telebot import types # для указание типов
import sqlite3
import asyncio

#bot 
bot = AsyncTeleBot("6066480941:AAHHJxBXlpLxc2RUFphoyS7KugmBnfpn_7c")

connect = sqlite3.connect('adviser.db')
cursor = connect.cursor()



@bot.message_handler(commands = ['start'])
async def start(message):
    

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Начать анкетирование")
    markup.add(btn1, btn2)
    await bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я твой бот-помощник в выборе досуга".format(message.from_user), reply_markup=markup)
    

    

    

async def registration(message):
    cursor.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER
    )""")

    connect.commit()

    #cheсk
    people_id = message.chat.id
    cursor.execute(f"SELECT id FROM user WHERE id = {people_id}")
    data = cursor.fetchone()
    
    if data is None:
        #add values in fields
        users = [message.chat.id]
        cursor.execute("INSERT INTO user (column1, column2) VALUES (?, ?);", (users, message.chat.first_name))
        connect.commit()
    else:
        await bot.send_message(message.chat.id, 'Такой пользователь уже существует')



@bot.message_handler(content_types=['text'])
async def func(message):
    if(message.text == "👋 Поздороваться"):
        await bot.send_message(message.chat.id, text="Привет) Спасибо что обратился ко мне за советом!)")
    if(message.text == "❓ Начать анкетирование"):
        await bot.send_message(message.chat.id, text="Хорошо, сейчас начнем!")


@bot.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
   if int(msg.text.lower()) <100 & int(msg.text.lower()) > 0 :
       await msg.answer('Запомню')
   else:
       await msg.answer('Точно? Может попробуем еще раз?')
       

@bot.message_handler(content_types=['text'])
async def func(message):
    pass

@bot.message_handler(commands = ['delete'])
async def delete(message):
    pass




#polling
asyncio.run(bot.polling())