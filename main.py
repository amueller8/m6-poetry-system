from line import Line
from api_keys import API_Key
import requests, json 
import os

"""
Abby Mueller

https://www.tutorialspoint.com/\
    find-current-weather-of-any-city-using-openweathermap-api-in-python
#https://geekyhumans.com/get-weather-information-using-python/ 
"""

#global, OpenWeather API key 
key = API_Key().get_key()

def query_city_for_weather(city, state=""):
    if state != "":
        state = ","+state
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    total_query = base_url + "q=" + city + state + "&APPID=" + key

    response = requests.get(total_query)

    if response.status_code == 200:
        resp = response.json()
        main_info = resp["main"]
        #temperature, in kelvin
        curr_temp = main_info["temp"]
        #convert to F
        print(curr_temp)
        curr_temp = (9/5) * (curr_temp - 273) + 32
        print(curr_temp)
        weather = resp["weather"][0]["main"]

        return [curr_temp, weather]

#weather options:
"""
thunderstorm
drizzle
rain
snow
clouds
mist
smoke
haze
dust
fog
sand
ash
squall
tornado
clear

extreme
"""



def main():
    print("hi")
    
    print(query_city_for_weather("Boston"))
main()