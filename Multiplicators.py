import requests
import json
from datetime import datetime

def Get_multiplicator_of_Russian_Corp(tiker):
    Multiplicator_HTML = requests.get('https://smart-lab.ru/q/{0}/f/y/MSFO'.format(tiker))
    Text = Multiplicator_HTML.text
    Text = Text[Text.find("P/E"):]
    Text = Text[Text.find("ltm_spc"):]
    Text = Text[Text.find("<td>")+4:Text.find("<td>")+10]
    print(Text)

def Get_multiplicator_of_Abroad_Corp(tiker):
    Multiplicator_HTML = requests.get('https://finbull.ru/stock/{0}/'.format(tiker))
    Text = Multiplicator_HTML.text
    Text = Text[Text.find("P/E"):]
    Text = Text[Text.find(">")+1:]
    Text = Text[Text.find(">"):]
    # print(Text.find("<"))
    # print(Text.find(">"))
    Text = Text[Text.find(">")+1:Text.find("<")]
    print(Text)


tiker = "RACE"
Get_multiplicator_of_Abroad_Corp(tiker)
'dick'