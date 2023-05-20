import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import sqlite3


conn = sqlite3.connect('adviser.db')
cursor = conn.cursor()


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Фантастика", callback_data='genre_fantastic'),
            InlineKeyboardButton("Детектив", callback_data='genre_detective'),
        ],
        [
            InlineKeyboardButton("Классика", callback_data='genre_classic'),
            InlineKeyboardButton("Фэнтези", callback_data='genre_fantasy'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Добро пожаловать! Какой жанр книг Вам нравится?', reply_markup=reply_markup)


def choose_genre(update, context):
    query = update.callback_query
    genre = query.data.split('_')[1]

    context.user_data['genre'] = genre

    query.edit_message_text(text=f"Вы выбрали жанр {genre}. Сколько Вам лет?")


def choose_age(update, context):
    age = int(update.message.text)

    context.user_data['age'] = age

    genre = context.user_data['genre']
    cursor.execute(f"SELECT * FROM books WHERE genre='{genre}' AND age<={age}")
    books = cursor.fetchall()

    if not books:
        update.message.reply_text("К сожалению, подходящих книг не найдено.")
        return

    book_list = '\n'.join([f"{book[0]} - {book[1]}" for book in books])
    update.message.reply_text(f"Подходящие книги:\n{book_list}")


def main():
    updater = Updater(token='TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(choose_genre))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, choose_age))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
