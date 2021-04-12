import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

# class Stoks_price(object):
#     def __init__(self, price, time):
#         self.price = price
#         self.time = time

def Stocks_Grafic(Time_Array, Price_Array,tiker):
    fig = plt.figure(figsize=(20,9))
    # for i in range(len(Time_Array)):
    #     Time_Array[i] = datetime.utcfromtimestamp(Time_Array[i]).strftime('%Y-%m-%d %H:%M:%S')
    plt.plot(Time_Array, Price_Array, color="coral")
    plt.show()
    fig.savefig(tiker)



def BCS_JSON_Parcing(tiker):
    STOСKS_JSON = requests.get('https://api.bcs.ru/udfdatafeed/v1/history?symbol={0}&resolution=D&from=672325461&to=1605445521'.format(tiker))
    Stoсks_Dict = json.loads(STOСKS_JSON.text)
    if Stoсks_Dict.get("errmsg") is None:
        Time_Array = Stoсks_Dict.get("t")
        Price_Array = Stoсks_Dict.get("c")
    Stocks_Grafic(Time_Array, Price_Array,tiker)
    return STOСKS_JSON.text

# def Stoсks_JSON_to_array(Stoks_JSON):
#     Stoсks_Dict = json.loads(Stoks_JSON)
#     Time_Array = Stoсks_Dict.get("errmsg")
#     print(Time_Array)
#     # Price_Array =
#     return Stoсks_Dict

tiker = "GAZP"
Stoks_JSON = BCS_JSON_Parcing(tiker)
# arr = Stoсks_JSON_to_array(Stoks_JSON)
# print(arr.keys())
# ts = int("1171918800")
# today = datetime.today()
# print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# # print(BCS_JSON_Parcing(tiker))
# print(datetime.timestamp(today))
