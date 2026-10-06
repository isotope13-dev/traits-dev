"""Library example bot: demonstrates the TeleBot message-handler API with a
documentation placeholder token. Example code using the library's own API
is not evidence of a C2 bot.
See https://github.com/eternnoir/pyTelegramBotAPI for documentation.
"""
import telebot

bot = telebot.TeleBot('1234567890:AAAABBBBCCCCDDDDeeeeFFFFgggGHHHH')


@bot.message_handler(commands=['pay'])
def send_invoice(message):
    bot.send_invoice(message.chat.id, 'Demo', 'Demo goods', 'demo-payload',
                     'PROVIDER_TOKEN', 'USD', [telebot.types.LabeledPrice('x', 100)])


@bot.message_handler(func=lambda m: True)
def echo_file(message):
    bot.send_document(message.chat.id, open('demo.txt', 'rb'))


bot.infinity_polling()
