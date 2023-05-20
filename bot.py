import asyncio
import logging
import pymysql
from aiogram import types
#from aiogram.types import ParseMode
#from aiogram.utils import executor
from database import database
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

    cursor = connection.cursor()
#   cursor.execute("SELECT * FROM mytable")
#   rows = cursor.fetchall()


    # Инициализируем логгер
    logger = logging.getLogger(__name__)

     # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    
    # Инициализируем бот и диспетчер
    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)
    dp.include_router(database.router)

    # Настраиваем кнопку Menu
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
    
    
    
    
    
    