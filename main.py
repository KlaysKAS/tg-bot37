import telebot
env = open('.env')
token = env.read()
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    if message.text == 'hello':
        bot.send_message(message.from_user.id, "И тебе привет")
    else:
        bot.send_message(message.from_user.id, message.text)

bot.polling(none_stop=True, interval=0)