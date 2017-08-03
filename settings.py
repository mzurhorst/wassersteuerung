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


def get_forecast_settings():
	""" Gets the settings for the forecast

	This public function reads the settings for the forecast from the OpenWeatherMap.org data.
	It considers the forecast days and the forecast progression factor.

	Returns:
	    []:  list of forecast_days (int), forecast_progression (float)
	"""

	import configparser
	
	list = []
	
	config=configparser.ConfigParser()
	config.read("settings.ini")
	
	
	try:
		forecast_days = int(config.get("General", "forecast_days"))
	except ValueError:
		# 2 days is a reasonable default setting.
		forecast_days = 2
	list.append(forecast_days)


	try:
		forecast_progression = config.get("General", "forecast_progression")
	except ValueError:
		# 0.85 is a reasonable default setting.
		foreacast_progression = 0.85
	list.append(forecast_progression)
	
	return list


get_forecast_settings()




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
