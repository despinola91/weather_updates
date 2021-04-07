import requests
from bs4 import BeautifulSoup
import json

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
    msg = f"""
Temperatura actual: { weather_data['current_temp'] }
Cielo: {weather_data['day_description']}.

*Mañana*
Temperatura: {weather_data['today_forecast'][0]['temperature']}
Porcentaje de lluvia: {weather_data['today_forecast'][0]['rain_percentage']}
    
*Tarde*
Temperatura: {weather_data['today_forecast'][1]['temperature']}
Porcentaje de lluvia: {weather_data['today_forecast'][1]['rain_percentage']}
    
*Noche*
Temperatura: {weather_data['today_forecast'][2]['temperature']}
Porcentaje de lluvia: {weather_data['today_forecast'][2]['rain_percentage']}
    
*Madrugada*
Temperatura: {weather_data['today_forecast'][3]['temperature']}
Porcentaje de lluvia: {weather_data['today_forecast'][3]['rain_percentage']}

Max/min: {weather_data['max_min']}
Humedad: {weather_data['humidity']}
Indice UV: {weather_data['uv_index']}.
"""

    #return json.dumps(weather_data, indent=4, ensure_ascii=False)
    return msg
