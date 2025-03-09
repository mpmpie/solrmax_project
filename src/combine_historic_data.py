import datetime as dt
from tools.datetools import DayOfWeek
from givenergy.api import GivEnergyAPI
import dotenv
import os
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")

pd.set_option("display.float_format", "{:.2f}".format)

def main():
    #### Creating dataframes from csv's and creating copies 
    weather = pd.read_csv(f'{data_directory}/historic_data/weather_data_keep.csv')
    weather_df = weather.copy()
    solar_panel = pd.read_csv(f'{data_directory}/historic_data/sp_data_v1.csv')
    solar_panel_df = solar_panel.copy()

    #### Filling empty data
    weather_df['rain_1h'] = weather_df['rain_1h'].fillna(0)
    weather_df['rain_3h'] = weather_df['rain_3h'].fillna(0)
    weather_df['snow_1h'] = weather_df['snow_1h'].fillna(0)
    weather_df['snow_3h'] = weather_df['snow_3h'].fillna(0)
    weather_df['visibility'] = weather_df['visibility'].fillna(-100)
    weather_df['wind_gust'] = weather_df['wind_gust'].fillna(0)
    weather_df = weather_df.drop(weather_df.index[0:533])
    weather_compressed_df = weather_df.drop(columns=['weather_main', 'weather_description', 'weather_icon', 'weather_id', 'lat', 'lon', 'city_name', 'timezone'])

    #### Compressing weather data into individual hours
    start_time = pd.Timestamp(2023, 9, 24, 0, 0, 0)  # 24th September 2023, 00:00
    end_time = pd.Timestamp(2025, 2, 22, 23, 0, 0)   # 14th February 2025, 23:00 (last hour)
    start_time = pd.Timestamp(start_time, tz="UTC")
    end_time = pd.Timestamp(end_time, tz="UTC")

    #### Iterate through each hour
    solar_panel_hourly_df = solar_panel_df.copy() 
    solar_panel_df["Time"] = solar_panel_df["Time"].apply(pd.Timestamp)

    current_time = start_time
    while current_time <= end_time:
        next_time = current_time + pd.Timedelta(hours=1)
        hourly_entries = solar_panel_df.loc[(solar_panel_df["Time"] >= current_time) & (solar_panel_df["Time"] < next_time), :]
        solar_panel_hourly_df.loc[(solar_panel_df["Time"] >= current_time) & (solar_panel_df["Time"] < next_time), 'Time'] = current_time
        current_time += pd.Timedelta(hours=1)
    
    #### Compressing solar panel data
    weather_compressed_df = weather_compressed_df.groupby(["dt", "dt_iso"]).agg({
            "temp": "mean",
            "visibility": "mean",
            "dew_point": "mean",
            "feels_like": "mean",
            "temp_min": "mean",
            "temp_max": "mean",
            "pressure": "mean",
            "humidity": "mean",
            "wind_speed": "mean",
            "wind_deg": "mean",
            "wind_gust": "mean",
            "rain_1h": "mean",
            "rain_3h": "mean",
            "snow_1h": "mean",
            "snow_3h": "mean",
            "clouds_all": "mean"
        }).reset_index()
    weather_compressed_df.columns = ['dt', 'dt_iso', 'temp', 'visibility', 'dew_point', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'wind_speed', 'wind_deg', 'wind_gust', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h', 'clouds_all']

    solar_panel_compressed_df = solar_panel_hourly_df.groupby("Time").agg({
            # "SolarPower": ["mean", "std"],   # Average temperature
            "SolarPower": "mean",   # Average temperature
            "Status": "max",   # Maximum power output
            "BatteryPercentage": "median",        # Minimum voltage
            "BatteryPower": "mean",        # Minimum voltage
            "BatteryTemperature": "max",        # Minimum voltage
            "PowerConsumption": "mean"        # Minimum voltage
        }).reset_index()
    solar_panel_compressed_df['dt'] = solar_panel_compressed_df['Time'].apply(lambda x : int(x.timestamp()))
    solar_panel_compressed_df = solar_panel_compressed_df.drop(0)

    # weather_compressed_df.to_csv(f'{data_directory}/historic_data/weather_all.csv')
    # solar_panel_compressed_df.to_csv(f'{data_directory}/historic_data/sp_all.csv')

    solar_panel_compressed_df.reset_index()
    weather_compressed_df.reset_index()
    weather_compressed_df.set_index('dt', inplace = True)
    solar_panel_compressed_df.set_index('dt', inplace = True)
    merged_df = pd.concat([solar_panel_compressed_df, weather_compressed_df], axis = 1, join = "inner")
    merged_df.index = pd.to_datetime(merged_df.index, unit = "s")

    solar_panel_compressed_df.to_csv(f'{data_directory}/historic_data/all_historic_data.csv')


if __name__ == "__main__":
    main()