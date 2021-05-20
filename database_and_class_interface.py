import os
import CompaniesClass
import DataBase

def get_company(tiker, country):
    if DataBase.db_company_is_in_base(tiker):
        company_as_dict = DataBase.db_get_company(tiker)
        if not company_as_dict["info"]:
            info = CompaniesClass.parsing.parse_information(tiker)
            if info:
                # DataBase.db_delete_company_by_tiker(tiker)
                # DataBase.db_add_company(company_as_dict["tiker"], company_as_dict["country"], company_as_dict["fullname"], info)
                DataBase.db_update_company_info(tiker, info)
        new_company = CompaniesClass.Company(company_as_dict["tiker"], company_as_dict["country"], company_as_dict["fullname"], company_as_dict["info"])
    else:
        new_company = CompaniesClass.Company(tiker, country)
        DataBase.db_add_company(new_company.get_tiker(), new_company.get_country(), new_company.get_fullname(), new_company.get_info())
    return new_company

if __name__ == "__main__":
    Comp = get_company("IRAO", "Rus")
