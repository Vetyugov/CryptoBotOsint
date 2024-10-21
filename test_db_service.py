from db_service import DataBaseService as db
import unittest
import sqlite3

class DBService_Test(unittest.TestCase):
    test_user_id = '99999999999'
    test_db_name = 'test_db'

    def setUp(self):
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute('create table if not exists tg_user(id integer not null constraint tg_user_pk primary key autoincrement, tg_user_id varchar(255) not null);')
        cursor.execute(f'INSERT INTO tg_user (tg_user_id) VALUES ({self.test_user_id})')
        conn.commit()
        conn.close()

    def tearDown(self):
        conn = sqlite3.connect(self.test_db_name)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM tg_user where tg_user_id = {self.test_user_id}')
        conn.commit()
        conn.close()

    def test_find_user(self):
        test_db = db(self.test_db_name)
        user_from_db = test_db.find_user(self.test_user_id)
        self.assertIsNotNone(user_from_db)
        self.assertEqual(user_from_db.user_tg_id, self.test_user_id)

    def test_save_new_user(self):
        test_db = db(self.test_db_name)
        new_user_id = '1234567890'
        test_db.save_new_user(new_user_id)
        user_from_db = test_db.find_user(new_user_id)
        self.assertIsNotNone(new_user_id)
        self.assertEqual(user_from_db.user_tg_id, new_user_id)
