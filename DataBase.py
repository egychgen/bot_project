import sqlite3

def DBInitialise():
    DBConnection = sqlite3.connect("FinanceBot.db")
    DBObject = DBConnection.cursor()
    # Для запроса
    # Request = DBConnection.execute()
    DBObject.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        gender TEXT,
        age TEXT); 
    """)
    DBConnection.commit()

    DBObject.execute("""CREATE TABLE IF NOT EXISTS Companies(
            tiker TEXT PRIMARY KEY,
            fullname TEXT,
            country TEXT,
             TEXT); 
        """)

    DBConnection.commit()
    DBConnection.close()




def DBAddUser(user):
    DBConnection = sqlite3.connect("FinanceBot.db")
    DBObject = DBConnection.cursor()
    DBObject.execute("INSERT INTO users VALUES(?, ?, ?);", user)
    DBConnection.commit()
    DBConnection.close()


def GetAllUsers():
    DBConnection = sqlite3.connect("FinanceBot.db")
    DBObject = DBConnection.cursor()
    DBObject.execute("""SELECT * FROM users;""")
    res = DBObject.fetchall()
    return res
    DBConnection.close()



while True:
    print("Введите Id, Пол и Возрвст пользователя через пробел")
    UserString = input()
    if UserString == "":
        print("Вы ничего не ввели я отключаюсь")
        break
    user = tuple(UserString.split())
    DBAddUser(user)

print(GetAllUsers())