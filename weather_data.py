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


def __get_owm_forecast_temperature(json_data=None):
    """ Calculates the forecast temperature from OpenWeatherMap.org data.

    This private function calculates the temperature forecast from the OpenWeatherMap.org data.
    The result depends on the progression factor and the number of forecast days.

    Args:
        json_data:  json formatted OpenWeatherMap weather forecast (optional)

    Returns:
        str:  forecast temperature
    """

    import settings

    # Read 'days' and 'progression' settings from settings.ini file
    temp = settings.get_owm_forecast_settings()
    days = temp[0]
    progression = temp[1]

    # confirm that 'progression' is in the allowable range and fix it if required
    # values outside this range do not make sense
    if progression < 0.8:
        progression = 0.8
    if progression > 0.92:
        progression = 0.92

    if json_data==None:
        import json
        data = json.loads(__get_owm_jsonstring(days))
    else:
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



def __get_owm_forecast_precipitation(json_data=None):
    """ Calculates the forecast precipitation from OpenWeatherMap.org data.

    This private function calculates the temperature precipitation from the OpenWeatherMap.org data.
    The result depends on the progression factor and the number of forecast days.

    Args:
        json_data:  json formatted OpenWeatherMap weather forecast (optional)

    Returns:
        str:  forecast precipitation
    """

    import settings

    # Read 'days' and 'progression' settings from settings.ini file
    temp = settings.get_owm_forecast_settings()
    days = temp[0]
    progression = temp[1]

    # confirm that 'progression' is in the allowable range and fix it if required
    # values outside this range do not make sense
    if progression < 0.8:
        progression = 0.8
    if progression > 0.92:
        progression = 0.92
    
    if json_data==None:
        import json
        data = json.loads(__get_owm_jsonstring(days))
    else:
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



def __get_dwd_recent_precipitation():
    """ Gets the recent precipitation from Deutscher Wetterdienst data.

    This private function gets the recent precipitation from the Deutscher Wetterdienst data.
        
    Returns:
        str:  recent precipitation
    """
    
    return



if debug:
    progression = 0.8
    import json
    owm_data = json.loads(__get_owm_jsonstring(2))      
    print("DEBUG:  Progression:  ", progression,  " ;  Temperature Average:  ", __get_owm_forecast_temperature(owm_data), "degree C")    
    print("DEBUG:  Progression:  ", progression,  " ;  Precipitation Average:  ", __get_owm_forecast_precipitation(owm_data), "liters per square meter")
    __download_dwd_zipfile()


