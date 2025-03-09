import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import dotenv
import logging
import os
from datetime import datetime as dt
from tools.emailtools import send_email
from openweather.api import OpenWeatherAPI

logger = logging.getLogger(__name__)

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")
log_directory = config.get("LOG_DIRECTORY")
log_level = config.get("LOG_LEVEL")

def main():
    pd.set_option('display.max_colwidth', None)
    np.set_printoptions(suppress=True)

    now = dt.now()
    # data = pd.read_csv(f'{data_directory}/2025-02-16.csv', delimiter = ',')
    data = pd.read_csv(f'{data_directory}/{now.date()}.csv', delimiter = ',')
    solar_panel_data = data.copy()
    solar_panel_data["Time"] = solar_panel_data["Timestamp"].apply(lambda x : dt.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%H:%M'))

    #### Solar Generation From Today Report
    plt.plot(solar_panel_data["Time"], solar_panel_data["SolarPower"])
    num_ticks = 12  # Change to 24 for more labels
    tick_labels = solar_panel_data["Time"][::12]  # Select time values
    plt.xticks(tick_labels, rotation=45)  # Set limited ticks and rotate for readability
    plt.title("Today's Solar Energy Generation")
    plt.xlabel('Time of Day')
    plt.ylabel('Energy Generation in Watts')
    plt.savefig('EnergyGeneration.jpg', format='jpg')
    plt.show()
    plt.close()

    #### Getting Weather Forecast Data
    forecast, sunrises_sunsets = OpenWeatherAPI.get_48hr_forecast()
    forecast_df = pd.DataFrame(forecast)
    sunrises_sunsets_df = pd.DataFrame(sunrises_sunsets)
    forecast_df["DayTime"] = forecast_df["Time"].dt.strftime('%a %H:%M')

    #### Generating Forecast
    figure, ax1 = plt.subplots()
    ax1.plot(forecast_df["DayTime"], forecast_df["Clouds"], label = "Clouds Percentage", color="red", marker="o", linestyle="-")
    ax1.set_xlabel('Day and Time')
    ax1.set_ylabel("Clouds Percentage", color="red")
    ax1.tick_params(axis="y", labelcolor="red")
    ax2 = ax1.twinx()
    ax2.plot(forecast_df["DayTime"], forecast_df["UVI"], label = "UVI", color="blue", marker="o", linestyle="-")
    ax2.set_ylabel("UVI", color="blue")

    ax1.set_xticks(forecast_df["DayTime"][::4])  # Ensure ticks are set
    ax1.set_xticklabels(forecast_df["DayTime"][::4], rotation=45, ha="right")  # Rotate labels & align right
    plt.title("Cloud and UV 48 Hour Forecast")
    plt.savefig('48HrForecast.jpg', format='jpg')
    plt.show()
    plt.close()

    #### Sending Daily Report Email
    send_email()

if __name__ == "__main__": 
    main()