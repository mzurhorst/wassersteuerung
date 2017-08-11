#!/usr/bin/python3
#
#File           :  settings.py
#Author         :  Marcus Zurhorst
#Email          :  marcuszurhorst@gmail.com
#License        :  MIT License
#Copyright      :  (c) 2017 Marcus Zurhorst
#
#Description    :  This module provides functions to read/write settings
#                  for the different water circuits from/to an INI file.

# TODO:   Add generic options based on particular soil conditions.
#         E.g., consider more days when soil keeps humidity.


# Define whether or not debug messages shall be printed
# debug = False     # debug messages surpressed
debug = True      # debug messages enabled


def get_owm_forecast_settings():
    """ Gets the settings for the OpenWeatherMap.org forecast

    This public function reads the settings for the forecast from the OpenWeatherMap.org data.
    It considers the forecast days and the forecast progression factor.

    Returns:
        []:  list of forecast_days (int), forecast_progression (float)
    """

    import configparser

    list = []

    config=configparser.ConfigParser()
    config.read("settings.ini")


    # initialize variable with default value.
    forecast_days = 0

    try:
        forecast_days = int(config.get("General", "forecast_days"))
    except ValueError:
        # 2 days is a reasonable default setting.
        forecast_days = 2
    list.append(forecast_days)


    # initialize variable with default value.
    forecast_progression = 0
    
    try:
        forecast_progression = float(config.get("General", "forecast_progression"))
    except:
        # 0.85 is a reasonable default setting.
        forecast_progression = 0.85
    list.append(forecast_progression)

    return list



def get_dwd_settings():
    """ Gets the settings for the Deutscher Wetterdienst recent precipitation

    This public function reads the settings for the recent precipitation from the Deutscher Wetterdienst data.
    This contains the path to the data on the DWD FTP server.

    Returns:
        str:  FTP URL to zip file on DWD server
    """

    import configparser

    config=configparser.ConfigParser()
    config.read("settings.ini")

    try:
        dwd_zipfile_url = int(config.get("General", "dwd_zipfile_url"))
    except ValueError:
        # hard-code URL for weather station in Baerl, Germany
        dwd_zipfile_url = 'ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/more_precip/recent/tageswerte_RR_13670_akt.zip'
    
    return dwd_zipfile_url



if debug:
    temp = get_owm_forecast_settings()
    print("value:",temp[1], ":", type(temp[1]))
    url = get_dwd_settings()
    print(url)



#print("Beschreibung für Ventil 1 (vor Update): ", config.get("Valve1", "description"))

#if config.getboolean("Valve2", "isactive"):
    #print("Status für Ventil 2:  Aktiviert")
#else:
    #print("Status für Ventil 2:  Nicht aktiviert")


#togglevar = config.get("Valve1", "description")
#if togglevar == "Rasen":
    #togglevar = "Aktualisierte Beschreibung"
#else:
    #togglevar = "Rasen"

#config.set("Valve1", "description", togglevar)

#print("Beschreibung für Ventil 1 nach Update: ", config.get("Valve1", "Description"))


#configfile = open("settings.ini", 'w')
#config.write(configfile)
#configfile.close()
