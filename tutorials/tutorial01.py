# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 20:11:08 2016

@author: Joseph
"""

import requests    # to get data from the web service
import json        # to parse JSON into Python data structures

# Get San Diego data and parse the JSON
san = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter?"    
                   "product=water_level&datum=MLLW&date=recent"
                   "&units=english&time_zone=gmt&format=json"
                   "&station=9410170")
sandata = json.loads(san.content.decode())

# Lazy Joe wants to avoid writing the whole URL twice
stations = ["9410170","8418150"]
urlroot = ("http://tidesandcurrents.noaa.gov/api/datagetter?"
           "product=water_level&datum=MLLW&date=recent"
           "&units=english&time_zone=gmt&format=json&station=")
san = requests.get(urlroot+stations[0])
pwm = requests.get(urlroot+stations[1])
sandata = json.loads(san.content.decode())
pwmdata = json.loads(pwm.content.decode())
# I actually could have been a whole lot lazier...

