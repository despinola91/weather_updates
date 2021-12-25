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
                        "uv_index": ""
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
  
    
    def get_current_temp(self, soup):
        result = ""
        try:
            result = str(soup.find(attrs={"data-testid": "TemperatureValue", "class": "CurrentConditions--tempValue--3KcTQ"}).string)
        except:
            print("Current temp could not be found") 
        
        return result

    
    def get_day_description(self, soup):
        result = ""
        try:
            result = soup.find(attrs={"data-testid": "wxPhrase", "class": "CurrentConditions--phraseValue--2xXSr"}).string
        except:
            print("Day description could not be found") 
        
        return result

    
    def fill_forecast(self, soup):

        general_table = soup.find(attrs={"data-testid": "WeatherTable", "class": "WeatherTable--columns--3q5Nx WeatherTable--wide--YogM9"})
        
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
        self.weather_raw_data["today_forecast"][0]["temperature"] = general_table.contents[0].find(attrs={"data-testid": "TemperatureValue"}).string
        self.weather_raw_data["today_forecast"][0]["rain_percentage"] = self.get_rain_percentage(general_table.contents[0])
        
        #afternoon
        self.weather_raw_data["today_forecast"][1]["temperature"] = general_table.contents[1].find(attrs={"data-testid": "TemperatureValue"}).string
        self.weather_raw_data["today_forecast"][1]["rain_percentage"] = self.get_rain_percentage(general_table.contents[1])

        #night
        self.weather_raw_data["today_forecast"][2]["temperature"] = general_table.contents[2].find(attrs={"data-testid": "TemperatureValue"}).string
        self.weather_raw_data["today_forecast"][2]["rain_percentage"] = self.get_rain_percentage(general_table.contents[2])

        #early morning
        self.weather_raw_data["today_forecast"][3]["temperature"] = general_table.contents[3].find(attrs={"data-testid": "TemperatureValue"}).string
        self.weather_raw_data["today_forecast"][3]["rain_percentage"] = self.get_rain_percentage(general_table.contents[3])


    def get_rain_percentage(self, column):
        result = ""
        try:    
            if len(column.find("span", attrs={"class": "Column--precip--2H5Iw"}).contents) > 1:
                result = column.find("span", attrs={"class": "Column--precip--2H5Iw"}).contents[1].string
        except:
            print("Rain percentage could not be found")

        return result
    
    
    def get_max_min(self, soup):
        result = ""
        try:
            for child in soup.find(attrs={"data-testid": "wxData", "class": "WeatherDetailsListItem--wxData--23DP5"}).contents: 
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


    def get_final_message(self):
        msg = f"""
        Temperatura actual: { self.weather_raw_data['current_temp'] }
        Cielo: {self.weather_raw_data['day_description']}.

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
        Indice UV: {self.weather_raw_data['uv_index']}.
        """
        
        return msg