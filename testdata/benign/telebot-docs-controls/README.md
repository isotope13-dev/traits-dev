
[![PyPi Package Version](https://img.shields.io/pypi/v/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/pyTelegramBotAPI)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyTelegramBotAPI.svg)](https://pypi.python.org/pypi/pyTelegramBotAPI)
[![Documentation Status](https://readthedocs.org/projects/pytba/badge/?version=latest)](https://pytba.readthedocs.io/en/latest/?badge=latest)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyTelegramBotAPI.svg)](https://pypi.org/project/pyTelegramBotAPI/)
[![PyPi status](https://img.shields.io/pypi/status/pytelegrambotapi.svg?style=flat-square)](https://pypi.python.org/pypi/pytelegrambotapi)

# <p align="center">pyTelegramBotAPI

<p align="center">A simple, but extensible Python implementation for the <a href="https://core.telegram.org/bots/api">Telegram Bot API</a>.</p>
<p align="center">Both synchronous and asynchronous.</p>

## <p align="center">Supported Bot API version: <a href="https://core.telegram.org/bots/api#august-24-2026"><img src="https://img.shields.io/badge/Bot%20API-10.3-blue?logo=telegram" alt="Supported Bot API version"></a>

<h2><a href='https://pytba.readthedocs.io/en/latest/index.html'>Official documentation</a></h2>
<h2><a href='https://pytba.readthedocs.io/ru/latest/index.html'>Official ru documentation</a></h2>
	

# DemoBot library

A Python Telegram bot library. See https://github.com/eternnoir/pyTelegramBotAPI
for full documentation.

## Quick start

```python
import telebot
bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! How are you doing?")

bot.infinity_polling()
```

## Sending files

```python
import telebot

tb = telebot.TeleBot("TOKEN")

with open('welcome.txt', 'rb') as doc:
    tb.send_document(123456, doc)
```

## Handling all messages

```python
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
```

## Polling options

```python
bot.infinity_polling(timeout=10, long_polling_timeout=5)
```
