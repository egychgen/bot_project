import sqlite3

# В данной области записаны функции и методы для работу с БД
# Все методы использованные здесь имеют понятные названия и преднозначены для формирования объекта класса Company
# И хранения большовательстких данный


def db_initialise():
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        # Для запроса
        # Request = DBConnection.execute()
        dbobject.execute("""CREATE TABLE IF NOT EXISTS users(
            id INT PRIMARY KEY,
            gender TEXT,
            age INT); 
        """)
        dbconnection.commit()

        dbobject.execute("""CREATE TABLE IF NOT EXISTS Companies(
                tiker TEXT PRIMARY KEY, fullname TEXT, country TEXT, info);
            """)

        dbconnection.commit()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
        dbconnection = False
    finally:
        if (dbconnection):
            dbconnection.close()




def db_add_user(user_id, gender = "", age = 0):
    user = tuple(user_id, gender, age)
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("INSERT INTO users VALUES(?, ?, ?);", user)
        dbconnection.commit()
        dbconnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
        dbconnection = False
    finally:
        if (dbconnection):
            dbconnection.close()

def db_get_all_users():
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT * FROM users;""")
        res_array = dbobject.fetchall()
        resDict_array = []
        for res in res_array:
            resDict_array.append(dict(zip([c[0] for c in dbobject.description], res)))
        dbconnection.close()
    except sqlite3.Error as error:
        resDict_array = []
        print("SQLite3 error", error)
    finally:
        return resDict_array


def db_get_user(user_id):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT * 
                            FROM users
                            WHERE userid = {};""".format(user_id))
        res = dbobject.fetchall()
        res = dict(zip([c[0] for c in dbobject.description], res))
        dbconnection.close()
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
    finally:
        return res



def db_company_is_in_base(tiker):
    res = []
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT * 
                            FROM Companies
                            WHERE tiker = "{0}"; """.format(tiker))
        res = dbobject.fetchall()
        dbconnection.close()
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)

        dbconnection = False
    finally:
        if not res:
            return False
        else:
            return True



def db_add_company(tiker: str,  country: str, fullname = "", info = ""):
    new_company = tuple([tiker, fullname, country, info])
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("INSERT INTO Companies VALUES(?, ?, ?, ?);", new_company)
        dbconnection.commit()
        dbconnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)
        dbconnection = False
    finally:
        if (dbconnection):
            dbconnection.close()

def db_update_company_info(tiker, info):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("UPDATE Companies SET info = '{0}' WHERE tiker = '{1}';".format(info, tiker))
        dbconnection.commit()
        dbconnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)

def db_set_company_full_name(tiker, fullname):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("UPDATE Companies SET fullname = '{0}' WHERE tiker = '{1}';".format(fullname, tiker))
        dbconnection.commit()
        dbconnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)


def db_get_company(tiker: str) -> dict:
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT *
                            FROM Companies
                            WHERE tiker = "{}" ;""".format(tiker))
        res = dbobject.fetchone()
        res = dict(zip([c[0] for c in dbobject.description], res))
    except sqlite3.Error as error:
        res = []
        print("SQLite3 error", error)
        dbconnection = False
    finally:
        if (dbconnection):
            dbconnection.close()
        return res


def db_get_all_companies():
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT * FROM Companies;""")
        res_array = dbobject.fetchall()
        resDict_array = []
        for res in res_array:
            resDict_array.append(dict(zip([c[0] for c in dbobject.description], res)))
        dbconnection.close()
    except sqlite3.Error as error:
        resDict_array = []
        print("SQLite3 error", error)
    finally:
        return resDict_array


def db_get_company_info(tiker):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT info 
                            FROM Companies
                            WHERE tiker = '{}' ;""".format(tiker))
        res = dbobject.fetchall()
        res = res[0]
        res = res[0]
        dbconnection.close()
    except sqlite3.Error as error:
        res = ""
        print("SQLite3 error", error)
        dbconnection = False
    finally:
        return res

def db_delete_company_by_tiker(tiker):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""DELETE 
                            FROM Companies
                            WHERE tiker = '{}';""".format(tiker))
        dbconnection.close()
    except sqlite3.Error as error:
        print("SQLite3 error", error)


def db_find_company_tiker_by_name(fullname):
    try:
        dbconnection = sqlite3.connect("FinanceBot.db")
        dbobject = dbconnection.cursor()
        dbobject.execute("""SELECT tiker 
                               FROM Companies
                               WHERE fullname = "{}" ;""".format(fullname))
        res = dbobject.fetchall()
        res = res[0]
        res = res[0]
        dbconnection.close()
    except sqlite3.Error as error:
        res = ""
        print("SQLite3 error", error)
    finally:
        return res



