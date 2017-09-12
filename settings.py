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
    This contains:
    - path to the data on the DWD FTP server
    - local path of the zip file
    - local path of the extracted text file with precipitation data

    Returns:
        []:  list of dwd_zipfile_url (str), dwd_zipfile_local (str), dwd_datafile (str)
    """

    import configparser

    list = []

    config=configparser.ConfigParser()
    config.read("settings.ini")

    try:
        dwd_zipfile_url = str(config.get("General", "dwd_zipfile_url"))
    except ValueError:
        # hard-code URL for weather station in Baerl, Germany
        dwd_zipfile_url = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/daily/more_precip/recent/tageswerte_RR_13670_akt.zip"
    list.append(dwd_zipfile_url)

    try:
        dwd_zipfile_local = str(config.get("General", "dwd_zipfile_local"))
    except ValueError:
        # hard-code local path to zip file from DWD server
        dwd_zipfile_local = 'E:\Marcus\Documents\Python Projekte\wassersteuerung\download\tageswerte_RR_13670_akt.zip'
    list.append(dwd_zipfile_local)

    try:
        dwd_datafile = str(config.get("General", "dwd_datafile"))
    except ValueError:
        # hard-code local path to the extracted data file
        dwd_datafile = 'E:\Marcus\Documents\Python Projekte\wassersteuerung\download\dwd_data.txt'
    list.append(dwd_datafile)

    try:
        dwd_recent_days = int(config.get("General", "dwd_recent_days"))
    except ValueError:
        # 2 days is a reasonable default setting.
        dwd_recent_days = 2
    list.append(dwd_recent_days)

    return list



def get_soil_settings():
    """ Gets the settings for the soil condition

    This public function reads the settings for the soil condition.
    This contains a factor (range: 0.8 - 1.2) for the water storage capacity of the soil.

    Returns:
        float:  soil water capacity
    """

    import configparser

    list = []

    config=configparser.ConfigParser()
    config.read("settings.ini")

    try:
        soil_water_capacity = float(config.get("General", "soil_water_capacity"))
    except ValueError:
        # hard-code to 1.0 when value not available
        soil_water_capacity = 1.0

    return soil_water_capacity


if debug:
    temp = get_owm_forecast_settings()
    print("DEBUG: forecast progression: ",temp[1])
    temp2 = get_dwd_settings()
    print("DEBUG: zipfile URL: ", temp2[0])
    print("DEBUG: local path: ", temp2[1])
    print("DEBUG: Soil water capacity factor: ", get_soil_settings())



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
