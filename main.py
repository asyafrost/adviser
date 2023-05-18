import sqlite3
import asyncio
from telegram.ext import *
from telegram.ext import filters
import tracemalloc
import time
import logging
from asgiref.sync import sync_to_async
import create_bd, Token, work_bd




logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)



tracemalloc.start()

create_bd.create_tabels()


# Функции для обработки команд бота
async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Как тебя зовут??")
    return "user_name"
    
async def user_name(update, context):
    try:
        
        name = update.message.text.strip()
        people_id = update.message.chat.id

        work_bd.add_user(people_id, name)
        #context.user_data["name"] = name
        await context.bot.register_next_step_handler(context, choose_type)

    except Exception as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, введите корректное имя.")
        print(e)

    
async def choose_type(update, context):

    people_id = update.message.chat.id
    name = work_bd.get_name(people_id)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {name}! Я могу помочь тебе выбрать книгу, сериал или фильм. Что тебе больше всего нравится?")
    
    user_choice = update.message.text.lower()
    if user_choice == "книга":
        context.user_data["type"] = "book"
    elif user_choice == "сериал":
        context.user_data["type"] = "tv_show"
    elif user_choice == "фильм":
        context.user_data["type"] = "movie"
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Я не понимаю, что ты хочешь. Выбери книгу, сериал или фильм.")
        await context.bot.register_next_step_handler(update, choose_type)
        return
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Какой жанр тебе нравится?")
    await context.bot.register_next_step_handler(update, choose_genre)



def choose_genre(update, context):
    user_genre = update.message.text.lower()
    context.user_data["genre"] = user_genre
    context.bot.send_message(chat_id=update.effective_chat.id, text="Сколько тебе лет?")
    return "choose_age"

def choose_age(update, context):
    user_age = update.message.text
    context.user_data["age"] = user_age
    
def find(update, context):
    Type = context.user_data['type']
    Age = context.user_data["age"]
    Genre = context.user_data['genre']
    results = work_bd.find_rec(Type, Genre, Age)
    if len(results) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text="К сожалению, я не могу найти подходящих рекомендаций.")
    else:
        message = "<b>Я нашел для тебя следующие рекомендации:</b>\n\n"
        message += "<table>"
        message += "<tr><th>Обложка</th><th>Название</th><th>Дата выхода</th><th>Описание</th></tr>"
        for result in results:
            message += f"<tr><td>{result[5]}</td><td>{result[2]}</td><td>{result[6]}</td><td>{result[7]}</td></tr>"
        message += "</table>"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")
    
            
    
    return ConversationHandler.END



def rate_item(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Оцените рекомендацию!")
    item_type = context.user_data["type"]
    item_id = context.user_data["id"]
    rating = update.message.text
    # Insert rating into database
    work_bd.add_rating(item_type, item_id, rating)
    # Send confirmation message to user
    context.bot.send_message(chat_id=update.effective_chat.id, text="Спасибо за вашу оценку!")
    return ConversationHandler.END

def calculate_average_ratings():
    conn = sqlite3.connect("adviser.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM items")
    item_ids = cursor.fetchall()
    for item_id in item_ids:
        cursor.execute(f"SELECT AVG(rating) FROM ratings WHERE item_id={item_id[0]}")
        average_rating = cursor.fetchone()[0]
        cursor.execute(f"UPDATE items SET rating={average_rating} WHERE id={item_id[0]}")
    conn.commit()
    conn.close()


# Создание объекта для работы с ботом
updater = Updater(Token.token_bot, update_queue=None)

# Создание обработчиков команд бота
def fallback(update, context):
    update.message.reply_text("Сори, я не понимаю.")

conv_handler = ConversationHandler(
    entry_points=[CommandHandler(["start", "help"], start), CommandHandler("rate", rate_item)],
    states={
        "choose_type": [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type)],
        "choose_genre": [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_genre)],
        "choose_age": [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_age)],
        "rate_item": [MessageHandler(filters.TEXT & ~filters.COMMAND, rate_item)],
    },
    fallbacks=[MessageHandler(filters.TEXT & ~filters.COMMAND, fallback)]
)

#def main():
    #updater.dispatcher.add_handler(CommandHandler('start', start))
    #updater.start_polling()
    #updater.initialize()

if __name__ == '__main__':
    #main()
    #updater = Updater("6066480941:AAHHJxBXlpLxc2RUFphoyS7KugmBnfpn_7c", update_queue=None)
    
    # Commands
    '''dispatcher = updater.dispatcher
    #dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler("help", start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_genre))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_genre))

    # Run bot
    updater.run_polling(1.0)
    '''
    application = Application.builder().token("6066480941:AAHHJxBXlpLxc2RUFphoyS7KugmBnfpn_7c").build()

    

    # Commands
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_type))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_genre))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, choose_age))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rate_item))
    
    

    # Run bot
    application.run_polling(1.0)
    
    while True:
        calculate_average_ratings()
        time.sleep(3600)  # Update ratings every hour