import sqlite3


def add_user(name, id_user):
    conn = sqlite3.connect('adviser_bd.db')

    cursor = conn.cursor()
    query = "INSERT INTO user (iduser, name) VALUES (?, ?)"
    cursor.execute(query, (id_user, name))
    conn.commit()
    cursor.close()
    conn.close()



def get_name(id_user):
    
    conn = sqlite3.connect('adviser_bd.db')
    cursor = conn.cursor()
    query = f"SELECT name FROM user WHERE iduser = {id_user}"
    name = cursor.execute(query)
    conn.close()
    return name
 

def add_rating(item_type, item_id, rating):

    conn = sqlite3.connect("adviser_bd.db")
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {item_type}_ratings (id, rating) VALUES (?, ?)", (item_id, rating))
    conn.commit()
    conn.close()


def find_rec(Type, Genre, Age):
     # Поиск рекомендаций в базе данных
    conn = sqlite3.connect("adviser_bd.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {Type} WHERE genre='{Genre}' AND age<={Age} ORDER BY RAND() LIMIT 5")
    results = cursor.fetchall()
    conn.commit()
    conn.close()

    return results