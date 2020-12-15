# Example of Instagram link:

# https://www.instagram.com/p/CIY38LkHLFF/?utm_source=ig_web_copy_link

import requests
from bs4 import BeautifulSoup
import json
from telebot import TeleBot

TOKEN = "TOKEN"


weather_data = {
                "current_temp": "",
                "day_description": "",
                "today_forecast": [
                                    {
                                        "day_time": "morning",
                                        "temperature":"",
                                        "rain_percentage": ""
                                    },
                                    {
                                        "day_time": "afternoon",
                                        "temperature":"",
                                        "rain_percentage": ""
                                    },
                                    {
                                        "day_time": "night",
                                        "temperature":"",
                                        "rain_percentage": ""
                                    },
                                    {
                                        "day_time": "early_morning",
                                        "temperature":"",
                                        "rain_percentage": ""
                                    },
                                ],
                "max_min": "",
                "humidity": "",
                "uv_index": ""
                }

def get_max_min(soup):
    result = ""
    for child in soup.find(attrs={"data-testid": "wxData", "class": "WeatherDetailsListItem--wxData--23DP5"}).contents: 
        result = result + child.string
    
    return result

def get_rain_percentage(column):
    
    if len(column.find("span", attrs={"class": "Column--precip--2H5Iw"}).contents) > 1:
        rain_percentage = column.find("span", attrs={"class": "Column--precip--2H5Iw"}).contents[1].string
    else:
        rain_percentage = ""

    return rain_percentage

def fill_forecast(soup):
    global weather_data

    general_table = soup.find(attrs={"data-testid": "WeatherTable", "class": "WeatherTable--columns--3q5Nx WeatherTable--wide--YogM9"})

    #morning
    weather_data["today_forecast"][0]["temperature"] = general_table.contents[0].find(attrs={"data-testid": "TemperatureValue"}).string
    weather_data["today_forecast"][0]["rain_percentage"] = get_rain_percentage(general_table.contents[0])
    
    #afternoon
    weather_data["today_forecast"][1]["temperature"] = general_table.contents[1].find(attrs={"data-testid": "TemperatureValue"}).string
    weather_data["today_forecast"][1]["rain_percentage"] = get_rain_percentage(general_table.contents[1])

    #night
    weather_data["today_forecast"][2]["temperature"] = general_table.contents[2].find(attrs={"data-testid": "TemperatureValue"}).string
    weather_data["today_forecast"][2]["rain_percentage"] = get_rain_percentage(general_table.contents[2])

    #early morning
    weather_data["today_forecast"][3]["temperature"] = general_table.contents[3].find(attrs={"data-testid": "TemperatureValue"}).string
    weather_data["today_forecast"][3]["rain_percentage"] = get_rain_percentage(general_table.contents[3])


def fill_weather_data(soup):
    global weather_data

    weather_data["current_temp"] = str(soup.find(attrs={"data-testid": "TemperatureValue", "class": "CurrentConditions--tempValue--3KcTQ"}).string)
    weather_data["day_description"] = soup.find(attrs={"data-testid": "wxPhrase", "class": "CurrentConditions--phraseValue--2xXSr"}).string
    
    fill_forecast(soup)
    
    weather_data["max_min"] = get_max_min(soup)
    weather_data["humidity"] = soup.find(attrs={"data-testid": "PercentageValue"}).string
    weather_data["uv_index"] = soup.find(attrs={"data-testid": "UVIndexValue"}).string

def get_weather_update():
    url = 'https://weather.com/es-AR/tiempo/hoy/l/ARBA0009:1:AR?Goto=Redirected'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    fill_weather_data(soup)
    return json.dumps(weather_data, indent=4, ensure_ascii=False)

app = TeleBot(__name__)
@app.route("/command ?(.*)")
def example_command(message, cmd):
    chat_dest = message["chat"]["id"]
    msg = "Command received: {}".format(cmd)

    app.send_message(chat_dest, msg)


@app.route("(?!/).+")
def send_weather_update(message):
    chat_dest = message['chat']['id']
    #user_msg = message['text']

    msg = get_weather_update()
    app.send_message(chat_dest, msg)

def config(app):
    app.config['api_key'] = 'TOKEN'
    app.poll(debug=True)

if __name__ == "__main__":
    config(app)