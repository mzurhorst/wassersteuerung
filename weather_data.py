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

#from my_credentials import  owm_apikey
# this section is here because I dislike to expose my personal API key on Github.com
try:
    from my_credentials import  owm_apikey
    print("OpenWeatherMap.org API Key:  ",  owm_apikey)
except ImportError:
    owm_apikey = "your_owm_apikey"
    print("Please create 'my_credentials.py' file with variable 'owm_apikey'")
    print("Visit http://api.openweathermap.org for details.")

# assemble the OpenWeatherMap API key in the JSON URL
owm_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=2953308&appid=' + owm_apikey + '&units=metric&lang=de&cnt=3'
print("-- Phase 1: Initialisieren:  --")



#past_json= 'http://api.openweathermap.org/data/2.5/forecast/daily?id=2953308&appid=b8ee3e33f288f292b85b1d3b139d8f30&units=metric&lang=de&cnt=3'
print("-- Phase 2: JSON Download mit requests:  --")

import requests
r = requests.get(url=owm_url)
print(r.json())


# commented because I don't want to download the zip file for each test
# TODO:  wrap this into functions and call from main.py on demand

#import wget
#dwd_zipfile_url = 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/more_precip/recent/tageswerte_RR_13670_akt.zip'
#fs = wget.download(url=dwd_zipfile_url)
#
#print(fs)
