# solrmax_project
To analyse data from solar panel energy output in relation to the weather

## Installation and Requirements

A device to collect data on, i.e. a raspberry pi 
A givenergy account and API Key
An openweather account and API key for 3.0 calls (1,000 free per day)

If running on a raspberry pi to install pandas you will need to run the below.

```bash
sudo apt-get install python3-pandas
```

Setup env variables with your givenergy api key, openweather api key and your location. 

``` bash
cp ./src/.env_example ./src/.env
vim ./src/.env
```

Set the `.env` file location;  

Set up a crontab

```bash 
crontab -e 
```
This will trigger a collection every 5 minutes:
```
*/5 * * * * python3 /home/pi/solrmax_project/src/get-daily-feed.py > /home/pi/log/log.log 2>&1

51 21 * * * python3 /home/jamesdavis/solrmax_project/src/create_daily_report.py > /home/jamesdavis/log/email_log.log 2>&1
```

## Sample data 

```csv
Timestamp,Temperature,Pressure,Humidity,Clouds,DewPoint,UVI,Visibility,WindSpeed,WindDegree,Daylight,SolarPower,Status,BatteryPercent,BatteryPower,BatteryTemperature,Consumption
2025-02-16 12:00:10,5.54,1000.0,66,40,-1.17,0.25,10000.0,5.14,60.0,36309.0,1529.0,1.0,90.0,-1318.0,18.0,124.0
```