import string

import requests
import datetime
import json

from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor



bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)



@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Salut! Scrie-mi numele orașului și eu îți voi trimite un raport meteo!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Senin \U00002600",
        "Clouds": "Înnorat \U00002601",
        "Rain": "Ploaie \U00002614",
        "Drizzle": "Ploaie \U00002614",
        "Thunderstorm": "Furtună \U000026A1",
        "Snow": "Zapadă \U0001F328",
        "Mist": "Tuman \U0001F32B"
    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Priviți pe geam, nu înțeleg ce fel de prognoza e acolo!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        visibility = data["visibility"]
        country = data["sys"]["country"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Prognoza meteo în orașul: {city} {country}\nTemperatura: {cur_weather} C° {wd}\n"
              f"Umidiatea: {humidity}%\nPresiunea: {pressure} hPa\nVânt: {wind} m/s\nVizibilitatea: {visibility} m\n"
              f"Răsăritul soarelui: {sunrise_timestamp}\nApusul soarelui: {sunset_timestamp}\nLungimea zilei: {length_of_the_day}\n"

              f"O zi frumoasa!"
              )


    except:
        await message.reply("\U00002620 Nu există așa oraș! \U00002620\n"
        "Verificați vă rog numele orașului:")

@dp.message_handler()
async def echo_send(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Nu vorbi urât!')
        await message.delete()



if __name__ == '__main__':
    executor.start_polling(dp)