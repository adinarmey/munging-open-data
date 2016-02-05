# -*- coding: utf-8 -*-
"""
Tutorial 03 from "Munging Open Data"
https://leanpub.com/munging-open-data
https://github.com/joeclark-phd/munging-open-data
Created on Thu Feb 4 2016

@author: Joseph Clark
"""

# pymongo must be installed by going to the "Anaconda command prompt"
# and entering: conda install pymongo
from pymongo import MongoClient

# your database connection URL from MongoLab:
MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER.mongolab.com:PORT/DATABASE"
client = MongoClient(MONGO_URL)
db = client.get_default_database()

# test to see if we can insert data into a collection/table and retrieve it
#db.testtable.insert({"answer":42}) # create a new collection with an insert
#db.testtable.find_one() # this should retrieve the data just inserted
#db.testtable.drop() # this should delete the collection we just created
#db.testtable.find_one() # this should return nothing because the data is gone




# Get the distance from a zip code to my office building from the Google Maps
# Distance Matrix API; you'll need to apply for a free API key first.

# your API key
mykey="YOUR GOOGLE MAPS API KEY, NOT MINE!"
# need a web connection to run this, of course
import requests
import json

# the office address
address="300 E Lemon St, Tempe AZ"
# the zip code to test
testzip="85226"
# do the test
re = requests.get(
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins="+testzip+"&destinations="+address+"&key="+mykey)
r = json.loads(re.content.decode())
# pretty-print the output
print(json.dumps(r,indent=2))
# a less cluttered version of the data, suitable for storage
d = {"zip":testzip,
     "origin":r["origin_addresses"][0],
     "response":r["rows"][0]["elements"]
     }
print(json.dumps(d,indent=2))




# Now we've proven both the Google API and that we can connect to
# our MongoDB database instance.  I've provided a file full of 
# Arizona zip codes.  Read this file as a CSV, loop through it,
# and store the distance data for each zipcode in the database.

import pandas as pd
zips = pd.read_csv("AZ_zipcodes.csv",names=["zip"],dtype="str")


# drop the data collection, in case you need to re-run this code
db.routes.drop()
# now do the following for every zip code
for z in zips.zip:
    # get the data from Google
    re = requests.get(
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins="+z+"&destinations="+address+"&key="+mykey)
    r = json.loads(re.content.decode())
    d = {"zip":z,
         "origin":r["origin_addresses"][0],
         "response":r["rows"][0]["elements"]
         }
    # store in the database (you might want to do some error checking first)
    db.routes.insert(d)
    # let us know progress is being made
    print("processed zip code "+z+"...")

# Now we query the database to get a table of distance (miles) 
# and time (minutes) for each route we analyzed


# Query the database
thedata = db.routes.find({},{"_id":False,
                             "zip":True,
                             "response.distance.value":True,
                             "response.duration.value":True})
# thedata is a "cursor", a kind of list we can iterate through
# but only once.  loop through to create three columns of data
qzips = []
qdist = []
qtime = []                             
for q in thedata:
    qzips.append(q["zip"])
    qdist.append(q["response"]["distance"]["value"])
    qdist.append(q["response"]["duration"]["value"])

# this should combine the lists into a DataFrame
df = pd.DataFrame({"qzips":qzips,"qdist":qdist,"qtime":qtime})

# now plot an XY chart of distance x time
# and add a "dot" and label for the slowest and fastest commute
