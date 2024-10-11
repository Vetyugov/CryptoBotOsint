
import sqlite3
SQLITE_FILE_PATH = './osint_tg.sqlite'


class TgUser():
    def __init__(self, id, user_tg_id):
        self.id = id,
        self.user_tg_id = user_tg_id

class DataBaseService:
    def __init__(self):
        # Создаем подключение к базе данных (файл source будет создан)
        # self.connection = sqlite3.connect(SQLITE_FILE_PATH)

        try:
            # пытаемся подключиться к базе данных
            self.sqlite_connection = sqlite3.connect(SQLITE_FILE_PATH)
            self.cursor = self.sqlite_connection.cursor()
            print("Подключен к SQLite")
        except:
            # в случае сбоя подключения будет выведено сообщение  в STDOUT
            print('Can`t establish connection to database')
        return

    def close_connection(self):
        self.sqlite_connection.close()
    def find_user(self, user_tg_id: str):
        self.cursor.execute(
            f'SELECT * FROM tg_user where tg_user_id = {user_tg_id}'
        )
        users = self.cursor.fetchall()
        if len(users) == 0:
            return None
        if len(users) > 1:
            return Exception("Пользователей оказалось более одного")
        user = users[0]
        return TgUser(user[0], user[1])

    def save_new_user(self, user_tg_id: str):
        if self.find_user(user_tg_id) is not None:
            return

        self.cursor.execute(
            f'INSERT INTO tg_user (tg_user_id) VALUES (?)',
            (user_tg_id,)
        )
        self.sqlite_connection.commit()
        print("Запись успешно добавлена таблицу tg_user ", self.cursor.rowcount)
        self.cursor.close()


