from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config_data.config import Config, load_config


# Загружаем конфиг в переменную config
config: Config = load_config("D:/Programms/XAMPP/htdocs/adviser/config_data/.env")

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()


# Создаем асинхронную функцию
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать работу с ботом'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/support',
                   description='Поддержка'),
        BotCommand(command='/authors',
                   description='Авторы бота')]

    await bot.set_my_commands(main_menu_commands)


if __name__ == '__main__':
    # Регистрируем асинхронную функцию в диспетчере,
    # которая будет выполняться на старте бота,
    dp.startup.register(set_main_menu)
    # Запускаем поллинг
    dp.run_polling(bot)