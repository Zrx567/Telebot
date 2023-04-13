import telebot
from config import TOKEN, keys
from extensions import APIException, TET

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет ,я узнаю для тебя стоимость одной валюты к другой, \nинструкции по команде /help.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы введите команду : Валюта 1  Валюта 2  Количество\nУвидеть список валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Виды валют:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
         raise APIException('Неверное количество параметров')
        quote, base, amount = values
        total_base = TET.get_price(quote, base,amount)
    except Exception:
        bot.reply_to(message,f'что-то идет не так...')
    else:
     text = f'Стоимость {amount} {quote} в {base} = {total_base}'
     bot.send_message(message.chat.id, text)
bot.polling()
