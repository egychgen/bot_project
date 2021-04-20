import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pdfkit
from datetime import datetime
from fake_useragent import UserAgent
ch = UserAgent().chrome

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
    def __init__(self, tiker, country):
        self.__tiker = tiker
        self.__country = country


    def get_price(self):
        r = requests.get("https://investmint.ru/{0}/".format(self.__tiker), headers={'User-Agent': ch})
        text = r.text
        text = text[text.find("Курс акций") + 10:text.find("Курс акций") + 200]
        return text[text.find("num150 me-2") + 13:text.find("num150 me-2") + 18]

    def get_info(self):
        r = requests.get("https://investmint.ru/{0}/".format(self.__tiker), headers={'User-Agent': ch})
        text = r.text
        text = text[text.find("<h2>О компании</h2>") + 19:]
        text = text[text.find("<p>") + 3:]
        text = text.replace("<strong>", "")
        text = text.replace("</strong>", "")
        text = text[:text.find("</div>") - 4]
        if text.find("<") > 0 or text.find("<") > 0:
            text = "We haven't got information"
        return text

    def Get_Multiplicators(self, names):
        if self.__country == "Russia" or self.__country == "Rus" or self.__country == "Россия":
            return self._Get_multiplicator_of_Russian_Comp(names)
        else:
            return self._Get_multiplicator_of_Abroad_Comp(names)


    def _Get_multiplicator_of_Russian_Comp(self, names):
        Multiplicator_HTML = requests.get('https://smart-lab.ru/q/{0}/f/y/MSFO'.format(self.__tiker), headers = {'User-Agent': ch } )
        Multiplicators_Dict = {}
        text = Multiplicator_HTML.text
        for i in range(len(names)):

            div = names[i].split("/")
            if text.find(div[0] + " / " + div[1]) > 0:
                Multiplicator_Value = text[text.find(div[0] + " / " + div[1]):]
            elif text.find(div[0] + "/" + div[1]) > 0:
                Multiplicator_Value = text[text.find(div[0] + "/" + div[1]):]
            else:
                Multiplicators_Dict.update({names[i]: "There is no such multiplicator"})
                continue
            Multiplicator_Value = Multiplicator_Value[str(Multiplicator_Value).find("ltm_spc"):]
            Multiplicator_Value = Multiplicator_Value[str(Multiplicator_Value).find("<td>") + 4:]
            Multiplicator_Value = str(Multiplicator_Value[:str(Multiplicator_Value).find("</td>")]).split()
            Value = ""
            for j in range(len(Multiplicator_Value)):
                Value = Value + Multiplicator_Value[j]
            Multiplicators_Dict.update({names[i]: Value})
        return Multiplicators_Dict



    def _Get_multiplicator_of_Abroad_Comp(self, names):
        Multiplicator_HTML = requests.get('https://finbull.ru/stock/{0}/'.format(self.__tiker), headers = {'User-Agent': ch } )
        Multiplicators_Dict = {}
        text = Multiplicator_HTML.text
        for i in range(len(names)):
            div = names[i].split("/")
            if text.find(div[0] + " / " + div[1]) > 0:
                Multiplicator_Value = text[text.find(div[0] + " / " + div[1]):]
            elif text.find(div[0] + "/" + div[1]) > 0:
                Multiplicator_Value = text[text.find(div[0] + "/" + div[1]):]
            else:
                Multiplicators_Dict.update({names[i]: "There is no such multiplicator"})
                continue
            Multiplicator_Value = Multiplicator_Value[Multiplicator_Value.find("<td"):]
            Multiplicator_Value = Multiplicator_Value[Multiplicator_Value.find(">") + 1:Multiplicator_Value.find("</")].split()
            Value = ""
            for j in range(len(Multiplicator_Value)):
                Value = Value + Multiplicator_Value[j]
            Multiplicators_Dict.update({names[i]: Value})

        return Multiplicators_Dict

    def Get_Company_Stocks_Grafic(self, date, Grafic_or_Arrays):
        STOСKS_JSON = requests.get('https://api.bcs.ru/udfdatafeed/v1/history?symbol={0}&resolution=D&from={1}&to={2}'.format(self.__tiker, date[0],date[1]), headers = {'User-Agent': ch } )
        Stoсks_Dict = json.loads(STOСKS_JSON.text)
        if Stoсks_Dict.get("errmsg") is None:
            Time_Array = Stoсks_Dict.get("t")
            Time_Array = [datetime.utcfromtimestamp(e) for e in Time_Array]
            Price_Array = Stoсks_Dict.get("c")
        else:
            print("There is no such tiker or date period")
            return [0], [0]
        if Grafic_or_Arrays == "Grafic":
            fig = plt.figure(figsize=(20, 9))
            plt.plot(Time_Array, Price_Array, color="coral")
            plt.show()
            fig.savefig(self.__tiker)
        elif Grafic_or_Arrays == "Arrays":
            return Time_Array, Price_Array
        else:
            print("This function can take only two values of Grafic_or_Arrays: Grafic or Arrays")
            return

    def Compare_Grafic_Of_To_Companies(self, other, date):
        selfTime_Array, selfPrice_Array = self.Get_Company_Stocks_Grafic(date, "Arrays");
        otherTime_Array, otherPrice_Array = other.Get_Company_Stocks_Grafic(date, "Arrays");
        fig = plt.figure(figsize=(20, 9))
        plt.plot(selfTime_Array, selfPrice_Array, color="coral")
        plt.plot(otherTime_Array, otherPrice_Array, color="blue")
        plt.show()
        fig.savefig(self.__tiker + "_" + other.__tiker)

    def parsing_divd(self):
        r = requests.get("https://investmint.ru/{0}/".format(self.__tiker), headers={'User-Agent': ch})
        text = r.text
        # print(text)
        text = text[text.find("История дивидендов") + 100:]
        text = text[text.find("История дивидендов"):]
        text = text[text.find("<table"):text.find("</table>") + 8]
        # text = text[text.find("<table"):]
        # print(text)
        pdfkit.from_string('<html><head><meta charset="utf-8"></head><body><h1>Таблица Дивидендов {0}</h>{1}</body></html>'.format(self.__tiker, text), "Otchet_{0}.pdf".format(self.__tiker))


date = ["1600000000", "1618317179"]

tiker1 = "FIVE"
tiker2 = "T"

names = ["P/E","P/S","EV/EBITDA", "HUI/432"]

Comp1 = Company(tiker1, "Russia")
Comp2 = Company(tiker2, "USA")

Comp1.Get_Company_Stocks_Grafic(date, "Grafic")
Comp2.Get_Company_Stocks_Grafic(date, "Grafic")

# Пока что это песпонтово, тк хз, как сравнивать,
# если у одних график в баксах, а у другиз в рублях
Comp1.Compare_Grafic_Of_To_Companies(Comp2, date)
print(tiker1 + "   "  + str(Comp1.Get_Multiplicators(names)))
print(tiker2 + "   "  + str(Comp2.Get_Multiplicators(names)))

Comp1.parsing_divd()
print(Comp1.get_info())


