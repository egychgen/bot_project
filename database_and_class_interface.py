from CompaniesClass import Company
import DataBase

def get_company(tiker, country):
    if DataBase.db_company_is_in_base(tiker):
        company_as_dict = DataBase.db_get_company(tiker)
        new_company = Company(company_as_dict["tiker"], company_as_dict["country"], company_as_dict["fullname"], company_as_dict["information"])
    else:
        new_company = Company(tiker, country)
        DataBase.db_add_company(new_company.get_tiker(), new_company.get_country(), new_company.get_fullname(), new_company.get_info())
    return new_company

