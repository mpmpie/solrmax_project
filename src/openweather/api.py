import requests
import dotenv
import datetime as dt

config = dotenv.dotenv_values("src/.env")

key = config.get('OPEN_WEATHER_API_KEY')
lat = config.get('OPEN_WEATHER_LAT')
lon = config.get('OPEN_WEATHER_LON')

url = "https://api.openweathermap.org/data/3.0"
units = "metric"

class OpenWeatherAPI:

    def get_live_weather():
        api_endpoint = "{}/onecall?lat={}&lon={}&appId={}&units={}&exclude=minutely,hourly,alerts,daily".format(url, lat, lon, key, units)
        print(api_endpoint)
        results = {}
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            current = response.json().get('current')
            results['Temperature'] = current.get('temp')
            results['Pressure'] = current.get('pressure')
            results['Humidity'] = current.get('humidity')
            results['Clouds'] = current.get('clouds')
            results['DewPoint'] = current.get('dew_point')
            results['UVI'] = current.get('uvi')
            results['Visibility'] = current.get('visibility')
            results['WindSpeed'] = current.get('wind_speed')
            results['WindDegree'] = current.get('wind_deg')
            daylight = dt.datetime.fromtimestamp(current.get('sunset')) - dt.datetime.fromtimestamp(current.get('sunrise'))
            daylight = daylight.seconds
            results['Daylight'] = daylight
            print(type(daylight))
        else:
            results['Status Code'] = response.json()['cod']
            results['Message'] = response.json()['message']
        return results
    
    def get_historic_weather(timestamp: int):
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
            print(type(daylight))
        else:
            results['Status Code'] = response_json['cod']
            results['Message'] = response_json['message']
        return results