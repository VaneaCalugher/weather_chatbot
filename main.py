
from pprint import pprint


import requests
import datetime
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
from config import tg_bot_token, open_weather_token




def get_weather(city):
    # city = input("Scrie-mi numele orasului si eu iti voi trimite un raport meteo! \n")
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
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        # pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]


        weather_description = data ["weather"] [0] ["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Priviți pe geam, nu înțeleg ce fel de prognoză e acolo!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        visibility = data["visibility"]
        country = data["sys"]["country"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        prognoza=(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                      f"Prognoza meteo în orașul: {city} {country}\nTemperatura: {cur_weather} C° {wd}\n"
                      f"Umidiatea: {humidity}%\nPresiunea: {pressure} hPa\nVânt: {wind} m/s\nVizibilitatea: {visibility} m\n"
                      f"Răsăritul soarelui: {sunrise_timestamp}\nApusul soarelui: {sunset_timestamp}\nLungimea zilei: {length_of_the_day}"

                      )
        # print (prognoza)
        return prognoza


    except Exception as ex:
        print(ex)
        eroare=("\U00002620 Nu există așa oraș! \U00002620\n"
        "Verificați vă rog numele orașului:")
        return eroare




def main():
    get_weather()



if __name__== '__main__':
    main()
