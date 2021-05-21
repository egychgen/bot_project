# Эта область является интерфейсом вызывающимся при создании из вне объекта класса компания и нужны
# для того чтобы при каждой новой инициализации компания добавлялась в БД
import CompaniesClass
import DataBase

# Данная функция принимает данные у пользовательствого интерфейса(бота) и отправляет полученные данные в БД,
# а обратно в область телеграмм бота отправляет объект класса Company  методами которого умеет пользовать бот
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



