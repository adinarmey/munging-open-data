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
#MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER.mongolab.com:PORT/DATABASE"
MONGO_URL = "mongodb://joe:root@ds051933.mongolab.com:51933/cis355sandbox"
client = MongoClient(MONGO_URL)
db = client.get_default_database()

# test some database operations
db.mycollection.insert_one({"answer":42})
x = db.mycollection.insert_one({"question":"to be or not to be"})
db.mycollection.find_one({"_id":x.inserted_id})
db.mycollection.find_one({"_id":x.inserted_id},{"_id":False})
# try out some more complex queries
heroes = [  {'name':'Batman', 'secret identity':'Bruce Wayne',
             'portrayals': [ {'year':1989,'actor':'Michael Keaton'},
                             {'year':1995,'actor':'Val Kilmer'},
                             {'year':1997,'actor':'George Clooney'},
                             {'year':2005,'actor':'Christian Bale'},
                             {'year':2016,'actor':'Ben Affleck'} ] },
            {'name':'Superman', 'secret identity':'Clark Kent',
             'portrayals': [ {'year':1978,'actor':'Christopher Reeve'},
                             {'year':2006,'actor':'Brandon Routh'},
                             {'year':2013,'actor':'Henry Cavill'} ] },
            {'name':'Aquaman', 'secret identity':'Arthur Curry',
             'portrayals': [ {'year':2016, 'actor':'Jason Momoa'} ] },
            {'name':'Antman','secret identity':'Hank Pym',
             'portrayals': [ {'year':2015, 'actor':'Michael Douglas'},
                             {'year':2015, 'actor':'Paul Rudd'} ] }  ]
db.heroes.insert_many(heroes)
db.heroes.find_one({"name":"Aquaman"},{"_id":0})
list( db.heroes.find({"name":{"$gte":"B"}},{"_id":0}) )
db.heroes.find({"portrayals.actor":"Christopher Reeve"},{"_id":0})
db.heroes.find({"portrayals.year":{"$gte":2000,"$lt":2010}},{"_id":0})
db.heroes.find({"portrayals.year":{"$gte":2000,"$lt":2010}},
               {"_id":0,"name":1,"portrayals.$":1})
db.heroes.find({},{"_id":0,"name":1,"secret identity":1})
# clean up
db.mycollection.drop()
db.heroes.drop()


#db.mycollection.find_one() # this should retrieve the data just inserted
#db.mycollection.drop() # this should delete the collection we just created
#db.mycollection.find_one() # this should return nothing because the data is gone




# Get the distance from a zip code to my office building from the Google Maps
# Distance Matrix API; you'll need to apply for a free API key first.

import requests
import json
# your API key
mykey="AIzaSyCEqH1F0f7kHhVvn8YqBgMVMFi6x4Fb_4g"
fro="Tempe, AZ"
to="Disneyland"
re = requests.get(
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins="+fro+"&destinations="+to+"&key="+mykey)
r = json.loads(re.content.decode())
# pretty-print the output
print(json.dumps(r,indent=2))

# a less cluttered version of the data, suitable for storage
d = {"origin":r["origin_addresses"][0],
     "duration":r["rows"][0]["elements"][0]["duration"]["value"],
     "distance":r["rows"][0]["elements"][0]["distance"]["value"] }
print(json.dumps(d,indent=2))




# Now we've proven both the Google API and that we can connect to
# our MongoDB database instance.  I've provided a file full of 
# Arizona zip codes.  Read this file as a CSV, loop through it,
# and store the distance data for each zipcode in the database.

import pandas as pd
zips = pd.read_csv("AZ_zipcodes.csv",names=["zip"],dtype="str")


# now load our database from the Google API
from pymongo import MongoClient
import requests
import json
# make the database connection
MONGO_URL = "mongodb://joe:root@ds051933.mongolab.com:51933/cis355sandbox"
client = MongoClient(MONGO_URL)
db = client.get_default_database()
# set the fixed URL paramaters
to="300 E Lemon St, Tempe AZ" # the author's office building
mykey="AIzaSyCEqH1F0f7kHhVvn8YqBgMVMFi6x4Fb_4g"
# drop the data collection, in case you need to re-run this code
db.routes.drop()
# now do the following for every zip code
for z in zips.zip:
    # get the data from Google
    re = requests.get(
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins="+z+"&destinations="+to+"&key="+mykey)
    r = json.loads(re.content.decode())
    if "distance" in r["rows"][0]["elements"][0].keys(): # error check
        d = {"zip":z,
             "origin":r["origin_addresses"][0],
             "duration":r["rows"][0]["elements"][0]["duration"]["value"],
             "distance":r["rows"][0]["elements"][0]["distance"]["value"] }
        db.routes.insert_one(d)
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
