import telebot
bot = telebot.TeleBot('1511883890:AAEpsssr89lPTWhibSZYIpULtkQtd6BN5a4')

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Я бот. Приятно познакомиться, {message.from_user.first_name}')
    
@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, 'Привет!')
    else:
        bot.send_message(message.from_user.id, 'Я не понимаю вас')
        
bot.polling(none_stop = True)

print(' ')