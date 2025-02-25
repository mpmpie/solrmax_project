from datetime import datetime as dt
from tools.datetools import DayOfWeek
from givenergy.api import GivEnergyAPI
import dotenv
import os
import pandas as pd

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")

def main():

    # openweather.get_historic_weather(1737115200)

    # weather = OpenWeatherAPI.get_historic_data(date)
    # historic_weather = pd.read_csv('/Users/ruthbeckwith/Downloads/8c681fe11b88a2371e4db0f41b498c7f.csv', delimiter = ',')
    # historic_weather_df = historic_weather.copy()
    # print(historic_weather.info())
    daterange = pd.date_range(pd.to_datetime('2023-09-25'), pd.to_datetime('2025-02-14'))
    historic_solar_panel_data = []
    for day in daterange:
        # print(dt.date(day))
        solar_panel_data = GivEnergyAPI.get_historic_data(dt.date(day), 850, 1)
        # print(type(solar_panel_data[0]))
        historic_solar_panel_data = historic_solar_panel_data + solar_panel_data
        # historic_solar_panel_data.append(solar_panel_data)
        # solar_panel_df = pd.DataFrame(solar_panel_data)
        # for entry in solar_panel_data:
            # if (entry['Time']).:

        # historic_solar_panel_data.append(solar_panel_data)
        # print(solar_panel_data)
    # print(len(historic_solar_panel_data))
    historic_solar_panel_df = pd.DataFrame(historic_solar_panel_data)
    # print(historic_solar_panel_df.head)
    historic_solar_panel_df.to_csv(f'{data_directory}/historic_data/sp_data_v1.csv')
    # print(historic_solar_panel_df)



if __name__ == "__main__": 
    main()