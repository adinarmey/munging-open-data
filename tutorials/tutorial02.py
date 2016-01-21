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



# now get all the years 1880-2014 into memory
data_chunks = []
for y in range(1880,2015): # don't be fooled; this gives us y=1880 to y=2014
    filename = "names/yob" + str(y) + ".txt" # str() converts number to text
    year_y_data = pd.read_csv(filename,names=["name","sex","number"])
    year_y_data["year"] = y
    year_y_data["prop"] = year_y_data.number/(year_y_data.number.sum())
    data_chunks.append(year_y_data)
# now data_chunks contains a whole list of DataFrames, one per year,
# so let's concatenate them together into one big one...
names = pd.concat(data_chunks, ignore_index=True)

# plot total births over time    
names.pivot_table("number",rows="year",aggfunc=sum).plot()

# pivot table to plot rise and fall for individual names
names_series = names.pivot_table("prop",rows="year",cols="name",aggfunc=sum)
# the only actual "sum" that will be taken is if a certain name appears
# twice in the same year's data, once for boys and once for girls

# plot my kids' names
names_series[["Kermit","Declan","Virginia"]].plot() # hard to compare
# now a bigger plot with different scales
names_series[["Kermit","Declan","Virginia"]].plot(subplots=True,figsize=(12,6))

# begin our search for good boys' names by subsetting just the boys
boys=names[names.sex=="M"]
# x%100 means the *remainder* when you divide x/100
# so the following gives you both years where that is 14 (1914 and 2014)
boys_compared=boys[boys.year%100==14] 
#boys_comparison=boys[(boys.year==1914)|(boys.year==2014)] # this also works

# create two columns (1914 and 2014) for each name; and drop all NA values
# so we just keep the names that were known in both years
boys_compared=boys_compared.pivot_table("prop",rows="name",
  cols="year").dropna()
# create two "delta" columns -- one for the absolute drop in popularity
# and one for its relative change in popularity
boys_compared["absdelta"]=boys_compared[1914]-boys_compared[2014]
boys_compared["reldelta"]=boys_compared["absdelta"]/boys_compared[1914]

#to check out the names that have declined the most in popularity
boys_compared.sort("absdelta").tail()
boys_compared.sort("reldelta").tail(25)

# get a list of 5 names to try plotting
best5 = list(boys_compared.sort("reldelta").tail().index)
names_series[best5].plot(subplots=True,figsize=(12,10),title="Trends in five names")
