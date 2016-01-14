# -*- coding: utf-8 -*-
"""
Tutorial 01 from "Munging Open Data"
https://leanpub.com/munging-open-data
https://github.com/joeclark-phd/munging-open-data
Created on Wed Jan 13 20:11:08 2016

@author: Joseph Clark
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
stations = ["9410170","8443970"]
urlroot = ("http://tidesandcurrents.noaa.gov/api/datagetter?"
           "product=water_level&datum=MLLW&date=recent"
           "&units=english&time_zone=gmt&format=json&station=")
san = requests.get(urlroot+stations[0])
bos = requests.get(urlroot+stations[1])
sandata = json.loads(san.content.decode())
bosdata = json.loads(bos.content.decode())
# I actually could have been a whole lot lazier...


# Extract the "v" values for each station
sanmllw = []  # an empty list
for i in sandata["data"]:
    sanmllw.append(i["v"])
    print("I just appended " + i["v"])  # for debugging
bosmllw = []  # an empty list
for i in bosdata["data"]:
    bosmllw.append(i["v"])
    print("I just appended " + i["v"])  # for debugging


# matplotlib is the most popular Python data visualization library
import matplotlib.pyplot as plt

# Run these statements together as a block; if run separately,
# you won't get the plot you want.
plt.plot(sanmllw,"g",bosmllw,"m")
plt.title("San Diego and Boston tides")
plt.ylabel("MLLW")
