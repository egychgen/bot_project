from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


import os
import time

from settings import TG_TOKEN
from CompaniesClass import Company

"""Глобальные переменные для корректной работы с методами класса Company"""

company_info = [None, None]
company_info_to_compare = [None, None]
company = None
company_to_compare = None
date = []
plot_name = None

"""Набор функций для ведения диалога с пользователем"""


def first_message(bot, update):
    bot.message.reply_text('Здравствуйте, уважаемый {}! \nДля ознакомления с функционалом бота введите команду \info. '
                           'Какую информацию вы хотите узнать?'.format(bot.message.chat.first_name),
                           reply_markup=get_keyboard(0))


def info_command(bot, update):
    bot.message.reply.text('Put text here')


def get_keyboard(x):
    yes_no_keyboard = ReplyKeyboardMarkup([['Да'], ['Нет']], resize_keyboard=True, one_time_keyboard=True)
    info_keyboard = ReplyKeyboardMarkup(
        [['Курс валют'], ['Данные о компании'], ['Основные понятия, которые вам пригодятся']],
        resize_keyboard=True, one_time_keyboard=True)
    company_keyboard = ReplyKeyboardMarkup(
        [['Мультипликатор'], ['График стоимости компании'], ['Информация о компании'],
         ['Стоимость компании']], resize_keyboard=True, one_time_keyboard=True)
    if x == 0:
        return info_keyboard
    elif x == 1:
        return yes_no_keyboard
    elif x == 2:
        return company_keyboard


"""Функции для сбора информации о комапнии"""


def company_name_func(bot, update):
    global company_info
    bot.message.reply_text('Введите тикер компании')
    return 'company_name'


def company_country_func(bot, update):
    global company_info, company
    bot.message.reply_text('Введите страну регистрации компании')
    company_info[0] = bot.message.text
    return 'company_country'


def info_about_company(bot, update):
    global company, company_info
    bot.message.reply_text('Выберите информацию, которую вы хотите узнать', reply_markup=get_keyboard(2))
    company_info[1] = bot.message.text
    company = Company(company_info[0], company_info[1])
    print('company =', company_info)
    return 'company_info'


"""Функции для работы с мультипликаторами"""


def multiplicators_names(bot, update):
    bot.message.reply_text('Введите названия интересующих вас мультипликаторов через пробел в формате Name/Name')
    return 'multiplicators_names'


def multiplicators(bot, update):
    global company
    names = bot.message.text.split()
    mult = company.Get_Multiplicators(names)
    line = str()
    for key, value in mult.items():
        line = line + key + ' : ' + value + ' ; '
    bot.message.reply_text(line)
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


"""Функции для работы с графиком 1 компаний"""


def plot_start_date(bot, update):
    bot.message.reply_text('Введите дату в формате DD.MM.YYYY, с которой хотите начать отслеживание стоимости компании')
    return 'plot_start_date'


def plot_end_date(bot, update):
    global date
    dmy = bot.message.text.split('.')
    date = date + [
        str(time.mktime(time.struct_time((int(dmy[2]), int(dmy[1]), int(dmy[0]), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    bot.message.reply_text(
        'Введите дату в формате DD.MM.YYYY, на которой хотите закончить отслеживание стоимости компании')
    return 'plot_end_date'


def get_plot(bot, update):
    global company, date, plot_name
    dmy = bot.message.text.split('.')
    date = date + [
        str(time.mktime(time.struct_time((int(dmy[2]), int(dmy[1]), int(dmy[0]), 0, 0, 0, 0, 0, 0)))).split('.')[0]]
    # print('time.struct_time =', time.struct_time((int(dmy[2]), int(dmy[1]), int(dmy[0]), 0, 0, 0, 0, 0, 0)))
    # print('date in first =', date)
    company.Get_Company_Stocks_Grafic(date, "Grafic")
    plot_name = company.get_tiker() + '.png'
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(plot_name, 'rb'))
    bot.message.reply_text('Хотите сравнить график стоимости с другой компанией?', reply_markup=get_keyboard(1))
    return 'get_plot'


"""Функции для работы с графиком 2 компаний"""


def company_name_to_compare_func(bot, update):
    global company_info_to_compare
    bot.message.reply_text('Введите тикер компании')
    return 'company_name_to_compare'


def company_country_to_compare_func(bot, update):
    global company_info_to_compare, company_to_compare
    company_info_to_compare[0] = bot.message.text
    bot.message.reply_text('Введите страну регистрации компании')
    return 'company_country_to_compare'


def send_comparing_plot(bot, update):
    global company_to_compare, date, company
    company_info_to_compare[1] = bot.message.text
    company_to_compare = Company(company_info_to_compare[0], company_info_to_compare[1])
    company_to_compare.Compare_Grafic_Of_To_Companies(company_to_compare, date)
    plot_name = company_to_compare.get_tiker() + '_' + company_to_compare.get_tiker() + '.png'
    update.bot.send_photo(chat_id=bot.message.chat.id, photo=open(plot_name, 'rb'))
    return 'send_comparing_plot'


""""""


def follow_question(bot, update):
    bot.message.reply_text('Хотите ещё что-либо узнать?', reply_markup=get_keyboard(1))
    return 'follow_question'


def goodbye(bot, update):
    bot.message.reply_text('До свидания, {}!'.format(bot.message.chat.first_name))
    for file in os.listdir():
        if file.split('.')[1] == 'png':
            os.remove(file)
    return 'goodbye'

def main():
    my_bot = Updater(TG_TOKEN, use_context=True)
    my_bot.dispatcher.add_handler(CommandHandler('start', first_message))
    my_bot.dispatcher.add_handler(CommandHandler('info', info_command))
    my_bot.dispatcher.add_handler(
        ConversationHandler(entry_points=[MessageHandler(Filters.regex('Данные о компании'), company_name_func)],
                            states={'company_name': [MessageHandler(Filters.text, company_country_func)],
                                    'company_country': [MessageHandler(Filters.text, info_about_company)],
                                    'company_info': [
                                        MessageHandler(Filters.regex('Мультипликатор'), multiplicators_names),
                                        MessageHandler(Filters.regex('График стоимости компании'), plot_start_date)],
                                    'multiplicators_names': [MessageHandler(Filters.text, multiplicators)],
                                    'plot_start_date': [MessageHandler(Filters.text, plot_end_date)],
                                    'plot_end_date': [MessageHandler(Filters.text, get_plot)],
                                    'get_plot': [MessageHandler(Filters.regex('Да'), company_name_to_compare_func),
                                                 MessageHandler(Filters.regex('Нет'), follow_question)],
                                    'company_name_to_compare': [MessageHandler(Filters.text,
                                                                               company_country_to_compare_func)],
                                    'company_country_to_compare': [MessageHandler(Filters.text, send_comparing_plot)],
                                    'follow_question': [MessageHandler(Filters.regex('Нет'), goodbye),
                                                        MessageHandler(Filters.regex('Да'), company_name_func)]
                                    },
                            fallbacks=[])
    )
    my_bot.start_polling()
    my_bot.idle()


main()

