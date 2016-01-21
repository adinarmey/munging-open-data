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
names1880.head() # shows the first 5 rows
names1880.info() # some info about the data types and length




