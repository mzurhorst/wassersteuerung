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
        days (int): number of days for weather forecast  (1-3)

    Returns:
        str:  OpenWeatherMap.org JSON string
    """

    import requests

    # assemble the OpenWeatherMap API key in the JSON URL
    # TODO:   Make weather station variable
    owm_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=2953308&appid=' + __get_owm_apikey() + '&units=metric&lang=de&cnt=' + str(days)
    if debug:
        print("DEBUG:   OpenWeatherMap.org URL:   ", owm_url)
        print("DEBUG:   import requests and load JSON string from owm_url")

    # this section will load the JSON object;  type: class requests.models.Response
    r = requests.get(url=owm_url)
    if debug:
        print("Type r:  ",  type(r))
        print("r.JSON Objekt:  ",   r.json())
        print("Type r.text:  ",  type(r.text))

    return r.text


# TODO:  Define functions for the JSON parsing logic

import json

#JSON Beispiel:

data = json.loads(__get_owm_jsonstring(3))



print("---- Abschnitt 3:  Einzelne JSON ELemente suchen ----")

# Erwartete Temperaturen auslesen

try:
    temperature_today = data["list"][0]["temp"]["max"]
except KeyError:
    temperature_today = 15

try:
    temperature_tomorrow = data["list"][1]["temp"]["max"]
except KeyError:
    temperature_tomorrow= 15


# Erwartete Niederschläge auslesen

try:
    rain_today = data["list"][0]["rain"]
except KeyError:
    rain_today = 0.0

try:
    rain_tomorrow = data["list"][1]["rain"]
except KeyError:
    rain_tomorrow = 0.0

print('Wetter, heute:  ', rain_today, 'l/m², ', temperature_today, '°C')
print('Wetter, morgen:  ', rain_tomorrow, 'l/m², ', temperature_tomorrow, '°C')


print("---- Abschnitt 4:  Forecast-Faktor berechnen ----")



def rain_forecast(rain1, rain2):
    rain_total = 0.9 * rain1 + 0.1 * rain2
    return rain_total

variable = rain_forecast(rain_today, rain_tomorrow)

print('Regen, gemittelt:  ', variable, 'l/m²')














# commented because I don't want to download the zip file for each test
# TODO:  wrap this into functions and call from main.py on demand

#import wget
#dwd_zipfile_url = 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/more_precip/recent/tageswerte_RR_13670_akt.zip'
#fs = wget.download(url=dwd_zipfile_url)
#
#print(fs)
