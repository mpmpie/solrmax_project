import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import dotenv
import logging
import os
from datetime import datetime as dt
from tools.emailtools import send_email

logger = logging.getLogger(__name__)

config = dotenv.dotenv_values(f'{os.path.dirname(os.path.abspath(__file__))}/.env')
data_directory = config.get("DATA_DIRECTORY")
log_directory = config.get("LOG_DIRECTORY")
log_level = config.get("LOG_LEVEL")

sns.set()
pd.set_option('display.max_colwidth', None)
np.set_printoptions(suppress=True)

now = dt.now()
print(f'{data_directory}/{now.date()}.csv')
data = pd.read_csv(f'{data_directory}/{now.date()}.csv', delimiter = ',')
solar_panel_data = data.copy()
solar_panel_data["Time"] = solar_panel_data["Timestamp"].apply(lambda x : dt.strptime(x,'%Y-%m-%d %H:%M:%S').strftime('%H:%M'))

plt.plot(solar_panel_data["Time"], solar_panel_data["SolarPower"])

num_ticks = 12  # Change to 24 for more labels
tick_labels = solar_panel_data["Time"][::12]  # Select time values
plt.xticks(tick_labels, rotation=90)  # Set limited ticks and rotate for readability
plt.savefig('figure.jpg', format='jpg')
plt.show()
plt.close()

send_email()