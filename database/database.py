import pymysql
import os
import requests
from aiogram import Router
from aiogram import Bot, Dispatcher,  F
import time
from PIL import Image
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from io import BytesIO
from aiogram.types import Message
import urllib.parse
from config_data.config import Config, load_config

config: Config = load_config('\.env')
router: Router = Router()

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher()

def connection(config: Config) -> pymysql.connect:
    return pymysql.connect(database=config.db.database, 
                           host=config.db.db_host, 
                           user=config.db.db_user,
                           passwd=config.db.db_password, 
                           port=int(config.db.db_port),
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)


def addUser(message: Message) -> bool:
    
    
    print(message.from_user.first_name)
    print(message.message_id, message.from_user.id)
    con = connection(config)
    try:
        with con.cursor() as cursor:
            insert_query = f'INSERT INTO user (`user_id`, `name`, `age`, `type`, `genre`, `in_find`)'\
            f'VALUES({message.from_user.id}, "{message.from_user.first_name}", null, null, null, False);'
            cursor.execute(insert_query)
            con.commit()
        return True
    except Exception as ex:
        print(ex)
        print("Ошибка работы бд")
    finally:
        return False
    
        
def haveUser(id: int) -> bool:

    try:
        con = connection(config)
        with con.cursor() as cursor:
            find_user = "SELECT * FROM user"\
            f" WHERE user_id = {id}"
            cursor.execute(find_user)
            result = cursor.fetchone()
            # if a row is returned, the user exists in the database
            if result:
                return True
            else:
                return False
    except Exception as ex:
        print(ex)
        return False



def SelectOneUser(msg: Message):
    try:
        con = connection(config)
        with con.cursor() as cursor:
            select_user = "SELECT * FROM user"\
            f" WHERE user_id = {msg.from_user.id}"
            cursor.execute(select_user)
            return cursor.fetchone()
    except Exception as ex:
        print(ex)

async def UpdateUser(msg: Message, name: str = None, age: int = None, type: str = None, genre: str = None, in_find: bool = False):
    try:
        con = connection(config)
        if name is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE user SET name = '{name}' WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if age is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE user SET age = '{age}' WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
        
        if type is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE user SET type = '{type}' WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
            
        if genre is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE user SET genre = '{genre}' WHERE user_id = {msg.from_user.id}"                    
                cursor.execute(update_user)
                con.commit()
            
        if in_find is not None:
            with con.cursor() as cursor:
                update_user = f"UPDATE user SET in_find = {in_find} WHERE user_id = {msg.from_user.id}"
                cursor.execute(update_user)
                con.commit()
    except Exception as ex:
        print(ex)


async def display_random_atributs(msg: Message):
    
    con = connection(config)
    with con.cursor() as cursor:
        try:
            cursor.execute(f"SELECT type FROM user WHERE user_id = {msg.from_user.id}")
            type_user = cursor.fetchone()
            

            cursor.execute(f"SELECT age FROM user WHERE user_id = {msg.from_user.id}")
            age_user = cursor.fetchone()

            cursor.execute(f"SELECT genre FROM user WHERE user_id = {msg.from_user.id}")
            genre_user = cursor.fetchone()

            type = type_user['type']
            age = age_user['age']
            genre = genre_user['genre']

            print(type, age, genre)

            query = f"SELECT * FROM `{type}` WHERE age <= {age} AND genre = '{genre}' ORDER BY RAND() LIMIT 1"
            cursor.execute(query)
                    
            result = cursor.fetchone()

            query = f"UPDATE user SET find_id = {result['id']} WHERE user_id = {msg.from_user.id}"    
            cursor.execute(query)
            con.commit()
                    

        except KeyError:
            print("The specified row does not exist.")

    title :str = result['name']
    year :int  = result['year']
    description :str= result['description']
    link :str= result['link']

    message = f"{title} ({year})\n\n{description}\n\nСсылка: {link}"
    print(message)
    print(link)

    try:
        # получение url изображения из MySQL
        image_blob = result['picture']
        if image_blob is not None:
            image = URLInputFile(f'{image_blob}')
            print('Все ок')
        else:
            print('Image blob is None')
    except Exception as ex:
        print(ex)

    

    return image, message


   

async def UpdateRating(msg:Message, new_rating: int):

    con = connection(config)
    with con.cursor() as cursor:
        try:
            cursor.execute(f"SELECT type, find_id FROM user WHERE user_id = {msg.from_user.id}")
            find_object = cursor.fetchone()

            type_name = find_object['type']
            res_id = find_object['find_id']

            sql = f"SELECT rating, number_of_ratings FROM `{type_name}` WHERE id = {res_id}"
            cursor.execute(sql)
            new_result = cursor.fetchone()

            current_rating = new_result['rating']
            number_of_ratings = new_result['number_of_ratings']

            # Calculate the new average rating
            new_average_rating = (current_rating * number_of_ratings + new_rating) / (number_of_ratings + 1)

            # Update the database with the new average rating
           
            sql = f"UPDATE `{type_name}` SET rating = {new_average_rating}, number_of_ratings = {number_of_ratings + 1} WHERE id = {res_id}"
            cursor.execute(sql)

            

        except KeyError:
            print("The specified row does not exist.")

        con.commit()

            # Close the database connection
        con.close()
   
'''
#image_blob = urllib.parse.quote(image_blob)
    response = requests.get(image_blob)
    photo_file = BytesIO(response.content)
    photo_file.name = 'image.jpeg' 
    if os.path.exists('image.jpeg'):
        os.remove('image.jpeg')

    # создание временного файла с изображением
    with open('image.jpeg', 'wb') as file:
        file.write(image_blob)
    
    # проверка, что файл создан корректно
    if os.path.exists('image.jpeg'):
        print('File created successfully')
        img = Image.open('image.jpeg')
        width, height = img.size
        print(f'Width: {width}, Height: {height}')

    else:
        print('Error creating file')
    
    
    chat_id = msg.chat.id
    file = FSInputFile("cat.png")
  
    with io.BytesIO(image_bytes) as file:
        image = Image.open(file)

         # Send photo to user
        with io.BytesIO() as photo_file:
            image.save(photo_file, 'JPG')
            photo_file.seek(0)
            await bot.send_photo(chat_id=msg.from_user.id, photo=photo_file)

    with open(image_bytes, 'rb') as f:
        img = Image.open(f)
        img.show()

 

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
        '''
