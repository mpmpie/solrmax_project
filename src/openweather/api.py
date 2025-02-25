import requests
import dotenv
import os
import datetime as dt

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/../.env')

key = config.get('OPEN_WEATHER_API_KEY')
lat = config.get('OPEN_WEATHER_LAT')
lon = config.get('OPEN_WEATHER_LON')

url = "https://api.openweathermap.org/data/3.0"
units = "metric"

class OpenWeatherAPI:

    def get_live_weather():
        api_endpoint = "{}/onecall?lat={}&lon={}&appId={}&units={}&exclude=minutely,hourly,alerts,daily".format(url, lat, lon, key, units)
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
        else:
            results['Status Code'] = response.json()['cod']
            results['Message'] = response.json()['message']
        return results
    
    def get_historic_weather(timestamp: int):
        api_endpoint = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={}&lon={}&dt={}&appId={}&units={}".format(lat, lon, timestamp, key, units)
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
    
    def get_48hr_forecast():
        api_endpoint = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,alerts,daily&appid={}&units={}".format(lat, lon, key, units)
        response = requests.get(api_endpoint)
        results = []
        if response.status_code == 200:
            hourly = response.json().get('hourly')
            for hour in hourly:
                entry = {}
                entry['Time'] = dt.datetime.fromtimestamp(hour.get('dt'))
                entry['Temperature'] = hour.get('temp')
                entry['Pressure'] = hour.get('pressure')
                entry['Humidity'] = hour.get('humidity')
                entry['Clouds'] = hour.get('clouds')
                entry['DewPoint'] = hour.get('dew_point')
                entry['UVI'] = hour.get('uvi')
                entry['Visibility'] = hour.get('visibility')
                entry['WindSpeed'] = hour.get('wind_speed')
                entry['WindDegree'] = hour.get('wind_deg')
                results.append(entry)
        else:
            error = {}
            error['Status Code'] = response.json()['cod']
            error['Message'] = response.json()['message']
            results.append(error)
        return results
    
    def get_8day_forecast():
        api_endpoint = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&exclude=current,minutely,alerts,hourly&appid={}&units={}".format(lat, lon, key, units)
        response = requests.get(api_endpoint)
        results = []
        if response.status_code == 200:
            daily = response.json().get('daily')
            for day in daily:
                entry = {}
                entry['Time'] = dt.datetime.fromtimestamp(day.get('dt'))
                entry['Temperature'] = day.get('temp')
                entry['Pressure'] = day.get('pressure')
                entry['Humidity'] = day.get('humidity')
                entry['Clouds'] = day.get('clouds')
                entry['DewPoint'] = day.get('dew_point')
                entry['UVI'] = day.get('uvi')
                entry['Visibility'] = day.get('visibility')
                entry['WindSpeed'] = day.get('wind_speed')
                entry['WindDegree'] = day.get('wind_deg')
                results.append(entry)
        else:
            error = {}
            error['Status Code'] = response.json()['cod']
            error['Message'] = response.json()['message']
            results.append(error)
        return results