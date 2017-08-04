#!/usr/bin/python3
#
#File           :  garden_timing.py
#Author         :  Marcus Zurhorst
#Email          :  marcuszurhorst@gmail.com
#License        :  MIT License
#Copyright      :  (c) 2017 Marcus Zurhorst
#
#Description    :  This module provides functions to calculate the next
#                  watering durations and manages a FIFO task queue.
#                  It takes recent recent weather and forecast into account and
#                  falls back to time of year (=rough climate) and defaults 
#                  from settings.ini when data is not available.

# Define whether or not debug messages shall be printed
# debug = False     # debug messages surpressed
debug = True      # debug messages enabled