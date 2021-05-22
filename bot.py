from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup

import os
import time

import DataBase
import parsing
from CompaniesClass import Company
from database_and_class_interface import get_company
from settings import TG_TOKEN

"""Глобальные переменные для корректной работы с методами класса Company"""

company_info = [None, None, None]
company_info_to_compare = [None, None, None]
company = None
company_to_compare = None
date = []
plot_name = None

"""Набор команд"""


def start_command(bot, update):
    bot.message.reply_text('Здравствуйте, {}! \nДля ознакомления с функционалом бота введите команду /info. '
                           'Какую информацию вы хотите узнать?'.format(bot.message.chat.first_name),
                           reply_markup=get_keyboard(0))


def info_command(bot, update):
    bot.message.reply_text('Наш бот умеет находить некоторую информацию об интересующей вас компании,'
                           'a именно строить графики стоимости акций компании в течение интересующего вас '
                           'периода времени, выдавать текущию стоимость компании, общую информацию о компании '
                           'и значние различных мультипликаторов. База данных со стоимостью акций компаний обновляется '
                           'раз в день, поэтому просим вас при построении графиков рассматривать стоимость на '
                           'промежутке времени не меньше месяца! Если вы хотите разобраться с основными понятиями,'
                           'необходимых для работы с ботом, воспользуйтесь командой \n /knowledge. Для работы с ботом '
                           'используйте команду /start')


def knowledge_command(bot, update):
    bot.message.reply_text('Тикер — это краткое название актива на бирже. '
                           'Как правило, тикер представляет собой сочетание '
                           'из нескольких латинских символов. Это сочетание '
                           'является уникальным на отдельно взятой бирже и '
                           'закреплено за конкретной акцией или другим биржевым '
                           'инструментом. Чаще всего слово тикер применяется именно '
                           'по отношению к акциям, в то время как коды других '
                           'инструментов чаще называются просто кодом инструмента')

    bot.message.reply_text('Мультипликаторы — это производные финансовые показатели. '
                           'Инвесторы считают мультипликаторы, чтобы понять: акция '
                           'компании переоценена, недооценена или соответствует своей цене.\n'
                           'Виды мультпликаторов:\n'
                           'ROE = чистая прибыль/капитал * 100 \n'
                           'ROA = чистая прибыль/активы компании * 100 \n'
                           'D/E = заемный капитал / собственный капитал \n'
                           'P/E = цена акции / прибыль на акцию \n'
                           'P/S = капитализация / годовая выручка \n'
                           'EV/EBITDA = (рыночная капитализация + долговые обязательства - денежные средства компании) / (прибыль до выплаты процентов, налогов и амортизации)')


def stop_command(bot, update):
    global company_info, company_info_to_compare, company, company_to_compare, date, plot_name
    bot.message.reply_text('До свидания, {}!'.format(bot.message.chat.first_name))
    company_info = [None, None, None]
    company_info_to_compare = [None, None, None]
    company = None
    company_to_compare = None
    date = []
    plot_name = None
    return ConversationHandler.END


def rate_command(bot, update):
    bot.message.reply_text('Выберите валюту, курс которой хотите узнать', reply_markup=get_keyboard(4))
    return 'rate'


"""Клавиатура"""


def get_keyboard(x):
    yes_no_keyboard = ReplyKeyboardMarkup([['Да'], ['Нет']], resize_keyboard=True, one_time_keyboard=True)
    info_keyboard = ReplyKeyboardMarkup(
        [['Курс валют'], ['Данные о компании'], ['Основные понятия, которые вам пригодятся']],
        resize_keyboard=True, one_time_keyboard=True)
    company_keyboard = ReplyKeyboardMarkup(
        [['Мультипликатор', 'График стоимости компании'], ['Информация о компании', 'Стоимость компании'],
         ['Смена компании']], resize_keyboard=True, one_time_keyboard=True)
    time_keyboard = ReplyKeyboardMarkup([['1 месяц', '3 месяца'], ['6 месяцев', '9 месяцев'],
                                         ['1 год', '3 года']], resize_keyboard=True, one_time_keyboard=True)
    rate_keyboard = ReplyKeyboardMarkup([['Китайский юань', 'Доллар США', 'Евро'], ['Индийских рупий',
                                                                                    'Белорусский рубль'],
                                         ['Киргизских сомов', 'Казахстанских тенге'],
                                         ['Турецких лир']], resize_keyboard=True, one_time_keyboard=True)
    country_keyboard = ReplyKeyboardMarkup([['Rus', 'Abroad']], resize_keyboard=True, one_time_keyboard=True)
    multiplicators_keyboard = ReplyKeyboardMarkup([['ROE', 'ROA'], ['D/E', 'P/E'], ['P/S', 'EV/EBITDA']],
                                                  resize_keyboard=True, one_time_keyboard=True)
    tiker_keyboard = ReplyKeyboardMarkup([['SBER', 'GAZP', 'AAPL'], ['MSFT', 'LNTA', 'RACE'], ['Свой тикер']],
                                         resize_keyboard=True, one_time_keyboard=True)
    fullname_keyboard = ReplyKeyboardMarkup([['Сбербанк', 'Газпром', 'Apple'], ['Microsoft', 'Лента', 'Ferrari'],
                                             ['Свое название']], resize_keyboard=True, one_time_keyboard=True)
    criteria_keyboard = ReplyKeyboardMarkup([['Тикер', 'Название компании']], resize_keyboard=True,
                                            one_time_keyboard=True)

    if x == 0:
        return info_keyboard
    elif x == 1:
        return yes_no_keyboard
    elif x == 2:
        return company_keyboard
    elif x == 3:
        return time_keyboard
    elif x == 4:
        return rate_keyboard
    elif x == 5:
        return country_keyboard
    elif x == 6:
        return multiplicators_keyboard
    elif x == 7:
        return tiker_keyboard
    elif x == 8:
        return fullname_keyboard
    elif x == 9:
        return criteria_keyboard


"""Функции для сбора информации о комапнии"""


def company_criteria_func(bot, update):
    bot.message.reply_text('По какому критерию хотите искать компанию?', reply_markup=get_keyboard(9))
    return 'company_criteria'


def company_tiker_func(bot, update):
    global company_info
    bot.message.reply_text('Выберите тикер компании или введите свой', reply_markup=get_keyboard(7))
    return 'company_tiker_func'


def company_fullname_func(bot, update):
    global company_info
    bot.message.reply_text('Выберите название компании или введите свое', reply_markup=get_keyboard(8))
    return 'company_fullname_func'


def user_tiker(bot, update):
    bot.message.reply_text('Введите навзвание тикера')
    return 'user_tiker'


def user_fullname(bot, update):
    bot.message.reply_text('Введите навзвание компании')
    return 'user_fullname'


def tiker_by_fullname_func(bot, update):
    global company_info
    reply = ['have_tiker_by_fullname_func', 'company_criteria']
    fullname = bot.message.text
    tiker = DataBase.db_find_company_tiker_by_name(fullname)
    if len(tiker) != 0:
        i = 0
        bot.message.reply_text('Тикер компании: ' + tiker)
        company_info[0] = tiker
        bot.message.reply_text('Введите страну регистрации компании', reply_markup=get_keyboard(5))
    else:
        i = 1
        bot.message.reply_text('Такой компании нет в нашей базе данных. '
                               'Попробуйте найти информацию о ней при помощи тикера')
        bot.message.reply_text('По какому критерию хотите искать компанию?', reply_markup=get_keyboard(9))
    return reply[i]


def company_country_func(bot, update):
    global company_info
    bot.message.reply_text('Введите страну регистрации компании', reply_markup=get_keyboard(5))
    company_info[0] = bot.message.text
    return 'company_country'


def info_about_company(bot, update):
    global company, company_info
    bot.message.reply_text('Выберите информацию, которую вы хотите узнать', reply_markup=get_keyboard(2))
    company_info[1] = bot.message.text
    company = get_company(company_info[0], company_info[1])
    # DataBase.db_set_company_full_name(company_info[0], company_info[2])
    return 'company_info'


def get_info_about_company(bot, update):
    bot.message.reply_text('Выберите информацию, которую вы хотите узнать', reply_markup=get_keyboard(2))
    return 'company_info'


"""Смена компании"""
def change_company(bot, update):
    bot.message.reply_text('Вы точно хотите сменить компанию?', reply_markup=get_keyboard(1))
    return 'change_company'

"""Функции для работы с мультипликаторами"""


def multiplicators_names(bot, update):
    bot.message.reply_text('Выберите интерисующий вас мультипликатор', reply_markup=get_keyboard(6))
    return 'multiplicators_names'


def multiplicators(bot, update):
    global company
    multiplicator = company.get_multiplicators([bot.message.text])
    bot.message.reply_text(multiplicator)
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


"""Функции для работы с графиком 1 компаний"""


def plot_time(bot, update):
    bot.message.reply_text('Выберите промежуток времени, в течение которого хотите отследить стоимость акций компании',
                           reply_markup=get_keyboard(3))
    return 'plot_time'


def get_plot(bot, update):
    global company, date
    date_now = bot.message.date
    line = bot.message.text
    # print('line =', line)
    if line == '1 месяц':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year), int(date_now.month) - 1, int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    elif line == '3 месяца':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year), int(date_now.month) - 3, int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    elif line == '6 месяцев':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year), int(date_now.month) - 6, int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    elif line == '9 месяцев':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year), int(date_now.month) - 9, int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    elif line == '1 год':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year) - 1, int(date_now.month), int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    elif line == '3 года':
        date = date + [
            str(time.mktime(time.struct_time(
                (int(date_now.year) - 3, int(date_now.month), int(date_now.day), 0, 0, 0, 0, 0, 0)))).split('.')[0]]

    date = date + [
        str(time.mktime(
            time.struct_time((int(date_now.year), int(date_now.month), int(date_now.day), 0, 0, 0, 0, 0, 0)))).split(
            '.')[0]]

    # print('date =', date)
    company.get_company_stocks_graphic(date, "Grafic")
    plot_name = company.get_tiker() + '.png'
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(plot_name, 'rb'))
    os.remove(plot_name)
    bot.message.reply_text('Хотите сравнить график стоимости с другой компанией?', reply_markup=get_keyboard(1))
    return 'get_plot'


"""Функции для работы с графиком 2x компаний"""


def company_to_compare_criteria_func(bot, update):
    bot.message.reply_text('По какому критерию хотите искать компанию?', reply_markup=get_keyboard(9))
    return 'company_to_compare_criteria'


def company_tiker_to_compare_func(bot, update):
    bot.message.reply_text('Выберите тикер компании или введите свой', reply_markup=get_keyboard(7))
    return 'company_to_compare_tiker_func'


def company_to_compare_fullname_func(bot, update):
    bot.message.reply_text('Выберите название компании или введите свое', reply_markup=get_keyboard(8))
    return 'company_to_compare_fullname_func'


def user_tiker_compare(bot, update):
    bot.message.reply_text('Введите навзвание тикера')
    return 'user_tiker_compare'


def user_fullname_compare(bot, update):
    bot.message.reply_text('Введите навзвание компании')
    return 'user_fullname_compare'


def tiker_by_fullname_func_compare(bot, update):
    global company_info_to_compare
    reply = ['have_tiker_by_fullname_func_compare', 'company_to_compare_criteria']
    fullname = bot.message.text
    tiker = DataBase.db_find_company_tiker_by_name(fullname)
    if len(tiker) != 0:
        i = 0
        bot.message.reply_text('Тикер компании: ' + tiker)
        company_info_to_compare[0] = tiker
        bot.message.reply_text('Введите страну регистрации компании', reply_markup=get_keyboard(5))
    else:
        i = 1
        bot.message.reply_text('Такой компании нет в нашей базе данных. '
                               'Попробуйте найти информацию о ней при помощи тикера')
        bot.message.reply_text('По какому критерию хотите искать компанию?', reply_markup=get_keyboard(9))
    print('reply[i] =', reply[i])
    return reply[i]


def company_to_compare_country_func(bot, update):
    global company_info_to_compare
    bot.message.reply_text('Введите страну регистрации компании', reply_markup=get_keyboard(5))
    company_info_to_compare[0] = bot.message.text
    return 'company_country_compare'


def send_comparing_plot(bot, update):
    global company_to_compare, date, company
    company_info_to_compare[1] = bot.message.text
    company_to_compare = get_company(company_info_to_compare[0], company_info_to_compare[1])
    DataBase.db_set_company_full_name(company_info_to_compare[0], company_info_to_compare[2])
    company.compare_graphics_of_to_companies(company_to_compare, date)
    plot_name = company.get_tiker() + '_' + company_to_compare.get_tiker() + '.png'
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(plot_name, 'rb'))
    os.remove(plot_name)
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


"""Другие функции"""


def delta_func(bot, update):
    bot.message.reply_text('Выберите информацию, которую хотите узнать', reply_markup=get_keyboard(0))
    return 'delta_func'


def rate(bot, update):
    currency = bot.message.text
    # print(currency)
    # print(parsing.parse_currency_value(currency))
    bot.message.reply_text(parsing.parse_currency_value(currency))
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'rate_end'


def get_company_price(bot, update):
    global company
    bot.message.reply_text(company.get_price())
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


def get_company_info(bot, update):
    global company
    bot.message.reply_text(company.get_info())
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


def main_func(bot, update):
    bot.message.reply_text('Тикер — это краткое название актива на бирже. '
                           'Как правило, тикер представляет собой сочетание '
                           'из нескольких латинских символов. Это сочетание '
                           'является уникальным на отдельно взятой бирже и '
                           'закреплено за конкретной акцией или другим биржевым '
                           'инструментом. Чаще всего слово тикер применяется именно '
                           'по отношению к акциям, в то время как коды других '
                           'инструментов чаще называются просто кодом инструмента')

    bot.message.reply_text('Мультипликаторы — это производные финансовые показатели. '
                           'Инвесторы считают мультипликаторы, чтобы понять: акция '
                           'компании переоценена, недооценена или соответствует своей цене.\n'
                           'Виды мультпликаторов:\n'
                           'ROE = чистая прибыль/капитал * 100 \n'
                           'ROA = чистая прибыль/активы компании * 100 \n'
                           ' D/E = заемный капитал / собственный капитал \n'
                           ' P/E = цена акции / прибыль на акцию \n'
                           ' P/S = капитализация / годовая выручка \n'
                           ' EV/EBITDA = (рыночная капитализация + долговые обязательства - денежные средства компании) / (прибыль до выплаты процентов, налогов и амортизации)')

    bot.message.reply_text('Какую информацию вы хотите узнать далее?'.format(bot.message.chat.first_name),
                           reply_markup=get_keyboard(0))
    return 'main_func'


def follow_question(bot, update):
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


def goodbye(bot, update):
    global company_info, company_info_to_compare, company, company_to_compare, date, plot_name
    bot.message.reply_text('До свидания, {}!'.format(bot.message.chat.first_name))
    company_info = [None, None, None]
    company_info_to_compare = [None, None, None]
    company = None
    company_to_compare = None
    date = []
    plot_name = None
    return ConversationHandler.END


def main():
    my_bot = Updater(TG_TOKEN, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', start_command))
    my_bot.dispatcher.add_handler(CommandHandler('info', info_command))
    my_bot.dispatcher.add_handler(CommandHandler('knowledge', knowledge_command))
    my_bot.dispatcher.add_handler(CommandHandler('stop', goodbye))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Основные понятия, которые вам пригодятся'), main_func))
    my_bot.dispatcher.add_handler(ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('Курс валют'), rate_command), CommandHandler('rate', rate_command)],
        states={'rate': [MessageHandler(Filters.text, rate)],
                'rate_end': [MessageHandler(Filters.regex('Нет'), goodbye),
                             MessageHandler(Filters.regex('Да'), delta_func)]},
        fallbacks=[CommandHandler('stop', goodbye)]))
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Данные о компании'), company_criteria_func)],
                            states={'company_criteria': [MessageHandler(Filters.regex('Тикер'), company_tiker_func),
                                                         MessageHandler(Filters.regex('Название компании'),
                                                                        company_fullname_func)],
                                    'company_tiker_func': [MessageHandler(Filters.regex('Свой тикер'), user_tiker),
                                                           MessageHandler(Filters.regex('SBER'), company_country_func),
                                                           MessageHandler(Filters.regex('GAZP'), company_country_func),
                                                           MessageHandler(Filters.regex('AAPL'), company_country_func),
                                                           MessageHandler(Filters.regex('MSFT'), company_country_func),
                                                           MessageHandler(Filters.regex('LNTA'), company_country_func),
                                                           MessageHandler(Filters.regex('RACE'), company_country_func)],
                                    'company_fullname_func': [
                                        MessageHandler(Filters.regex('Свое название'), user_fullname),
                                        MessageHandler(Filters.regex('Сбербанк'), tiker_by_fullname_func),
                                        MessageHandler(Filters.regex('Газпром'), tiker_by_fullname_func),
                                        MessageHandler(Filters.regex('Apple'), tiker_by_fullname_func),
                                        MessageHandler(Filters.regex('Microsoft'), tiker_by_fullname_func),
                                        MessageHandler(Filters.regex('Лента'), tiker_by_fullname_func),
                                        MessageHandler(Filters.regex('Ferrari'), tiker_by_fullname_func)],
                                    'user_tiker': [MessageHandler(Filters.text, company_country_func)],
                                    'user_fullname': [MessageHandler(Filters.text, tiker_by_fullname_func)],
                                    'have_tiker_by_fullname_func': [MessageHandler(Filters.text, info_about_company)],
                                    'company_country': [MessageHandler(Filters.text, info_about_company)],
                                    'company_info': [
                                        MessageHandler(Filters.regex('Мультипликатор'), multiplicators_names),
                                        MessageHandler(Filters.regex('График стоимости компании'), plot_time),
                                        MessageHandler(Filters.regex('Стоимость компании'), get_company_price),
                                        MessageHandler(Filters.regex('Информация о компании'), get_company_info),
                                        MessageHandler(Filters.regex(''), change_company)],
                                    'change_company': [MessageHandler(Filters.regex('Да'), company_criteria_func),
                                                       MessageHandler(Filters.regex('Нет'), info_about_company)],
                                    'multiplicators_names': [MessageHandler(Filters.text, multiplicators)],
                                    'plot_time': [MessageHandler(Filters.text, get_plot)],
                                    'get_plot': [MessageHandler(Filters.regex('Да'), company_to_compare_criteria_func),
                                                 MessageHandler(Filters.regex('Нет'), follow_question)],
                                    'company_to_compare_criteria': [
                                        MessageHandler(Filters.regex('Тикер'), company_tiker_to_compare_func),
                                        MessageHandler(Filters.regex('Название компании'),
                                                       company_to_compare_fullname_func)],
                                    'company_to_compare_tiker_func': [MessageHandler(Filters.regex('Свой тикер'), user_tiker_compare),
                                                           MessageHandler(Filters.regex('SBER'), company_to_compare_country_func),
                                                           MessageHandler(Filters.regex('GAZP'), company_to_compare_country_func),
                                                           MessageHandler(Filters.regex('AAPL'), company_to_compare_country_func),
                                                           MessageHandler(Filters.regex('MSFT'), company_to_compare_country_func),
                                                           MessageHandler(Filters.regex('LNTA'), company_to_compare_country_func),
                                                           MessageHandler(Filters.regex('RACE'), company_to_compare_country_func)],
                                    'company_to_compare_fullname_func': [
                                        MessageHandler(Filters.regex('Свое название'), user_fullname_compare),
                                        MessageHandler(Filters.regex('Сбербанк'), tiker_by_fullname_func_compare),
                                        MessageHandler(Filters.regex('Газпром'), tiker_by_fullname_func_compare),
                                        MessageHandler(Filters.regex('Apple'), tiker_by_fullname_func_compare),
                                        MessageHandler(Filters.regex('Microsoft'), tiker_by_fullname_func_compare),
                                        MessageHandler(Filters.regex('Лента'), tiker_by_fullname_func_compare),
                                        MessageHandler(Filters.regex('Ferrari'), tiker_by_fullname_func_compare)],
                                    'user_tiker_compare': [MessageHandler(Filters.text, company_to_compare_country_func)],
                                    'user_fullname_compare': [MessageHandler(Filters.text, tiker_by_fullname_func_compare)],
                                    'have_tiker_by_fullname_func_compare': [MessageHandler(Filters.text, send_comparing_plot)],
                                    'dont_have_tiker_by_fullname_func_compare': [
                                        MessageHandler(Filters.text, company_to_compare_criteria_func)],
                                    'company_country_compare': [MessageHandler(Filters.text, send_comparing_plot)],
                                    'follow_question': [MessageHandler(Filters.regex('Нет'), goodbye),
                                                        MessageHandler(Filters.regex('Да'), get_info_about_company)],
                                    },
                            fallbacks=[CommandHandler('stop', goodbye)])
    )
    my_bot.start_polling()
    my_bot.idle()


main()
