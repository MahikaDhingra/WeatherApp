import requests
from dotenv import load_dotenv
import os
import json
from model.weatherdata import WeatherData

load_dotenv()
api_key = os.getenv('API_KEY')


def getLatAndLong(city_name, state_code, country_code, API_key):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}'
    response = requests.get(url, timeout=6).json()
    data = response[0]
    print(data)
    lat = data.get('lat')
    lon = data.get('lon')
    return lat, lon

def getCurrentWeather(lat, lng, API_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_key}'
    response = requests.get(url, timeout=6).json()
    print(response)
    data = WeatherData(
        main=response.get('weather')[0].get('main'),
        description=response.get('weather')[0].get('description'),
        icon=response.get('weather')[0].get('icon'),
        temperature=int(response.get('main').get('temp')) - 273,
        lat=lat,
        lng=lng
    )

    return data

def main (city_name, state_code, country_code):
    lat, lon = getLatAndLong(city_name, state_code, country_code, api_key)
    return getCurrentWeather(lat, lon, api_key)

if __name__ == "__main__":
    lat, lon = getLatAndLong('Melbourne', 'VIC', 'Australia', api_key)
    print(getCurrentWeather(lat, lon, api_key))