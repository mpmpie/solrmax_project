from openweather.api import OpenWeatherAPI
from givenergy.api import GivEnergyAPI
import datetime as dt
import dotenv

config = dotenv.dotenv_values('.env')
data_directory = config.get("DATA_DIRECTORY")

def main():
    now = dt.datetime
    data = [now]
    weather = OpenWeatherAPI.get_live_weather()
    print(weather)
    # energy = GivEnergyAPI.get_latest_data()
    # print(energy)
    # for i in weather: 
    #     data.append(i)
    # for i in energy:
    #     data.append(i)
    # filepath = f"{data_directory}/data/{now.date()}.csv"
if __name__ == "__main__": 
    main()