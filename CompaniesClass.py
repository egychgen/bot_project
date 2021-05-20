# import requests
# import json
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import matplotlib.dates as mdates
# # import pdfkit
# # import DataBase
# # path_wkhtmltopdf = '/.local/lib/python3.8/site-packages'
# # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# from datetime import datetime
# from fake_useragent import UserAgent
# ch = UserAgent().safari

import parsing



# Класс компания, принимает значение тикера компании и страны регистрации
# Доступные методы:
#     Get_Multiplicators принимает массив имен необходимых мультипликаторов(Мультипликатор -
#         это коэффициент пропорциональности, который измеряет, насколько эндогенная переменная
#         изменяется в ответ на изменение некоторой экзогенной переменной.), исходя из определения не трудно понять, \
#         что мультипликатор - некое отношение => в его названии обязательно должен содержаться "/".
#         Возвращает словарь в котором ключи - значения мультипликаторов, а значения - значания
#     Get_Company_Stocks_Grafic принимает на вход дату - массив из двух дат в секундах от 1970 года
#         (значения стоит преобразовывать через библиотеку datetime)
#         Сохраниет график в текущую директорию с название тикер.png
#     Compare_Grafic_Of_To_Companies принимает на вход дату и другой объект класса company, строит график
#         цен обоих компаний на одном поле.
#     get_price Возвращает цену (тип строка)
#     get_info Возвращает информацию о компании, если таковой нет возвращает что нет информации
#     parsing_divd Сохраняет в диррикторию таблицу с дивами в пдф
# Скрытые методы:
#     _Get_multiplicator_of_Russian_Comp
#     _Get_multiplicator_of_Abroad_Comp
#     Обе функции парсят мультипликторы, просто с различных сайтов
class Company:
    def __init__(self, tiker, country, fullname = "", info = "",):
        self.__tiker = tiker
        self.__country = country
        self.__fullname = fullname
        # db_companie_info = db_get_companie(tiker)
        if info == "":
            self.__info = parsing.parse_information(self.__tiker)

    def get_fullname(self):
        return self.__fullname

    def get_tiker(self):
        return self.__tiker

    def get_country(self):
        return self.__country

    def get_info(self):
        return self.__info

    def get_price(self):
        return parsing.parse_price(self.__tiker)

    def get_multiplicators(self, names):
        return parsing.parse_multiplicators(self.__tiker, self.__country ,names)

    def get_company_stocks_graphic(self, date, grafic_or_arrays):
        price_array, time_array = parsing.parse_graphics_data(self.__tiker, date)
        if grafic_or_arrays == "Grafic":
            fig = plt.figure(figsize=(20, 9))
            plt.plot(Time_Array, Price_Array, color="coral")
            plt.show()
            fig.savefig(self.__tiker)
        elif grafic_or_arrays == "Arrays":
            return time_array, price_array
        else:
            print("This function can take only two values of Grafic_or_Arrays: Grafic or Arrays")


    def compare_graphics_of_to_companies(self, other, date):
        self_time_array, self_price_array = self.get_company_stocks_graphic(date, "Arrays");
        other_time_array, other_price_array = other.get_company_stocks_graphic(date, "Arrays");
        fig = plt.figure(figsize=(20, 9))
        plt.plot(self_time_array, self_price_array, color="coral")
        plt.plot(other_time_array, other_price_array, color="blue")
        plt.show()
        fig.savefig(self.__tiker + "_" + other.__tiker)




# if __name__ == "__main__":
#     print(DataBase.db_get_all_companies())




#     date = ["1600000000", "1618317179"]
#
#     tiker1 = "FIVE"
#     tiker2 = "T"
#
#     names = ["P/E","P/S","EV/EBITDA", "HUI/432"]
#
#     Comp1 = Company(tiker1, "Russia")
#     Comp2 = Company(tiker2, "USA")
#
#     Comp1.get_company_stocks_graphic(date, "Grafic")
#     Comp2.Get_Company_Stocks_Graphic(date, "Grafic")
#
#     # Пока что это песпонтово, тк хз, как сравнивать,
#     # если у одних график в баксах, а у другиз в рублях
#     Comp1.compare_graphics_of_to_companies(Comp2, date)
#     print(tiker1 + "   "  + str(Comp1.get_multiplicators(names)))
#     print(tiker2 + "   "  + str(Comp2.get_multiplicators(names)))
#
#     Comp1.parsing_divd()
#     print(Comp1.get_info())


