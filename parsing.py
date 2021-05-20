import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from datetime import datetime
from fake_useragent import UserAgent
ch = UserAgent().chrome


def parse_information(tiker: str) -> str:
    text = ""
    try:
        r = requests.get("https://investmint.ru/{0}/".format(tiker), headers={'User-Agent': ch})
        text = r.text
        text = text[text.find("<h2>О компании</h2>") + 19:]
        text = text[text.find("<p>") + 3:]
        text = text.replace("<strong>", "")
        text = text.replace("</strong>", "")
        text = text[:text.find("</div>") - 4]
        if text.find("<") > 0 or text.find("<") > 0:
            text = "We havent got information"
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        text = ""
    finally:
        return text


def parse_graphics_data(tiker: str, date):
    Price_Array, Time_Array = [0], [0]
    try:
        STOСKS_JSON = requests.get(
            'https://api.bcs.ru/udfdatafeed/v1/history?symbol={0}&resolution=D&from={1}&to={2}'.format(tiker,
                                                                                                       date[0],
                                                                                                       date[1]),
            headers={'User-Agent': ch})
        Stoсks_Dict = json.loads(STOСKS_JSON.text)
        if Stoсks_Dict.get("errmsg") is None:
            Time_Array = Stoсks_Dict.get("t")
            Time_Array = [datetime.utcfromtimestamp(e) for e in Time_Array]
            Price_Array = Stoсks_Dict.get("c")
            return Price_Array, Time_Array
        else:
            print("There is no such tiker or date period")
            return [0], [0]
    except:
        print("Request error", STOСKS_JSON.status_code)
    finally:
        return Price_Array, Time_Array



def parse_multiplicators(tiker: str,country: str,names) -> dict:
    if country == "Russia" or country == "Rus" or country == "Россия":
        return parse_multiplicators_for_russian_company(tiker, names)
    else:
        return parse_multiplicators_for_abroad_company(tiker, names)


def parse_multiplicators_for_russian_company(tiker, names) -> dict:
    Multiplicators_Dict = {}
    try:
        Multiplicator_HTML = requests.get('https://smart-lab.ru/q/{0}/f/y/MSFO'.format(tiker),
                                          headers={'User-Agent': ch})
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
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        Multiplicators_Dict = {"No": 0}
    finally:
        return Multiplicators_Dict


def parse_multiplicators_for_abroad_company(tiker: str, names) -> dict:
    Multiplicators_Dict = {}
    try:
        Multiplicator_HTML = requests.get('https://finbull.ru/stock/{0}/'.format(tiker),
                                          headers={'User-Agent': ch})
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
            Multiplicator_Value = Multiplicator_Value[
                                  Multiplicator_Value.find(">") + 1:Multiplicator_Value.find("</")].split()
            Value = ""
            for j in range(len(Multiplicator_Value)):
                Value = Value + Multiplicator_Value[j]
            Multiplicators_Dict.update({names[i]: Value})
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        Multiplicators_Dict = {"No": 0}
    finally:
        return Multiplicators_Dict


def parse_price(tiker: str) -> str:
    text = ""
    try:
        r = requests.get("https://investmint.ru/{0}/".format(tiker), headers={'User-Agent': ch})
        text = r.text
        text = text[text.find("Курс акций") + 10:text.find("Курс акций") + 200]
        text = text[text.find("num150 me-2") + 13:text.find("num150 me-2") + 18]
        if text.find("<") > 0 or text.find("<") > 0:
            text = "We haven't got information"
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
    finally:
        return text

if __name__ == "__main__":
    date = ["1600000000", "1620000000"]

    print(parse_price("FIVE"))
    print(parse_multiplicators("FIVE", "Rus", ["P/E"]))
    print(parse_information("FIVE"))
    print(parse_graphics_data("T", date))

# def parse_dividens():
#     pass

