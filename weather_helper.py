import requests
from bs4 import BeautifulSoup
import json

class WeatherInfoHandler:
    """Simple class to get specific weather information from website"""
    
    URL = 'https://weather.com/es-AR/tiempo/hoy/l/ARBA0009:1:AR?Goto=Redirected'
    weather_raw_data = {
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
                        "uv_index": "",
                        "sunrise_time": "",
                        "sunset_time":""
                        }


    def get_weather_update(self):
        r = requests.get(self.URL)
        soup = BeautifulSoup(r.text, "html.parser")
        self.fill_weather_data(soup)
        
        return self.get_final_message()
    
    
    def fill_weather_data(self, soup):
        self.weather_raw_data["current_temp"] = self.get_current_temp(soup)
        self.weather_raw_data["day_description"] = self.get_day_description(soup)
        
        self.fill_forecast(soup)
        
        self.weather_raw_data["max_min"] = self.get_max_min(soup)
        self.weather_raw_data["humidity"] = self.get_humidity(soup)
        self.weather_raw_data["uv_index"] = self.get_uv_index(soup)
        
        self.weather_raw_data["sunrise_time"] = self.get_sunrise_time(soup)
        self.weather_raw_data["sunset_time"] = self.get_sunset_time(soup)
  
    
    def get_current_temp(self, soup):
        result = ""
        try:
            result = str(soup.find(attrs={"data-testid": "TemperatureValue"}).string)
        except:
            print("Current temp could not be found") 
        
        return result

    
    def get_day_description(self, soup):
        result = ""
        try:
            result = soup.find(attrs={"data-testid": "wxPhrase"}).string
        except:
            print("Day description could not be found") 
        
        return result

    
    def fill_forecast(self, soup):

        general_table = soup.find(attrs={"data-testid": "WeatherTable", "class": "WeatherTable--columns--OWgEl WeatherTable--wide--3dFXu"})
        
        if general_table == None:
            print("General table could not be found")
        
            #morning
            self.weather_raw_data["today_forecast"][0]["temperature"] = ""
            self.weather_raw_data["today_forecast"][0]["rain_percentage"] = ""
            
            #afternoon
            self.weather_raw_data["today_forecast"][1]["temperature"] = ""
            self.weather_raw_data["today_forecast"][1]["rain_percentage"] = ""

            #night
            self.weather_raw_data["today_forecast"][2]["temperature"] = ""
            self.weather_raw_data["today_forecast"][2]["rain_percentage"] = ""

            #early morning
            self.weather_raw_data["today_forecast"][3]["temperature"] = ""
            self.weather_raw_data["today_forecast"][3]["rain_percentage"] = ""
            
            return
            
        #morning
        self.weather_raw_data["today_forecast"][0]["temperature"] = self.get_forecast_temperature(general_table.contents[0])
        self.weather_raw_data["today_forecast"][0]["rain_percentage"] = self.get_rain_percentage(general_table.contents[0])
        
        #afternoon
        self.weather_raw_data["today_forecast"][1]["temperature"] = self.get_forecast_temperature(general_table.contents[1])
        self.weather_raw_data["today_forecast"][1]["rain_percentage"] = self.get_rain_percentage(general_table.contents[1])

        #night
        self.weather_raw_data["today_forecast"][2]["temperature"] = self.get_forecast_temperature(general_table.contents[2])
        self.weather_raw_data["today_forecast"][2]["rain_percentage"] = self.get_rain_percentage(general_table.contents[2])

        #early morning
        self.weather_raw_data["today_forecast"][3]["temperature"] = self.get_forecast_temperature(general_table.contents[3])
        self.weather_raw_data["today_forecast"][3]["rain_percentage"] = self.get_rain_percentage(general_table.contents[3])


    def get_forecast_temperature(self, column):
        result = ""
        try:
            result = column.find(attrs={"data-testid": "TemperatureValue"}).string
        except:
            print("Forecast temperature could not be found")
            
        return result


    def get_rain_percentage(self, column):
        result = ""
        try:    
            if len(column.find("span", attrs={"class": "Column--precip--2ck8J"}).contents) > 1:
                result = column.find("span", attrs={"class": "Column--precip--2ck8J"}).contents[1].string
        except:
            print("Rain percentage could not be found")

        return result
    
    
    def get_max_min(self, soup):
        result = ""
        try:
            for child in soup.find(attrs={"data-testid": "wxData", "class": "WeatherDetailsListItem--wxData--2s6HT"}).contents: 
                result = result + child.string
        except:
            print("Max and min could not be found")
        
        return result
    
    
    def get_humidity(self, soup):
        result = ""
        try:
            result = soup.find(attrs={"data-testid": "PercentageValue"}).string
        except:
            print("Humidity could not be found") 
        
        return result

    
    def get_uv_index(self, soup):
        result = ""
        try:
            result = soup.find(attrs={"data-testid": "UVIndexValue"}).string
        except:
            print("UV index could not be found") 
        
        return result


    def get_sunrise_time(self, soup):
        result = ""
        try:
            sunrise = soup.find(attrs={"class":"SunriseSunset--sunriseDateItem--3qqf7", "data-testid":"SunriseValue"})
            emoji = Emojis()
            result = sunrise.contents[1].string + " " + emoji.emojis["sunrise"]
        except:
            print("Sunrise time could not be found")
        
        return result
    
    
    def get_sunset_time(self, soup):
        result = ""
        try:
            sunset = soup.find(attrs={"class": "SunriseSunset--sunsetDateItem--34dPe SunriseSunset--sunriseDateItem--3qqf7", "data-testid":"SunsetValue"})
            emoji = Emojis()
            result = sunset.contents[1].string + " " + emoji.emojis["sunset"]
        except:
            print("Sunset time could not be found") 
        
        return result
    
     
    def get_final_message(self):
        emoji = Emojis()
        msg = f"""
Temperatura actual: { self.weather_raw_data['current_temp'] }
Cielo: {self.weather_raw_data['day_description']}  {emoji.get_day_description_emoji(description=self.weather_raw_data['day_description'])}

*Mañana*
Temperatura: {self.weather_raw_data['today_forecast'][0]['temperature']}
Porcentaje de lluvia: {self.weather_raw_data['today_forecast'][0]['rain_percentage']}
            
*Tarde*
Temperatura: {self.weather_raw_data['today_forecast'][1]['temperature']}
Porcentaje de lluvia: {self.weather_raw_data['today_forecast'][1]['rain_percentage']}
            
*Noche*
Temperatura: {self.weather_raw_data['today_forecast'][2]['temperature']}
Porcentaje de lluvia: {self.weather_raw_data['today_forecast'][2]['rain_percentage']}
            
*Madrugada*
Temperatura: {self.weather_raw_data['today_forecast'][3]['temperature']}
Porcentaje de lluvia: {self.weather_raw_data['today_forecast'][3]['rain_percentage']}

Max/min: {self.weather_raw_data['max_min']}
Humedad: {self.weather_raw_data['humidity']}
Indice UV: {self.weather_raw_data['uv_index']} {emoji.get_uvindex_emoji(description=self.weather_raw_data['uv_index'])}

Sunrise time: {self.weather_raw_data['sunrise_time']}
Sunset time: {self.weather_raw_data['sunset_time']}
"""
        return msg
    
    
    
class Emojis:
    """Class to retrieve right emojis to add some funny context"""
    
    emojis = {
        #day description
        'sunny': '\U00002600',
        'cloudy': '\U000026C5',
        'rain': '\U0001F327',
        'storm': '\U000026C8',
        
        #UV index
        'uvindex_low': '\U0001F600',
        'uvindex_medium': '\U0001F642',
        'uvindex_high': '\U0001F975',
        'uvindex_extreme': '\U00002620',
        'sunrise': '\U0001F304',
        'sunset': '\U0001F307'
    }
    
    def get_uvindex_emoji(self, description):
        if description == "0 de 10" or description == "1 de 10" or description == "2 de 10" or description == "3 de 10":
            return self.emojis['uvindex_low']
        if description == "4 de 10" or description == "5 de 10" or description == "6 de 10" or description == "7 de 10":
            return self.emojis['uvindex_medium']
        if description == "8 de 10" or description == "9 de 10" or description == "10 de 10":
            return self.emojis['uvindex_high']
        if description == "Extremo":
            return self.emojis['uvindex_extreme']
        
    def get_day_description_emoji(self, description):
        if description == 'Soleado':
            return self.emojis['sunny']
        elif description == "Mayormente nublado":
            return self.emojis['cloudy']
        
    