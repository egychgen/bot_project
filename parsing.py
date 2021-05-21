import requests
import json
from datetime import datetime
from fake_useragent import UserAgent
ch = UserAgent().safari

# Область работы с внешними данными
# Функции из данной области используются в методах класса Company
# Данные беруться с сайтов:
# https://investmint.ru/
# https://api.bcs.ru/
# https://smart-lab.ru/
# http://www.cbr.ru/
# https://finsovetnik.com/
#
#
#
#
def parse_information(tiker: str) -> str:
    text = ""
    try:
        r = requests.get("https://investmint.ru/{0}/".format(tiker), headers={'User-Agent': ch})
        text = r.text
        text = text[text.find("<h2>О компании</h2>") :]
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
    price_array, time_array = [0], [0]
    try:
        stoсks_json = requests.get(
            'https://api.bcs.ru/udfdatafeed/v1/history?symbol={0}&resolution=D&from={1}&to={2}'.format(tiker,
                                                                                                       date[0],
                                                                                                       date[1]),
            headers={'User-Agent': ch})
        stoсks_dict = json.loads(stoсks_json.text)
        if stoсks_dict.get("errmsg") is None:
            time_array = stoсks_dict.get("t")
            time_array = [datetime.utcfromtimestamp(e) for e in time_array]
            price_array = stoсks_dict.get("c")
            return price_array, time_array
        else:
            print("There is no such tiker or date period")
            return [0], [0]
    except:
        print("Request error", stoсks_json.status_code)
    finally:
        return price_array, time_array



def parse_multiplicators(tiker: str,country: str,names) -> dict:
    if country == "Russia" or country == "Rus" or country == "Россия":
        return parse_multiplicators_for_russian_company(tiker, names)
    else:
        return parse_multiplicators_for_abroad_company(tiker, names)


def parse_multiplicators_for_russian_company(tiker, names) -> dict:
    multiplicators_dict = {}
    try:
        multiplicator_html = requests.get('https://smart-lab.ru/q/{0}/f/y/MSFO'.format(tiker),
                                          headers={'User-Agent': ch})
        text = multiplicator_html.text
        for i in range(len(names)):

            div = names[i].split("/")
            if text.find(div[0] + " / " + div[1]) > 0:
                multiplicator_value = text[text.find(div[0] + " / " + div[1]):]
            elif text.find(div[0] + "/" + div[1]) > 0:
                multiplicator_value = text[text.find(div[0] + "/" + div[1]):]
            else:
                multiplicators_dict.update({names[i]: "There is no such multiplicator"})
                continue
            multiplicator_value = multiplicator_value[str(multiplicator_value).find("ltm_spc"):]
            multiplicator_value = multiplicator_value[str(multiplicator_value).find("<td>") + 4:]
            multiplicator_value = str(multiplicator_value[:str(multiplicator_value).find("</td>")]).split()
            Value = ""
            for j in range(len(multiplicator_value)):
                Value = Value + multiplicator_value[j]
                multiplicators_dict.update({names[i]: Value})
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        multiplicators_dict = {"No": 0}
    finally:
        return multiplicators_dict


def parse_multiplicators_for_abroad_company(tiker: str, names) -> dict:
    multiplicators_dict = {}
    try:
        multiplicator_html = requests.get('https://finbull.ru/stock/{0}/'.format(tiker),
                                          headers={'User-Agent': ch})
        text = multiplicator_html.text
        for i in range(len(names)):
            div = names[i].split("/")
            if text.find(div[0] + " / " + div[1]) > 0:
                multiplicator_value = text[text.find(div[0] + " / " + div[1]):]
            elif text.find(div[0] + "/" + div[1]) > 0:
                multiplicator_value = text[text.find(div[0] + "/" + div[1]):]
            else:
                multiplicators_dict.update({names[i]: "There is no such multiplicator"})
                continue
            multiplicator_value = multiplicator_value[multiplicator_value.find("<td"):]
            multiplicator_value = multiplicator_value[
                                  multiplicator_value.find(">") + 1:multiplicator_value.find("</")].split()
            Value = ""
            for j in range(len(multiplicator_value)):
                Value = Value + multiplicator_value[j]
            multiplicators_dict.update({names[i]: Value})
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        multiplicators_dict = {"No": 0}
    finally:
        return multiplicators_dict


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

def parse_Central_Bank_to_get_currecy(currency_name):
    text = ""
    try:
        r = requests.get("http://www.cbr.ru/scripts/XML_daily.asp?")
        text = r.text
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        text = "We haven't got information"
    finally:
        return text

def parse_currency_value(currency_name):
    text = parse_Central_Bank_to_get_currecy(currency_name)
    if text != "We haven't got information":
        text = text[text.find(currency_name):]
        text = text[text.find("Value") + 6:text.find("</Value>")]
    return text

def parse_currency_value_for_graphics(currency_name):
    text = parse_Central_Bank_to_get_currecy(currency_name)
    if text != "We haven't got information":
        text = text[text.find(currency_name):]
        text = text[text.find("Value") + 6:text.find("</Value>")]
    text = text[:text.find(",")]
    return int(text)

def parse_company_tiker_by_name(fullname):
    text = ""
    try:
        r = requests.get("https://finsovetnik.com/rf/")
        text = r.text
        text = text[text.find(fullname):]
        text = text[text.find("even")+6:]
        text = text[:text.find("</td")]
        print(text)
    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        text = "We haven't got information"
    finally:
        return text

def parse_companies_names_tikers_categories():
    arr = [[],[]]
    try:
        r = requests.get("https://finsovetnik.com/rf/")
        maintext = r.text
        maintext = maintext[maintext.find("ETLN"):]
        maintext = maintext[maintext.find("href")+3:]
        while len(arr[0]) < 76:
            nametext = maintext[maintext.find(">")+1:maintext.find("<")]
            tikertext = maintext[maintext.find("even")+6:]
            tikertext = tikertext[:tikertext.find("</td")]
            maintext = maintext[maintext.find("</tr>"):]
            maintext = maintext[maintext.find("href")+3:]
        # print(maintext)
            arr[0].append(nametext)
            arr[1].append(tikertext)
        return arr


    except requests.exceptions.HTTPError as error:
        print("Request error", error.response.status_code)
        text = "We haven't got information"
    finally:
        # return text
        pass



if __name__ == "__main__":
    # date = ["1600000000", "1620000000"]
    #
    # print(parse_price("FIVE"))
    # print(parse_multiplicators("FIVE", "Rus", ["P/E"]))
    # print(parse_information("FIVE"))
    # print(parse_graphics_data("T", date))
    # print(int(parse_currency_value_for_graphics("USD")))
    print(parse_information("FIVE"))
    # def parse_dividens():
    #       pass

