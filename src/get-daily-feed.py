from openweather.api import OpenWeatherAPI
from givenergy.api import GivEnergyAPI
import datetime as dt
import dotenv
import pandas as pd
import os

config = dotenv.dotenv_values('src/.env')
data_directory = config.get("DATA_DIRECTORY")

def main():
    now = dt.datetime.now()
    timestamp = {'Timestamp': now.strftime("%Y-%m-%d %H:%M:%S")}

    weather = OpenWeatherAPI.get_live_weather()
    print(weather)
    energy = GivEnergyAPI.get_latest_data()
    data_entry = pd.Series({**timestamp, **weather, **energy})
    print(data_entry)

    filepath = f"{data_directory}/{now.date()}.csv"

    if os.path.exists(filepath):

        df = pd.read_csv(filepath, parse_dates=True) 
    
        # Append the new row to the DataFrame
        df = pd.concat([df, data_entry.to_frame().T ])
        df.set_index("Timestamp", inplace=True)

        print(df)
    else: 
        df = pd.DataFrame(data_entry.to_frame().T)
        df.set_index("Timestamp", inplace=True)


    # Save back to CSV
    df.to_csv(filepath)

if __name__ == "__main__": 
    main()