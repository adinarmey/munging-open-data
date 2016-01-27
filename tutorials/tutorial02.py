# -*- coding: utf-8 -*-
"""
Tutorial 02 from "Munging Open Data"
https://leanpub.com/munging-open-data
https://github.com/joeclark-phd/munging-open-data
Created on Wed Jan 20 14:59:00 2016

@author: Joseph Clark
"""

# Baby names data (national level) available from Data.gov:
# http://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data
# This script is meant to be run in a parent folder of the unzipped
# "names" directory.

# Three ways to read a CSV file into Python
#
# 1. With the standard library's "open" command:
#f = open("names/yob1880.txt","r")
#names,sexes,counts=[],[],[] # create 3 empty lists
#for line in f.readlines():
#    line = line.strip().split(",")
#    names.append(line[0])
#    sexes.append(line[1])
#    counts.append(line[2])
#f.close() # close the file

# 2. With the "csv" library
#import csv
#
#f = open("names/yob1880.txt","r")
#names,sexes,counts=[],[],[] # create 3 empty lists
#reader = csv.reader(f)
#for row in reader:
#    names.append(row[0])
#    sexes.append(row[1])
#    counts.append(row[2])
#f.close() 

# 3. With "pandas"
import pandas as pd
names1880 = pd.read_csv("names/yob1880.txt",names=["name","sex","number"])

# commands to run at the console to inspect the dataset
names1880.head() 
names1880.info() 
names1880.sex.value_counts()
names1880.number.sum()
names1880.groupby("sex").sum()
names1880.groupby("sex").sum().plot(kind="bar")
names1880.sort("number").tail()

# create a new column for the proportion of the population with each name
names1880["prop"]=names1880.number/(names1880.number.sum())







# Here's one way to load all the years 1880-2014 into memory.
data_chunks = []
for y in range(1880,2015): # don't be fooled; this gives us y=1880 to y=2014
    filename = "names/yob" + str(y) + ".txt" # str() converts number to text
    year_y_data = pd.read_csv(filename,names=["name","sex","number"])
    year_y_data["year"] = y
    data_chunks.append(year_y_data)
# now data_chunks contains a whole list of DataFrames, one per year,
# so let's concatenate them together into one big one...
names = pd.concat(data_chunks, ignore_index=True)

# names.info()

# plot total births over time    
names.pivot_table("number",index="year",aggfunc=sum).plot()


nameseries = names.pivot_table("number",index="year",columns="name",aggfunc=sum)
# nameseries has 1 row per year, 1 column per name
josephseries = nameseries["Joseph"]
# josephseries has 1 row per year, but only one column
totalseries = names.pivot_table("number",index="year",aggfunc=sum)
# totalseries has the same dimensionality as josephseries, but sums all births
(josephseries/totalseries).plot(title="Proportion named Joseph, 1880-2014")


#all names as proportions of births over all years
propseries=nameseries.div(totalseries,axis="index")

#propseries["Kermit"].plot()

# plot my kids' names
propseries[["Kermit","Declan","Virginia"]].plot() # hard to compare
# now a bigger plot with different scales
propseries[["Kermit","Declan","Virginia"]].plot(subplots=True,figsize=(12,6))

# begin our search for good boys' names by subsetting just the boys
boys=names[names.sex=="M"]
# now subset just those rows of data from 1914 and 2014
boys14=boys[(boys.year==1914)|(boys.year==2014)] 
#boys14=boys[boys.year.isin([1914,2014])] # this also works
#boys14=bosy[boys.year%100==14] # this too...

# create two columns (1914 and 2014) for each name; and drop all NA values
# so we just keep the names that were known in both years
boyscompared=boys14.pivot_table("number",index="name",
                                columns="year").dropna()
# figure these out as proportions of boys only
totalboys1914=names.number[(names.sex=="M")&(names.year==1914)].sum()
totalboys2014=names.number[(names.sex=="M")&(names.year==2014)].sum()
boyscompared["1914p"]=boyscompared[1914]/totalboys1914
boyscompared["2014p"]=boyscompared[2014]/totalboys2014

# create two "delta" columns -- one for the absolute drop in popularity
# and one for its relative change in popularity
boyscompared["delta"]=boyscompared["1914p"]-boyscompared["2014p"]
boyscompared["reldelta"]=boyscompared["delta"]/boyscompared["1914p"]

#to check out the names that have declined the most in popularity
boyscompared.sort("delta").tail()
boyscompared.sort("reldelta").tail(25)

# get a list of 5 names and try plotting them
best5 = list(boyscompared.sort("reldelta").tail().index)
propseries[best5].plot(subplots=True,figsize=(12,10),
                       title="Trends in five names")
