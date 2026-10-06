"""Library test suite: exercises the TeleBot handler and polling API with a
mocked transport. Test code using the library's own API is not evidence of
a C2 bot. Upstream: https://github.com/eternnoir/pyTelegramBotAPI."""
import os
import telebot
from unittest import mock

TOKEN = os.environ.get('BOT_TOKEN', '1234567890:TESTTESTTESTTESTTESTTESTTEST01')


def test_handler_dispatch():
    bot = telebot.TeleBot(TOKEN)
    seen = []

    @bot.message_handler(commands=['start'])
    def start(message):
        seen.append(message)
        bot.send_document(message.chat.id, open('fixture.txt', 'rb'))

    with mock.patch.object(bot, 'send_document') as sender:
        start(mock.Mock(chat=mock.Mock(id=1)))
    assert sender.called


def test_polling_loop():
    bot = telebot.TeleBot(TOKEN)
    with mock.patch.object(bot, 'infinity_polling') as poll:
        bot.infinity_polling()
    assert poll.called
