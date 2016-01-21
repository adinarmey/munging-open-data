# Chapter 2

Introduce Kaggle.  Download baby names data.

Use pandas to load the CSV and do summary stats. First total births, then 
total births by year, then male/female ratio by year.

For a given name, plot a time series of count per year.  (More on data viz.)
Now do that as percent of names (of that sex) per year.

Find the top 1000 boys' names and print them in order.
For these names, calculate how much popularity they *lost* from 1915 to 2015
and print them in order from most-lost to least-lost (most gained).

Homework: do a plot of <your name>'s popularity over the past 30 years, with
a box-whisker plot showing the distribution of popularity in the 50 states for
each year.

## Baby Names Data

My wife and I are expecting a new baby this year, so baby names have been on 
my mind.  Fortunately, there's a great dataset out there that might help me to
assuage my curiosity.  The U.S. Social Security Administration has been issuing
Social Security numbers (SSNs) to newborns for decades now, and their data can
therefore be used to track the number of births as well as trends in naming.  

The data from 1880 to 2014 is available here:
http://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data

A subset of the data broken down by state from 1910 to 2014 can be found here:
http://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-data-by-state-and-district-of-

## Loading Data From a File

We'll start by exploring the national data, which you can download from the
web page as a ZIP file containing several files in a CSV (comma-separated
values) format---one file for each year that the dataset includes.  A quick
look inside one of the files (here, `yob1880.txt`), shows that each line of
the file holds a name, a one-letter code for the sex, and the
number of American children given that name in that year.  For those names that
can be given to both boys and girls, two lines will be found in the 
file. Names given to fewer than five children are omitted.

![Fig. 2.1: Sample of data for 1880](/images/babynames_rawdata.png)

There are a number of ways we could read a CSV file into Python.  For example,
we could use the "open" command in the standard library[^stdlib].  In this code
sample, we read the file into a variable, "f", which can be read line by line.
For each line, we `strip()` off the invisible end-of-line whitespace and then
`split()` the line at the commas to make a 3-element list:
    
    f = open("names/yob1880.txt","r")
    names,sexes,counts=[],[],[] # create 3 empty lists
    for line in f.readlines():
        line = line.strip().split(",")
        names.append(line[0])
        sexes.append(line[1])
        counts.append(line[2])
    f.close() # close the file

This code results in three lists of the same length: names, sexes, and counts.
Be aware that the script only works if it is stored in the parent folder of the
unzipped "names" data; you can of course change the reference to the file if 
you want to store the Python script in a different directory relative to the
unzipped data files.

[^stdlib]: The standard library means the set of functions available by default,
    without importing any additional packages or modules.

The second approach is to use the `csv` package, which includes "reader" and
"writer" functions that simplify interacting with CSV files.  Although the code
for this simple task looks almost the same as above, the `csv` package can make
it much simpler to deal with more complex files and different dialects of CSV.

    import csv

    f = open("names/yob1880.txt","r")
    names,sexes,counts=[],[],[] # create 3 empty lists
    reader = csv.reader(f)
    for row in reader:
        names.append(row[0])
        sexes.append(row[1])
        counts.append(row[2])
    f.close() 
    
We will use a third approach today, because it shows off one of the most useful
Python packages for data munging: **`pandas`**.  `Pandas` offers a bunch of 
data types and functions that augment the core of Python and allow us to load,
manipulate, and do basic analysis on data.  Chief among these is the DataFrame,
a data structure that can be thought of as a list of columns or a sort of
spreadsheet in code.  (Users of the R statistical programming language will 
recognize it as an imitator of the good features of R's data.frame type.)

We can load a CSV file into a DataFrame with a one-liner, after importing the
pandas package:

    import pandas as pd
    names1880 = pd.read_csv("names/yob1880.txt",names=["name","sex","number"])

Instead of creating three lists, as the first two methods do, this creates one
DataFrame.  We can access a column by name[^colname], in either of two ways:

    In [1]: names1880["name"]
    
    In [2]: names1880.name  # same thing

To get a quick look at the DataFrame's contents, the `head()` method shows
you five lines of data.  This function is actually a **method**, meaning it 
"belongs to" the DataFrame, and is called by appending the function call to
the variable name (i.e., you couldn't type `head(names1880)` at the console,
but you can type `names1880.head()`).

    In [3]: names1880.head()
    Out[3]: 
            name sex  number
    0       Mary   F    7065
    1       Anna   F    2604
    2       Emma   F    2003
    3  Elizabeth   F    1939
    4     Minnie   F    1746
 
## Summary Statistics

That was just one example of the many functions provided by `pandas` 
for quickly examining a dataset.  Another good one to run when inspecting
a new set of data is the `info()` method, which tells you a bit about the size,
number and data types of the DataFrame's columns.

    In [4]: names1880.info()
       ...:
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 2000 entries, 0 to 1999
    Data columns (total 3 columns):
    name     2000 non-null object
    sex      2000 non-null object
    number   2000 non-null int64
    dtypes: int64(1), object(2)
    memory usage: 62.5+ KB

We might want to do some quick counts of the data values, for example, to see
how many male and female names are in the dataset, with the `value_counts()`
applied to the "sex" column:

    In [5]: names1880.sex.value_counts()
    Out[5]: 
    M    1058
    F     942
    dtype: int64
    
That's how many *names* are in the data, but how many actual babies were born
that year?  As you might have guessed, the relevant method is `sum()`:

    In [6]: names1880.number.sum()
    Out[6]: 201484
    
We can also take the sums of subsets of the data using the `groupby()` method,
not unlike the `GROUP BY` clause in SQL.  For example, if we want the subtotals
of the `number` column for the two sexes:

    In [7]: names1880.groupby("sex").sum()
    Out[7]: 
         number
    sex        
    F     90993
    M    110491

For a visual comparison, we can do a quick bar chart with a few extra
keystrokes:

    In [7]: names1880.groupby("sex").sum().plot(kind="bar")
    Out[7]: <matplotlib.axes._subplots.AxesSubplot at 0x10f62b00>

![Fig. 2.2: A quick visual comparison](/images/ch2_quickbars.png)
    
What were the top names in 1880?  We can sort the DataFrame by the "number"
column and use the `tail()` method to display the last 5 rows.  (This is
just the opposite of what `head()` does.)

    In [8]: names1880.sort("number").tail()
    Out[8]: 
            name sex  number
    945  Charles   M    5348
    944    James   M    5927
    0       Mary   F    7065
    943  William   M    9532
    942     John   M    9655

We may also want to know how common these names are as a percentage of the
total population.  One of my favorite things about `pandas` is that, much like
a spreadsheet, you can easily do calculations on entire data columns that
result in new columns.  In other words, if we want to divide a column by a 
certain number, we don't have to write a loop that does the calculation 
separately on each element, nor do we have to add things up and divide only
the grand total.  We can just do something like the following code, which
creates a new column containing the proportion of babies with each name:

    names1880["prop"]=names1880.number/(names1880.number.sum())

Here's a great example of turning raw data into information that means 
something to us.  Now we can judge just how popular certain names actually
are... and perhaps then check to see if they retain their popularity in later
years.

    In [9]: names1880.sort("prop").tail()
    Out[9]: 
            name sex  number      prop
    945  Charles   M    5348  0.026543
    944    James   M    5927  0.029417
    0       Mary   F    7065  0.035065
    943  William   M    9532  0.047309
    942     John   M    9655  0.047919

## Naming Trends Over Time


    