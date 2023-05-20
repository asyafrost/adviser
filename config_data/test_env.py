import asyncio
import logging
import pymysql
from aiogram import types
#from aiogram.types import ParseMode
#from aiogram.utils import executor
from database.database import display_random_movie
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_main_menu

# Функция конфигурирования и запуска бота
async def main():

    # Загружаем конфиг в переменную config
    config: Config = load_config("D:/Programms/XAMPP/htdocs/adviser/config_data/.env")

    connection = pymysql.connect(
       host=config.db.db_host,
       user=config.db.db_user,
       password=config.db.db_password,
       database=config.db.database,
       port=config.db.db_port,
       charset='utf8mb4',
       cursorclass=pymysql.cursors.DictCursor
   )

