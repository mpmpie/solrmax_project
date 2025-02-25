import datetime as dt
from tools.datetools import DayOfWeek
from givenergy.api import GivEnergyAPI
import os
import dotenv
import pandas as pd
import logging

logger = logging.getLogger(__name__)

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")
log_directory = config.get("LOG_DIRECTORY")
log_level = config.get("LOG_LEVEL")

# Produces CSV file with
# date, temp, air pressure, humidity, cloud cover, sunlight hours, solar power, status, battery %, b power, b temp, consumption
def main():
    now = dt.datetime.now()
    logging.basicConfig(filename=f"{log_directory}/{now.date()}.log",level=log_level)
    date = dt.datetime.fromisoformat('2024-01-23').date()
    day_of_week = DayOfWeek.getShort(date)
    data = []
    page_size = 24
    pages = 12
    for page in range(pages):
        energy = GivEnergyAPI.get_historic_data(date, page_size, page + 1)
        if energy[0].keys().__contains__('Error'):
            logger.error('Error with GivEnergy API')
        else: 
            logger.info('Successful GivEnergy call')
            data = data + energy
            # data.update(energy)
    # print('Data: {}  \nSize: {}'.format(data, len(data)))
    solar_data_frame = pd.DataFrame(data)
    # solar_data_frame = solar_data_frame.transpose()
    # solar_csv  = solar_data_frame.to_csv('')
    #     for i in energy:
    #         data.append(i)
    # for d in data:
    #     Writer.writeToCSVFile(d, f"{data_directory}/data/{date}.csv")
    # TODO
    # Group the above in to 15 mins worth of data
    # Get weather data for the date times 
    

        
    # weather = OpenWeatherAPI.get_historic_data(date)
if __name__ == "__main__": 
    main()