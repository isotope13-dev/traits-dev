import telebot
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['document'])
def echo(message):
    content = bot.download_file(bot.get_file(message.document.file_id).file_path)
    bot.send_document(message.chat.id, content)
