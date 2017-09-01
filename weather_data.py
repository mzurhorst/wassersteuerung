#!/usr/bin/python3
#
#File           :  weather_data.py
#Author         :  Marcus Zurhorst
#Email          :  marcuszurhorst@gmail.com
#License        :  MIT License
#Copyright      :  (c) 2017 Marcus Zurhorst
#
#Description    :  This module provides functions to fetch weather data from
#                  OpenWeatherMap.org and DWD.de and calculates weighting
#                  factors for the watering duration based weather conditions.

# TODO:   Add customization options based on particular soil conditions.
#         E.g., consider more days when soil keeps humidity.


# Define whether or not debug messages shall be printed
# debug = False     # debug messages surpressed
debug = True      # debug messages enabled


def __get_owm_apikey():
    """ Import the OpenWeatherMap.org API key from a local file.

    This private function is here because I dislike to expose my personal API key on Github.com
    The function will import the API key from a local file 'my_credentials.py'

    Returns:
        str:  OpenWeatherMap.org API key
    """

    try:
        from my_credentials import  owm_apikey
        if debug:
            print("DEBUG:  OpenWeatherMap.org API Key:   ",  owm_apikey)
    except ImportError:
        owm_apikey = "your_owm_apikey"
        print("Please create 'my_credentials.py' file with variable 'owm_apikey'")
        print("Visit http://api.openweathermap.org for details.")

    return owm_apikey


def __get_owm_jsonstring(days):
    """ Load weather forecast JSON string from OpenWeatherMap.org.

    This private function loads the JSON string for the weather forecast from OpenWeatherMap.org
    The URL is hard-coded for my favorite weather station.

    Args:
        days (int):  number of days for weather forecast  (allowable range:  1-3)

    Returns:
        str:  OpenWeatherMap.org JSON string
    """

    # confirm that 'days' is in the allowable range and fix it if required
    if days < 1:
        days = 1
    if days > 3:
        days = 3

    
    import requests

    # assemble the OpenWeatherMap API key in the JSON URL
    # TODO:   Make weather station variable
    owm_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=2953308&appid=' + __get_owm_apikey() + '&units=metric&lang=de&cnt=' + str(days)
    if debug:
        print("DEBUG:   OpenWeatherMap.org URL:   ", owm_url)
        print("DEBUG:   import requests and load JSON string from owm_url")

    # this section will load the JSON object;  type: class requests.models.Response
    r = requests.get(url=owm_url)

    return r.text


def __get_owm_forecast_temperature(json_data, days, progression):
    """ Calculates the forecast temperature from OpenWeatherMap.org data.

    This private function calculates the temperature forecast from the OpenWeatherMap.org data.
    The result depends on the progression factor and the number of forecast days.

    Args:
        json_data:  json formatted OpenWeatherMap weather forecast (optional)

    Returns:
        str:  forecast temperature
    """

    # confirm that 'progression' is in the allowable range and fix it if required
    # values outside this range do not make sense
    if progression < 0.8:
        progression = 0.8
    if progression > 0.92:
        progression = 0.92

    data = json_data

    temperature_avg = 0
    remainder = 1 - progression

    # Run the loop "days" times
    for i in range(days):

        try:
            temperature = data["list"][i]["temp"]["max"]
        except KeyError:
            temperature = 15

        print("Temperatur an der Stelle ", str(i), ":  ", temperature)
        # Following equation has been provided by user Manul in the german Raspberry Pi forum
        # http://www.forum-raspberrypi.de/Thread-python-benoetige-hilfe-bei-formeln-in-einer-schleife?pid=293772#pid293772
        temperature_avg += temperature * (progression + remainder * (i==days-1)) * remainder**i
        print("Aktuelle Durchschnittstemperatur:  ", temperature_avg)

    return round(temperature_avg, 1)



def __get_owm_forecast_precipitation(json_data, days, progression):
    """ Calculates the forecast precipitation from OpenWeatherMap.org data.

    This private function calculates the temperature precipitation from the OpenWeatherMap.org data.
    The result depends on the progression factor and the number of forecast days.

    Args:
        json_data:  json formatted OpenWeatherMap weather forecast
        days:  number of days 
        progression:  progression factor 

    Returns:
        float:  forecast precipitation
    """


    # confirm that 'progression' is in the allowable range and fix it if required
    # values outside this range do not make sense
    if progression < 0.8:
        progression = 0.8
    if progression > 0.92:
        progression = 0.92 

    data = json_data
    
    precipitation_avg = 0
    remainder = 1 - progression

    # Run the loop "days" times
    for i in range(days):

        try:
            precipitation = data["list"][i]["rain"]
        except KeyError:
            precipitation = 0

        print("Niederschlag an der Stelle ", str(i), ":  ", precipitation)
        # Following equation has been provided by user Manul in the german Raspberry Pi forum
        # http://www.forum-raspberrypi.de/Thread-python-benoetige-hilfe-bei-formeln-in-einer-schleife?pid=293772#pid293772
        precipitation_avg += precipitation * (progression + remainder * (i==days-1)) * remainder**i
        print("Aktueller Durchschnittsniederschlag:  ", precipitation_avg)

    return round(precipitation_avg, 1)



def __download_dwd_zipfile():
    """ Downloads the zipfile from Deutscher Wetterdienst FTP server.

    This private function downloads the zipfile with recent precipitation data from 
    the Deutscher Wetterdienst FTP server.
        
    Returns:
        str:  path to zipfile
    """

    import settings, wget
    
    # Read 'dwd_zipfile_url' setting from settings.ini file
    dwd_settings = settings.get_dwd_settings()
    dwd_zipfile_url   = dwd_settings[0]
    dwd_zipfile_local = dwd_settings[1]
    print("URL:  ", dwd_settings[0])
    print("Local Path:  ", dwd_settings[1])

    zipfiles = wget.download(url=dwd_zipfile_url)
    print(zipfiles)    
    
    return zipfiles


def __time_of_year():
    """ Gets the weighting factor for the time of the year.

    This private function returns the general weighting factor for the time of year.
    Values are fetched from an dictionary.
        
    Returns:
        float:  weighting factor for time of year
    """
    
    # Step 1:  import modules    
    import datetime
    
    # Step 2:  default assignment
    weighting_factor = 1
    
    # define dictionary with weighting factors per months
    wf_table = {
    "1"  : "0.0", 
    "2"  : "0.0", 
    "3"  : "0.7", 
    "4"  : "0.9", 
    "5"  : "1.1",  
    "6"  : "1.2",  
    "7"  : "1.2",  
    "8"  : "1.3",
    "9"  : "1.2",
    "10" : "1.0",
    "11" : "0.0",
    "12" : "0.0"
    }
    
    # Step 3:  identify current month and read weighting factor from lookup table
    current_month = datetime.datetime.now().month
    weighting_factor = float(wf_table.get(str(current_month)))

    return  weighting_factor



def __get_dwd_recent_precipitation():
    """ Gets the recent precipitation from Deutscher Wetterdienst data.

    This private function gets the recent precipitation from the Deutscher Wetterdienst data.
        
    Returns:
        str:  recent precipitation
    """
    
    return



def calculate_watering_factor():
    """ Calculates the watering factor.

    This function calculates the individual watering factor for the current watering event.
    It considers:
    - recent precipitation from the Deutscher Wetterdienst data
    - forecast precipitation and temperature from OpenWeatherMap data
    - time/season of year
    - watering factor from previous watering event
    - soil condition
        
    Returns:
        float:  watering factor
    """
    
    # Step 1:  import modules
    import settings, json
    
    # Step 2:  Read required settings from settings.ini
    # Read 'days' and 'progression' settings from settings.ini file
    temp = settings.get_owm_forecast_settings()
    days = temp[0]
    progression = temp[1]   
    
    # Read the soil conditions from settings.ini file
    soil_water_capacity = settings.get_soil_settings()
    
    # Step 3:  Fetch all contributors
    # OpenWeatherMap.org forecast data
    json_string = json.loads(__get_owm_jsonstring(days))
    print("DEBUG:   Type json_string: ", type(json_string))
    owm_forecast_precipitation = __get_owm_forecast_precipitation(json_string, days, progression)
    owm_forecast_temperature = __get_owm_forecast_temperature(json_string, days, progression)

    # Deutscher Wetterdienst recent data
    dwd_recent_precipitation = __get_dwd_recent_precipitation()
    
    # season/time of year
    print("DEBUG:   Time of Year factor: ", __time_of_year())
    
    # other items
    print("DEBUG:   OWM Precipitation: ", owm_forecast_precipitation)
    print("DEBUG:   OWM Temperature: ", owm_forecast_temperature)
    print("DEBUG:   DWD Precipitation: ", dwd_recent_precipitation)


    return



if debug:
    calculate_watering_factor()


