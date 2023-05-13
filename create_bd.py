import sqlite3

def create_tabels():
    conn = sqlite3.connect("adviser_bd.db")
    cursor = conn.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS book(
    `idbook` int NOT NULL,
    `name` varchar(45) NOT NULL,
    `age` int DEFAULT NULL,
    `genre` varchar(45) DEFAULT NULL,
    `picture` longblob,
    `release` date DEFAULT NULL,
    `description` mediumtext,
    PRIMARY KEY (`idbook`),
    UNIQUE KEY `idbook_UNIQUE` (`idbook`))
    '''
    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS `user` (
    `iduser` int NOT NULL,
    `name` varchar(45) DEFAULT NULL,
    `prev_book` varchar(45) DEFAULT NULL,
    `prev_movie` varchar(45) DEFAULT NULL,
    `prev_tv_show` varchar(45) DEFAULT NULL,
    PRIMARY KEY (`iduser`),
    UNIQUE KEY `iduser_UNIQUE` (`iduser`)
    )
    '''
    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS movie(
    `idmovie` int NOT NULL,
    `name` varchar(45) NOT NULL,
    `age` int DEFAULT NULL,
    `genre` varchar(45) DEFAULT NULL,
    `picture` longblob,
    `release` date DEFAULT NULL,
    `description` mediumtext,
    PRIMARY KEY (`idmovie`),
    UNIQUE KEY `idmovie_UNIQUE` (`idmovie`))
    '''
    )


    cursor.execute('''CREATE TABLE IF NOT EXISTS tv_show(
    `idtv_show` int NOT NULL,
    `name` varchar(45) NOT NULL,
    `age` int DEFAULT NULL,
    `genre` varchar(45) DEFAULT NULL,
    `picture` longblob,
    `release` date DEFAULT NULL,
    `description` mediumtext,
    PRIMARY KEY (`idtv_show`),
    UNIQUE KEY `idtv_show_UNIQUE` (`idtv_show`))
    '''
    )

    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    FOREIGN KEY (item_id) REFERENCES items (id),
                    FOREIGN KEY (user_id) REFERENCES users (id))''')

    conn.commit()
    conn.close()



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
 