# Эта область является интерфейсом вызывающимся при создании из вне объекта класса компания и нужны
# для того чтобы при каждой новой инециализации компания добавлялась в БД
import CompaniesClass
import DataBase

def get_company(tiker, country):
    if DataBase.db_company_is_in_base(tiker):
        company_as_dict = DataBase.db_get_company(tiker)
        if company_as_dict["info"] == "We haven't got information" or not company_as_dict["info"]:
            info = CompaniesClass.parsing.parse_information(tiker)
            if info:
                DataBase.db_update_company_info(tiker, info)
        new_company = CompaniesClass.Company(company_as_dict["tiker"], company_as_dict["country"], company_as_dict["fullname"], company_as_dict["info"])
    else:
        info = CompaniesClass.parsing.parse_information(tiker)
        new_company = CompaniesClass.Company(tiker, country, "", info)
        DataBase.db_add_company(new_company.get_tiker(), new_company.get_country(), new_company.get_fullname(), new_company.get_info())
    return new_company



if __name__ == "__main__":
    #print(DataBase.db_find_company_tiker_by_name("bum"))
    arr = [['Qiwi', 'X5 Retail Group', 'Акрон', 'Алроса', 'Аэрофлот', 'Башнефть', 'БСПб', 'ВСМПО-АВИСМА', 'ВТБ', 'Газпром', 'Газпром нефть', 'Группа ПИК', 'Детский мир', 'Интер РАО ЕЭС', 'Лента', 'Ленэнерго', 'ЛСР', 'Лукойл', 'М.Видео', 'Магнит', 'МГТС', 'Мечел', 'МКБ', 'ММК', 'Мосбиржа', 'Мосэнерго', 'МОЭСК', 'МРСК Волги', 'МРСК Урала', 'МРСК Центра', 'МРСК Центра и Приволжья', 'МТС', 'НКНХ', 'НЛМК', 'НМТП', 'Новатэк', 'Норникель', 'ОГК-2', 'Полиметалл', 'Полюс', 'Распадская', 'Роснефть', 'Россети', 'Ростелеком', 'Русагро', 'Русал', 'Русгидро', 'РуссНефть', 'Сафмар', 'Сбербанк', 'Северсталь', 'Система', 'Сургутнефтегаз', 'Татнефть', 'TCS Group (Тинькофф)', 'ТГК-1', 'ТМК', 'Транснефть', 'Фосагро', 'ФСК', 'Черкизово', 'Энел', 'Юнипро', 'Яндекс', 'Mail.ru Group', 'Petropavlovsk', 'Совкомфлот', 'HeadHunter', 'Эн+ Груп', 'Русская Аквакультура', 'Globaltrans', 'ГК Самолет', 'O&#039;KEY Group', 'MD Medical Group', 'Ozon', ''], ['QIWI', 'FIVE', 'AKRN', 'ALRS', 'AFLT', 'BANE, BANEР', 'BSPB', 'VSMO', 'VTBR', 'GAZP', 'SIBN', 'PIKK', 'DSKY', 'IRAO', 'LNTA', 'LSNG, LSNGР', 'LSRG', 'LKOH', 'MVID', 'MGNT', 'MGTS, MGTSР', 'MTLR, MTLRР', 'CBOM', 'MAGN', 'MOEX', 'MSNG', 'MSRS', 'MRKV', 'MRKU', 'MRKC', 'MRKP', 'MTSS', 'NKNC, NKNCР', 'NLMK', 'NMTP', 'NVTK', 'GMKN', 'OGKB', 'POLY', 'PLZL', 'RASP', 'ROSN', 'RSTI, RSTIР', 'RTKM, RTKMР', 'AGRO', 'RUAL', 'HYDR', 'RNFT', 'SFIN', 'SBER, SBERP', 'CHMF', 'AFKS', 'SNGS, SNGSР', 'TATN, TATNР', 'TCSG', 'TGKA', 'TRMK', 'TRNFP', 'PHOR', 'FEES', 'GCHE', 'ENRU', 'UPRO', 'YNDX', 'MAIL', 'POGR', 'FLOT', 'HHRU', 'ENPG', 'AQUA', 'GLTR', 'SMLT', 'OKEY', 'MDMG', 'OZON']]
    for i in range(len(arr[1])):
        if arr[1][i].find(",") > 0:
            arr[1][i] = arr[1][i].split(",")[0]
        Comp = get_company(arr[1][i], "Rus")
        DataBase.db_set_company_full_name(arr[1][i], arr[0][i])
    # Comp = get_company("PM", "Abroad")
    # DataBase.db_set_company_full_name("PM", "Philip Morris")
    # Comp = get_company("IBM", "Abroad")
    # DataBase.db_set_company_full_name("IBM", "IBM")
    # Comp = get_company("AAPL", "Abroad")
    # DataBase.db_set_company_full_name("AAPL", "Apple")
    # Comp = get_company("ACH", "Abroad")
    # DataBase.db_set_company_full_name("ACH", "Aluminum Corp")
    # Comp = get_company("GMKN", "Rus")
    # DataBase.db_set_company_full_name("GMKN", "ГМК Норникель")
    # Comp = get_company("BABA", "Abroad")
    # DataBase.db_set_company_full_name("BABA", "Alibaba")
    # Comp = get_company("GOOG", "Abroad")
    # DataBase.db_set_company_full_name("GOOG", "Alphabet")
    # Comp = get_company("AMZN", "Abroad")
    # DataBase.db_set_company_full_name("AMZN", "Amazon")
    # Comp = get_company("RACE", "Abroad")
    # DataBase.db_set_company_full_name("RACE", "Ferrari")
    # Comp = get_company("KO", "Abroad")
    # DataBase.db_set_company_full_name("KO", "Coca-Cola")




    # date = ["1600000000", "1618317179"]
    # print(Comp.get_info())
    # print(Comp.get_tiker())
    # print(Comp.get_country())
    # print(Comp.get_fullname())
    # print(Comp.get_price())
    # print(Comp.get_multiplicators(["P/E"]))
    # print(Comp.get_company_stocks_graphic(date, "Grafic"))
