from db_service import DataBaseService

def save_user():
    database = DataBaseService()
    database.save_new_user("123123123123")
def test_find_user():
    database = DataBaseService()
    database.find_user()


if __name__ == '__main__':
    save_user()