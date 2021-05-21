# import requests
# import json
import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import matplotlib.dates as mdates
# import pandas as pd
# import numpy as np
import parsing



# Класс компания, принимает значение тикера компании и страны регистрации
# Доступные методы:
#     get_multiplicators принимает массив имен необходимых мультипликаторов(Мультипликатор -
#         это коэффициент пропорциональности, который измеряет, насколько эндогенная переменная
#         изменяется в ответ на изменение некоторой экзогенной переменной.), исходя из определения не трудно понять, \
#         что мультипликатор - некое отношение => в его названии обязательно должен содержаться "/".
#         Возвращает словарь в котором ключи - значения мультипликаторов, а значения - значания
#     get_company_stocks_graphic принимает на вход дату - массив из двух дат в секундах от 1970 года
#         (значения стоит преобразовывать через библиотеку datetime)
#         Сохраниет график в текущую директорию с название тикер.png
#     compare_graphics_of_to_companies принимает на вход дату и другой объект класса company, строит график
#         цен обоих компаний на одном поле.
#     get_price Возвращает цену (тип строка)
#     get_info Возвращает информацию о компании, если таковой нет возвращает что нет информации
#     get_fullname - возвращает название компании
#     get_country - возвращает страну регистрации компании
#     get_tiker - возвращает тикер компании
#
#     parsing_divd Сохраняет в диррикторию таблицу с дивами в пдф
# Скрытые методы:
#     _Get_multiplicator_of_Russian_Comp
#     _Get_multiplicator_of_Abroad_Comp
#     Обе функции парсят мультипликторы, просто с различных сайтов
class Company:
    def __init__(self, tiker, country, fullname = "", info = "",):
        self.__tiker = tiker
        self.__country = country
        if not fullname:
            self.__fullname = tiker
        else:
            self.__fullname = fullname
        self.__info = info

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
            if price_array[0] > price_array[-1]:
                color = "red"
            else:
                color = "forestgreen"
            if self.get_country() != "Rus":
                y_label = "Price in USA Dollars"
            else:
                y_label = "Price in Russian Rubles"
            data = {self.get_tiker(): price_array}
            fig = plt.figure(figsize=(8, 5))
            plt.ylabel(y_label)
            plt.xlabel("Date")
            plt.title(self.get_fullname())
            plt.plot(time_array, price_array, color=color, linewidth=3)
            plt.legend(data, loc=2, fontsize="large", labelcolor=color, shadow=True)
            plt.grid()
            plt.show()
            fig.savefig(self.__tiker)
        elif grafic_or_arrays == "Arrays":
            return time_array, price_array
        else:
            print("This function can take only two values of Grafic_or_Arrays: Grafic or Arrays")


    def compare_graphics_of_to_companies(self, other, date):
        self_time_array, self_price_array = self.get_company_stocks_graphic(date, "Arrays");
        other_time_array, other_price_array = other.get_company_stocks_graphic(date, "Arrays");
        if self.get_country() != "Rus":
            try:
                currency_value = int(parsing.parse_currency_value_for_graphics("USD"))
            except:
                currency_value = 75
            for i in range(len(self_price_array)):
                self_price_array[i] = self_price_array[i] * currency_value
        if other.get_country() != "Rus":
            try:
                currency_value = int(parsing.parse_currency_value_for_graphics("USD"))
            except:
                currency_value = 75
            for i in range(len(other_price_array)):
                other_price_array[i] = other_price_array[i] * currency_value
        if self_price_array[0] > self_price_array[-1]:
            self_color = "red"
        else:
            self_color = "lime"
        if other_price_array[0] > other_price_array[-1]:
            other_color = "red"
        else:
            other_color = "forestgreen"
        data = {self.get_tiker(): self_price_array,
                other.get_tiker(): other_price_array}
        fig = plt.figure(figsize=(8, 5))
        plt.ylabel("Price in Russian Rubles")
        plt.xlabel("Date")
        plt.title(self.get_fullname() + "  VS  "  + other.get_fullname())
        plt.plot(self_time_array, self_price_array, color=self_color, linewidth = 3)
        plt.plot(other_time_array, other_price_array, color=other_color, linewidth = 3)
        plt.legend(data, loc=2, fontsize="large", labelcolor = "blue", shadow=True)
        plt.grid()
        plt.show()
        fig.savefig(self.__tiker + "_" + other.__tiker)




if __name__ == "__main__":
    # print(DataBase.db_get_all_companies())




    date = ["1600000000", "1618317179"]

    tiker1 = "SBER"
    tiker2 = "AAPL"

    # names = ["P/E","P/S","EV/EBITDA", "HUI/432"]

    Comp1 = Company(tiker1, "Rus")
    Comp2 = Company(tiker2, "USA")

    Comp1.get_company_stocks_graphic(date, "Grafic")
    # Comp2.Get_Company_Stocks_Graphic(date, "Grafic")

    # Пока что это песпонтово, тк хз, как сравнивать,
    # если у одних график в баксах, а у другиз в рублях
    # Comp1.compare_graphics_of_to_companies(Comp2, date)
    # print(tiker1 + "   "  + str(Comp1.get_multiplicators(names)))
    # print(tiker2 + "   "  + str(Comp2.get_multiplicators(names)))

    # Comp1.parsing_divd()
    # print(Comp1.get_info())


