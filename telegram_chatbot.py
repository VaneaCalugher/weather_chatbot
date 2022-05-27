
import telebot
from chatbot_model import get_message_response
from main import get_weather
import meteo
TOKEN = "5326686254:AAE5_8LX9a_DcCOhAd78h2F0JpX_cTiaZnQ"
bot = telebot.TeleBot(TOKEN)


meteo.init()

@bot.message_handler(commands=["start"])
def start_command(message):
     bot.send_message(message.chat.id,"Bine v-am gasit! Hai sa discutam!")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if meteo.meteo == True:
        prognoza = get_weather(message.html_text)
        bot.send_message(message.chat.id, prognoza)
        result = ("O zi frumoasa!")
        bot.send_message(message.chat.id, result)
        meteo.meteo = False
    else:
        bot.send_message(message.chat.id,get_message_response(str(message.html_text)) )


# Запускаем бота
bot.polling(none_stop=True, interval=0)
