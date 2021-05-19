import sqlite3
import CompaniesClass


def DBInitialise():
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        # Для запроса
        # Request = DBConnection.execute()
        DBObject.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY,
            gender TEXT,
            age TEXT); 
        """)
        DBConnection.commit()

        DBObject.execute("""CREATE TABLE IF NOT EXISTS Companies(
                tiker TEXT PRIMARY KEY,
                fullname TEXT,
                country TEXT,
                information TEXT
                firstuser INTEGER,
                FOREIGN KEY (firstuser) REFERENCES user(id) ON DELETE CASCADE  ON UPDATE  CASCADE); 
            """)

        DBConnection.commit()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()




def DBAddUser(user: tuple):
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        DBObject.execute("INSERT INTO users VALUES(?, ?, ?);", user)
        DBConnection.commit()
        DBConnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()

def GetAllUsers():
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        DBObject.execute("""SELECT * FROM users;""")
        res = DBObject.fetchall()
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()
        return res


def GetUser(user: tuple):
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        DBObject.execute("""SELECT * 
                            FROM users
                            WHERE userid = {};""".format(user[0]))
        res = DBObject.fetchall()
        if res == []:
            DBAddUser(user)
            res = GetUser(user)
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()
        return res


def DBAddCompanie(Emitent: CompaniesClass.Company):
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        CompanyTuple=(Emitent.get_tiker(), Emitent.get_tiker(), Emitent.get_country(), Emitent.get_info())
        DBObject.execute("INSERT INTO Companies VALUES(?, ?, ?);", CompanyTuple)
        DBConnection.commit()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()


def GetAllCompanies():
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        DBObject.execute("""SELECT * FROM Companies;""")
        res = DBObject.fetchall()
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()
        return res


def GetCompany(Emitent: CompaniesClass.Company):
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        DBObject.execute("""SELECT * 
                            FROM Companies;
                            WHERE tiker = {}""".format(Emitent.get_tiker()))
        res = DBObject.fetchall()
        if res == []:
                DBAddCompanie(Emitent)
                res = GetCompany(Emitent)
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()
        return res

def TestAddCompanie():
    try:
        DBConnection = sqlite3.connect("FinanceBot.db")
        DBObject = DBConnection.cursor()
        CompanyTuple=tuple(tiker = "FIVE", name = "X5GDR", country = "RUSSIA", info = "paterocka perik", userid = "23")
        DBObject.execute("INSERT INTO Companies VALUES(?, ?, ?);", CompanyTuple)
        DBConnection.commit()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
    finally:
        if (DBConnection):
            DBConnection.close()


DBInitialise()
# A = CompaniesClass.Company()

GetAllUsers()

# while True:
#     print("Введите Id, Пол и Возрвст пользователя через пробел")
#     UserString = input()
#     if UserString == "":
#         print("Вы ничего не ввели я отключаюсь")
#         break
#     user = tuple(UserString.split())
#     DBAddUser(user)
#
print(GetAllUsers())