import mysql
from aiogram import Router
from aiogram import Bot, Dispatcher
import time
from PIL import Image
from io import BytesIO
from aiogram.types import Message

from config_data.config import Config, load_config

config: Config = load_config('\.env')
router: Router = Router()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()

def connection(config: Config) -> mysql.connect:
    return mysql.connect(host=config.db.db_host, user=config.db.db_user,
                           passwd=config.db.db_password, database=config.db.database, port=int(config.database.port))


def addUser(msg: Message) -> bool:
    name = msg.text
    
    print(name)
    print(msg.from_id, msg.from_user.id)
    con = connection(config)
    try:
        with con.cursor() as cursor:
            insert_query = f'INSERT INTO user (`user_id`, `name`, `age`, `type`, `genre`, `in_find`)'\
            f'VALUES({msg.from_user.id}, "{name}", null, null, null, False);'
            cursor.execute(insert_query)
            con.commit()
        return True
    except Exception as ex:
        print(ex)
        print("Ошибка работы бд")
    finally:
        return False
    
        
def SelectOneUser(msg: Message):
    try:
        con = connection(config)
        with con.cursor() as cursor:
            select_user = "SELECT * FROM user"\
            f" WHERE idUser = {msg.from_user.id}"
            cursor.execute(select_user)
            return cursor.fetchone()
    except Exception as ex:
        print(ex)

def UpdateUser(msg: Message, name: str = None, age: int = None, type: str = None, genre: str = None, in_find: bool = None):
    try:
        con = connection(config)
        if name is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET name = {name} WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if age is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET age = {age} WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if type is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET type = {type} WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
            
        if genre is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET genre = {genre} WHERE user_id = {msg.from_user.id}"                    
                cursor.execute(update_user)
                con.commit()
            
        if in_find is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE users_game SET in_find = {in_find} WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
    except Exception as ex:
        print(ex)


def display_random_movie(msg: Message):

    con = connection(config)
    with con.cursor() as cursor:
        cursor.execute("SELECT * FROM movie ORDER BY RAND() LIMIT 1")
        movie = cursor.fetchone()

    cover = Image.open(BytesIO(movie[1]))
    title = movie[2]
    year = movie[3]
    description = movie[5]

    #print(f"Title: {title} ({year})")
    #cover.show()

    with open(cover, 'rb') as photo_file:
        bot.send_photo(photo=photo_file)
    # Send the movie information

    message = f"{title} ({year})\n{description}"
    bot.send_message(text=message)




def get_movie_info(movie_id):
    # Create a cursor object
    con = connection(config)
    cursor = con.cursor()

    # Execute the SELECT query
    query = "SELECT cover, title, release_year FROM movies WHERE id = %s"
    cursor.execute(query, (movie_id,))

    # Fetch the first row of the result set
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    # Return the movie cover, title, and release year
    return result






def FirstFiveUsers(msg: Message) -> str:
    first_five: str = "Tоп-игроков\n"
    try:
        con = connection(config)
        with con.cursor() as cursor:
            sortusers = "select * from users_game order by wins DESC limit 5"
            cursor.execute(sortusers)
            rows = cursor.fetchall()
            count: int = 1
            for row in rows:
                first_five += f"{count}). " + f"{row[3]} {row[2]} --- Сыграно: " + f'{row[7]}, Побед: {row[6]};\n'
                count += 1
        return first_five
    except Exception as ex:
        print(ex)
    finally:
        return first_five

def isFindUser(id: int):
    try:
        con = connection(config)
        with con.cursor() as cursor:
            select_user = "SELECT * FROM users_game"\
                    f" WHERE idUser = {id}"
            cursor.execute(select_user)
            if len(cursor.fetchall()) > 0:
                return False
        return True
    finally:
        return False

def addHistory(msg: Message, iswin: int):
    try:
        con = connection(config)
        named_tuple = time.localtime() # получить struct_time
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        with con.cursor() as cursor:
            add_history = f'INSERT INTO history (`id_user`, `old_game`, `time`) '\
            f'VALUES ({msg.from_id}, {iswin}, "{time_string}");'
            cursor.execute(add_history)
            con.commit()
    except Exception as ex:
        print(ex)

def updateKD(msg: Message):
    count_win = _counWinGame(msg)
    count_game = _countGame(msg)
    print(count_game, count_win, count_win/count_game)
    try:
        con = connection(config)
        with con.cursor() as cursor:
            update_kd = f'UPDATE kd SET total_games = {count_game}, total_wins = {count_win}, ratio = {count_win/count_game} WHERE id=1;'
            cursor.execute(update_kd)
            con.commit()
    except Exception as ex:
        print(ex, "updateKD")

def _counWinGame(msg: Message) -> int:
    try:
        con = connection(config)
        with con.cursor() as cursor:
            count_win_game = 'select * from history where old_game=1;'
            count = cursor.execute(count_win_game)
            print("Победныx игр: ",count)
            return count
    except Exception as ex:
        print(ex)

def _countGame(msg: Message) -> int:
    try:
        con = connection(config)
        with con.cursor() as cursor:
            count_game = 'select * from history;'
            count = cursor.execute(count_game)
            print("Всего игр", count)
            return count
    except Exception as ex:
        print(ex)

def stringKD(msg: Message):
    try:
        con = connection(config)
        string = "Статистика игр всего сервера:\n"
        with con.cursor() as cursor:
            string_kd = "SELECT * FROM kd WHERE id=1;"
            cursor.execute(string_kd)
            data = cursor.fetchone()
            string += f"Всего игр сыграно на сервере: {data[1]}\n\n"
            string += f"Всего побед на сервере: {data[2]}\n\n"
            string += f"Побед/кол-во игр: {data[3]}\n"       
        return string
    except Exception as ex:
        print(ex)
    finally:
        return string