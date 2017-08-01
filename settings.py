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


import configparser

config=configparser.ConfigParser()
config.read("C:\Data\FISCH00M\Python_Workspace\Gartenbewässerung\settings.ini")
print(config.sections())

print("Beschreibung für Ventil 1 (vor Update): ", config.get("Valve1", "Description"))

if config.getboolean(print("Valve2", "IsActive"):
	print("Status für Ventil 2:  Aktiviert")
else:
	print("Status für Ventil 2:  Nicht aktiviert")


togglevar = config.get("Valve1", "Description")
if togglevar == "Rasen":
    togglevar = "Aktualisierte Beschreibung"
else:
    togglevar = "Rasen"

config.set("Valve1", "Description", togglevar)

print("Beschreibung für Ventil 1 nach Update: ", config.get("Valve1", "Description"))


configfile = open("C:\Data\FISCH00M\Python_Workspace\Gartenbewässerung\settings.ini", 'w')
config.write(configfile)
configfile.close()
