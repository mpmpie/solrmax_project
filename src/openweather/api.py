import requests
import dotenv
import datetime as dt

config = dotenv.dotenv_values(".env")

key = config.get('OPEN_WEATHER_API_KEY')
lat = config.get('OPEN_WEATHER_LAT')
lon = config.get('OPEN_WEATHER_LON')

url = "https://api.openweathermap.org/data/2.5"
units = "metric"

class OpenWeatherAPI:

    def get_live_weather():
        api_endpoint = "{}/weather?lat={}&lon={}&appId={}&units={}".format(url, lat, lon, key, units)
        results = {}
        response = requests.get(api_endpoint)
        response_json = response.json()
        if response.status_code == 200:
            results['Temperature'] = response_json.get('main').get('temp')
            results['Pressure'] = response_json.get('main').get('pressure')
            results['Humidity'] = response_json.get('main').get('humidity')
            results['Clouds'] = response_json.get('clouds').get('all')
            daylight = dt.datetime.fromtimestamp(response_json.get('sys').get('sunset')) - dt.datetime.fromtimestamp(response_json.get('sys').get('sunrise'))
            results['Daylight'] = daylight
        else:
            results['Status Code'] = response_json['cod']
            results['Message'] = response_json['message']
        return results
    
    def get_historic_weather(timestamp: int):
        # https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=39.099724&lon=-94.578331&dt=1643803200&appid={API key}
        api_endpoint = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={}&lon={}&dt={}&appId={}&units={}".format(lat, lon, timestamp, key, units)
        results = {}
        response = requests.get(api_endpoint)
        response_json = response.json()
        print(response_json)
        if response.status_code == 200:
            results['Temperature'] = response_json.get('main').get('temp')
            results['Pressure'] = response_json.get('main').get('pressure')
            results['Humidity'] = response_json.get('main').get('humidity')
            results['Clouds'] = response_json.get('clouds').get('all')
            daylight = dt.datetime.fromtimestamp(response_json.get('sys').get('sunset')) - dt.datetime.fromtimestamp(response_json.get('sys').get('sunrise'))
            results['Daylight'] = daylight
        else:
            results['Status Code'] = response_json['cod']
            results['Message'] = response_json['message']
        return results