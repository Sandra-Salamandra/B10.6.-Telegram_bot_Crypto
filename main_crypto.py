import telebot

from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Приветствую!) \n' \
           '\nЧтобы начать работу, введите команду через пробел в следующем формате:' \
           '\n<Валюта> <В какую валюту перевести> <Сколько>' \
           '\n' \
           '\nЧтобы увидеть доступные валюты, введите /values.'
    bot.send_message(message.chat.id, text)  # прикрепляет к ответу сообщение, на которое отвечает

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Введите команду через пробел в следующем формате:' \
           '\n<Валюта> <В какую валюту перевести> <Сколько>.' \
           '\n' \
           '\nЧтобы увидеть доступные валюты, введите /values.'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверно введены параметры.\n/help')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода.\n{e}')
    except Exception as e:
        bot.reply_to(message, 'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} "{base}" в валюте "{quote}" = {total_base}'
        bot.reply_to(message, text)


bot.polling()