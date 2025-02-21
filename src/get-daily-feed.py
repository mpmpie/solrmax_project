from openweather.api import OpenWeatherAPI
from givenergy.api import GivEnergyAPI
import datetime as dt
import dotenv
import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")
log_directory = config.get("LOG_DIRECTORY")
log_level = config.get("LOG_LEVEL")

def main():
    now = dt.datetime.now()
    logging.basicConfig(filename=f"{log_directory}/{now.date()}.log",level=log_level)
    timestamp = {'Timestamp': now.strftime("%Y-%m-%d %H:%M:%S")}

    weather = OpenWeatherAPI.get_live_weather()
    energy = GivEnergyAPI.get_latest_data()
    data_entry = pd.Series({**timestamp, **weather, **energy})
    logger.debug(data_entry)

    filepath = f"{data_directory}/{now.date()}.csv"

    if os.path.exists(filepath):

        df = pd.read_csv(filepath, parse_dates=True) 
    
        # Append the new row to the DataFrame
        df = pd.concat([df, data_entry.to_frame().T ])
        df.set_index("Timestamp", inplace=True)

    else: 
        df = pd.DataFrame(data_entry.to_frame().T)
        df.set_index("Timestamp", inplace=True)


    # Save back to CSV
    df.to_csv(filepath)

if __name__ == "__main__": 
    main()