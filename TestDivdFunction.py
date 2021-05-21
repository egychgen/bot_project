import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pdfkit

from datetime import datetime
from fake_useragent import UserAgent
ch = UserAgent().chrome


def parsing_divd(ticker):
    r = requests.get("https://investmint.ru/{0}/".format(ticker), headers = {'User-Agent': ch })
    text = r.text
    print(text)
    text = text[text.find("История дивидендов") + 100:]
    text = text[text.find("История дивидендов"):]
    text = text[text.find("<table"):text.find("</table>") + 8]
    # text = text[text.find("<table"):]
    print(text)
    pdfkit.from_string('<html><head><meta charset="utf-8"></head><body><h1>Таблица Дивидендов {0}</h>{1}</body></html>'.format(ticker, text) , "Otchet_{0}.pdf".format(ticker))


ticker = "SBER"
parsing_divd(ticker)



