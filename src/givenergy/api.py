import requests
import dotenv

config = dotenv.dotenv_values("src/.env")

key = config.get('GIV_ENERGY_API_KEY')
inverter_id = config.get("GIV_ENERGY_INVERTER_SERIAL_NUMBER")
url = 'https://api.givenergy.cloud/v1/inverter/{}'.format(inverter_id)
headers = {
            'Authorization': 'Bearer {}'.format(key),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }


class GivEnergyAPI:

    def get_latest_data():
        endpoint = '{}/system-data/latest'.format(url)
        response = requests.get(url = endpoint, headers = headers)
        print(response.json())
        results = {}
        if response.status_code == 200:
            response_json = response.json()['data']
            results['SolarPower'] = response_json['solar']['power']
            results['Status'] = GivEnergyAPI.get_status_int(response_json['status'])
            results['BatteryPercent'] = response_json['battery']['percent']
            results['BatteryPower'] = response_json['battery']['power']
            results['BatteryTemperature'] = response_json['battery']['temperature']
            results['Consumption'] = response_json['consumption']
        else:
            results['Status'] = response.status_code
            results['Error'] = response.json()['message']
        return results
    
    def get_historic_data(date, pageSize, pageNumber):
        endpoint = f'{url}/data-points/{date}'
        params = {
                'page': pageNumber,
                'pageSize': pageSize
            }
        response = requests.request('GET', endpoint, headers=headers, params=params)
        results = []
        if response.status_code == 200:
            response_json = response.json()['data']
            for entry in response_json: 
                data_point = {}
                # data_point['Time'] = entry['time']
                data_point['SolarPower'] = entry['power']['solar']['power']
                data_point['Status'] = GivEnergyAPI.get_status_int(entry['status'])
                data_point['BatteryPercentage'] = entry['power']['battery']['percent']
                data_point['BatteryPower'] = entry['power']['battery']['power']
                data_point['BatteryTemperature'] = entry['power']['battery']['temperature']
                data_point['PowerConsumption'] = entry['power']['consumption']['power']
                data_point['Time'] = entry['time']
                results.append(data_point)
        else:
            results = []
            error = {}
            error['Status'] = response.status_code
            error['Error'] = response.json()['message']
            results.append(error)
        return results

    def get_status_int(status):
        status_mapping = {
            "WAITING": 0,
            "NORMAL": 1,
            "WARNING": 2,
            "ERROR": 3,
            "UPDATING": 4,
            "BYPASS": 5
        }
        return status_mapping.get(status.upper(), 6)