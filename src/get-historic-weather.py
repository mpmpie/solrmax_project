from datetime import datetime as dt
from tools.datetools import DayOfWeek
from openweather.api import OpenWeatherAPI as openweather
import dotenv
import pandas as pd

config = dotenv.dotenv_values('.env')
data_directory = config.get("DATA_DIRECTORY")

def main():

    openweather.get_historic_weather(1737115200)

    # weather = OpenWeatherAPI.get_historic_data(date)
if __name__ == "__main__": 
    main()