# Tutorial 2

## Munging public data sets

Some data you have to fight for, but quite a bit of data is available in 
easy-to-use formats like CSV and all you have to do is point and click.  CSV
(or comma-separated values) is a common way we can encode tabular data (tables
with rows and consistent columns, like spreadsheets) and Python has some pretty
good tools for exploring and munging these kinds of data, once you load them in.

In this tutorial, we'll work with a dataset of baby names tabulated by the
Social Security Administration, and you're going to help me find a name for a
future child.  As an extension, you'll analyze the popularity of your own name
(or one of your choice) over time and across the 50 states.

### Baby Names Data

My wife and I are expecting a new baby this year, so baby names have been on 
my mind.  Fortunately, there's a great dataset out there that might help me to
assuage my curiosity.  The U.S. Social Security Administration has been issuing
Social Security numbers (SSNs) to newborns for decades now, and their data can
therefore be used to track the number of births as well as trends in naming.  

The data from 1880 to 2014 is available [here](http://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-level-data).

A subset of the data broken down by state from 1910 to 2014 can be found [here](http://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-data-by-state-and-district-of-)

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
  
Notice that the engine for these graphics is `matplotlib`, the same thing
we used in the previous tutorial for our plots.  Many of the popular packages
used in data analytics, such as `pandas` and `matplotlib`, are pretty tightly
integrated and rely on each other.  For that reason, a distribution of Python
like Anaconda, which has all of these popular packages pre-installed, can be
very helpful in getting started with data analysis. 
  
Here's a question: What were the top names in 1880?  We can sort the DataFrame 
by the "number" column and use the `tail()` method to display the last 5 
rows.  (This is just the opposite of what `head()` does.)

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

The data from 1880 is interesting but is just one slice of a very rich time
series.  Let's get all of the other data into memory so we can start to do some
analysis of it.  The way we'll do this is to loop through the numbers from
1880 to 2014 (or whatever is the latest year of data at the time you're
reading this), read the corresponding data file as a DataFrame, and stash that
DataFrame into a big list.  At the end of that, we'll **concatenate** (combine)
all the yearly data into one big DataFrame.  

In order for us to later tell
which data is from which year, we'll add a new column to each intermediate
DataFrame for the year.

    data_chunks = []
    for y in range(1880,2015): # don't be fooled; this gives us y=1880 to y=2014
        filename = "names/yob" + str(y) + ".txt" # str() converts number to text
        year_y_data = pd.read_csv(filename,names=["name","sex","number"])
        year_y_data["year"] = y 
        data_chunks.append(year_y_data)

    names = pd.concat(data_chunks, ignore_index=True)

If you explore this dataset, you'll see that it takes up about 70 megabytes
of computer memory; enough that analytical functions may take a few seconds,
but probably not enough to put you out of business.

    In [10]: names.info()
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 1825433 entries, 0 to 1825432
    Data columns (total 4 columns):
    name      object
    sex       object
    number    int64
    year      int64
    dtypes: int64(2), object(2)
    memory usage: 69.6+ MB
    
We have four columns to work with: name, sex, number, and year.  For
any given analysis, we may only be interested in one or a few of these, so 
it is convenient that `pandas` gives us a **pivot table** 
function. Essentially this allows us to re-arrange the data table with our 
selection
of rows and column headings, and aggregate (e.g. sum or average) the values
to conform to those dimensions. To sum up the number of births in each year, 
for example, try this:

    In [11]: names.pivot_table("number",index="year",aggfunc=sum)

This can be plotted as a line graph by simply appending `.plot()` after it:

    In [12]: names.pivot_table("number",index="year",aggfunc=sum).plot()
    Out[12]: <matplotlib.axes._subplots.AxesSubplot at 0x1fac71d0>
    
![Fig. 2.3: Births per year](/images/ch2_birthsperyear.png)

In addition to being able to do calculations on columns, as we did with the 
1880 data, pandas allows us to do calculations on entire DataFrame objects,
especially if they have the same dimensionality.  In order to generate the
time series of a name's *proportion* of births, we can use `pivot_table()` to
create a new DataFrame with the time series of occurences of that name, another
new DataFrame with the time series of total births, and divide one by
the other:

    nameseries = names.pivot_table("number",index="year",
                                   columns="name",aggfunc=sum)
    # nameseries has 1 row per year, 1 column per name
    josephseries = nameseries["Joseph"]
    # josephseries has 1 row per year, but only one column
    totalseries = names.pivot_table("number",index="year",
                                    aggfunc=sum)
    # totalseries has the same dimensionality but sums all births
    (josephseries/totalseries).plot(title="Proportion named Joseph, 1880-2014")

![Fig. 2.4: Proportion named Joseph, 1880-2014](/images/ch2_propnamedjoe.png)

It's also possible to divide a DataFrame by another DataFrame that does *not*
have the same dimensionality, in which case the second term (the divisor) will
be repeated or "broadcasted" as needed.  By default, rows will be divided by
rows.  If we want to divide the columns of `nameseries` by the 1-column 
`totalseries`, to generate the time series of name proportion for *all* names
at the same time, we have to use the `.div()` function as a workaround:

    propseries=nameseries.div(totalseries,axis="index")

The resulting DataFrame, `propseries`, has one column for each name, one
row for each year (the same dimensions as `nameseries`), so we can select one
or more columns at the same time.  Now, on to my problem: When naming our 
first three children, I aimed for "old-fashioned" names that
were still well-known enough that people would know how to spell them.  How
well did I do?  Here's how you'd plot a time series for my oldest, Kermit:

    propseries["Kermit"].plot()

Remember that in this pivot table, each name has a column of its own, so we're
using the name as an index to pick the column we want to plot.  If we want 
to plot more than one name, we could use a Python list of indices.  That means 
one more pair of `[` square brackets `]`:

    propseries[["Kermit","Declan","Virginia"]].plot() # hard to compare
    
![Fig. 2.5: My kids' names](/images/3kidsnames.png)

This plot is hard to analyze because my daughter's name is overhwelmingly more
popular than either of my sons'. I'm not interested in the total popularity
so much as the rise and fall of these names, so I'd rather plot them with 
different y-axis scales if it makes the trends more visible.  Adding a couple
of arguments to the `plot()` method gives me a bigger graphic and splits it
into subplots:

    propseries[["Kermit","Declan","Virginia"]].plot(subplots=True,
                                                    figsize=(12,6))

![Fig. 2.6: Historical trends of my kids' names](/images/3kidstrends.png)

I notice that Kermit's and Virginia's names both peaked around 1920, but I 
completely missed my aim with Declan's name, which seems to have become very
recently fashionable.  (At least in this U.S. data.  Maybe it's considered
old-fashioned in Ireland!)
 
## Looking For a Good Old Boy's Name

Here, then, is what I'm looking for: a name for a boy that was popular in the
past but is much less popular now.  I'll start by adding two new columns to the
`names` data, one for the change in *number* of kids with a name, and one for
the change in *proportion*.

First, we'll subset the data to just the boys.  DataFrames can be indexed
in an interesting way: by True/False expressions (called Boolean 
expressions).  Python will interpret `names.sex=="M"` as a sequence of True
and False values the same length as `names.sex`, with True for each position in
the sequence that corresponds to a value of "M".  This sequence of True/False
values can be used as an index to return a subset of the original DataFrame:

    boys=names[names.sex=="M"]

We'll use this principle again to pick out just two years to compare.  Since
my data goes to 2014, and a hundred years is a good round number, I'll compare
the 1914 and 2014 data to decide which names have fallen in popularity.  The
"pipe" character (`|`) means "or", so the following statement will yield rows
where the year is 1914 *or* 2014.

    boys14=boys[(boys.year==1914)|(boys.year==2014)] 

We pivot the data so that there is one row per name with two columns (the
1914 and 2014 values) per row.  We add the `.dropna()` method to drop all rows
with `NaN` ("not a number") values, hence keeping only the names that were
known in both 1914 and 2014:
    
    boyscompared=boys14.pivot_table("prop",index="name",
                                    columns="year").dropna()

Let's look at these names as proportions of boy names.  We can
calculate the total number of boys in each year from the `names` 
DataFrame, and do a quick division to create new columns for `boyscompared`:

    # figure these out as proportions of boys only
    totalboys1914=names.number[(names.sex=="M")&(names.year==1914)].sum()
    totalboys2014=names.number[(names.sex=="M")&(names.year==2014)].sum()
    boyscompared["1914p"]=boyscompared[1914]/totalboys1914
    boyscompared["2014p"]=boyscompared[2014]/totalboys2014

Check our work at the console:

    In [13]: boys_compared.head()
    Out[13]: 
    year      1914  2014     1914p     2014p
    name                                    
    Aaron      485  7334  0.000741  0.003857
    Abbott      13    47  0.000020  0.000025
    Abe        225    56  0.000344  0.000029
    Abel        51  2551  0.000078  0.001342
    Abelardo     6    53  0.000009  0.000028

I'll add two calculated columns: one for the absolute change (or "delta")
in a name's
percentage of births, and one for the relative change.  These are calculated
like so:

    boyscompared["delta"]=boyscompared["1914p"]-boyscompared["2014p"]
    boyscompared["reldelta"]=boyscompared["delta"]/boyscompared["1914p"]

Now the question that remains is: which of these comparisons is most useful for
my purposes?  We can sort and inspect the results with methods I've shown you
previously.  First, the names that have declined most in absolute terms:

    In [14]: boyscompared.sort("absdelta").tail()
    Out[14]: 
    year      1914   2014     1914p     2014p     delta  reldelta
    name                                                         
    George   17603   2988  0.026885  0.001571  0.025313  0.941547
    Robert   21188   6572  0.032360  0.003456  0.028903  0.893187
    James    26263  14301  0.040111  0.007521  0.032589  0.812484
    William  29756  16687  0.045446  0.008776  0.036669  0.806884
    John     37948  10600  0.057957  0.005575  0.052382  0.903809

Surprisingly, we see five of what seem like the most common boys' names leading
the list.  These are by no means old-fashioned names that have gone out of 
style.  What could be the reason for these to appear to have fallen in 
popularity?  The answer, it turns out, is that Americans have tended toward
much greater diversity of naming in recent years than in the past.  In 1900,
for example, only 25 boys' names accounted for half of all births, but now 
naming is much more diverse.[^namediversity]

[^namediversity]: Wes McKinney's handy 2013 book *Python for Data Analysis*
    shows you how to use `pandas` to find this result yourself from the Social
    Security Administration data, and I heartily
    recommend it.
    
What about those names that have declined in *relative* popularity?  Well here
we find some interesting old-fashioned sounding choices in the top 25:

    In [15]: boyscompared.sort("reldelta").tail(25)
    Out[15]: 
    year       1914  2014     1914p     2014p     delta  reldelta
    name                                                         
    Alva        178     6  0.000272  0.000003  0.000269  0.988392
    Claude     1284    42  0.001961  0.000022  0.001939  0.988736
    Cleo        215     7  0.000328  0.000004  0.000325  0.988788
    Woodrow    1785    57  0.002726  0.000030  0.002696  0.989004
    Norbert     288     9  0.000440  0.000005  0.000435  0.989239
    Elbert      450    14  0.000687  0.000007  0.000680  0.989287
    Earle       194     6  0.000296  0.000003  0.000293  0.989350
    Herman     2430    73  0.003711  0.000038  0.003673  0.989655
    Kermit      401    12  0.000612  0.000006  0.000606  0.989695
    Thurman     241     7  0.000368  0.000004  0.000364  0.989998
    Bob         217     6  0.000331  0.000003  0.000328  0.990478
    Ellsworth   219     6  0.000334  0.000003  0.000331  0.990565
    Earl       3842   103  0.005868  0.000054  0.005814  0.990768
    Willard    1302    34  0.001989  0.000018  0.001971  0.991007
    Fred       4441   109  0.006783  0.000057  0.006725  0.991548
    Homer      1152    28  0.001759  0.000015  0.001745  0.991630
    Herbert    3253    74  0.004968  0.000039  0.004929  0.992166
    Orville     787    17  0.001202  0.000009  0.001193  0.992561
    Ed          286     6  0.000437  0.000003  0.000434  0.992776
    Hyman       336     7  0.000513  0.000004  0.000509  0.992826
    Seymour     245     5  0.000374  0.000003  0.000372  0.992972
    Adolph      418     8  0.000638  0.000004  0.000634  0.993409
    Wilbur     1248    23  0.001906  0.000012  0.001894  0.993654
    Loyd        312     5  0.000477  0.000003  0.000474  0.994481
    Carroll     382     6  0.000583  0.000003  0.000580  0.994591

These look like the kinds of names I've been looking for, and the fact that 
my oldest son's name is in the list confirms it.  These names may never have 
been extremely popular, but what is clear is that they were more popular
in 1914 than they are today by multiple orders of magnitude (over 100x).

To examine these names further, what I might do is simply extract the first
five names into a list, and use this list to plot time series as before:

    best5 = list(boyscompared.sort("reldelta").tail().index)
    propseries[best5].plot(subplots=True,figsize=(12,10),
                           title="Trends in five names")
    
![Fig. 2.7: Historical trends of five names](/images/best5namesplot.png)

Well, I'm definitely not naming him Adolph, but there's great food for thought
here.  Can you repeat this analysis but for girls' names?

## Extending this Exercise

There's another, related dataset provided by the Social Security 
Administration which breaks down the names by states.  It would be interesting
to see how much the popularity of a name varies across the states and over 
time.  Maybe some names are about equally popular everywhere, while others are
regional.

Your homework, should you choose to accept it, is to download the *state-level
data set* and conduct an analysis on your name, or any name you like.  The
files in this dataset are named for the states, so you'll need a new way to
loop through all of them and load the data.  One way to do this is to use the
`os` package to get the list of filenames in the "namesbystate" folder.  You'll
also need to use a Python "`if`" statement to filter out the PDF or any other
non-data files included.  Here's an example:

    import pandas as pd
    import os
    statesdata=[]
    files=os.listdir("namesbystate")
    for f in files:
        if f.endswith(".TXT"):
            state = pd.read_csv("namesbystate/"+f,
                                names=["state","sex","year","name","num"])
            statesdata.append(state)
    names = pd.concat(statesdata, ignore_index=True)
  
Load all the data into Python and try to do the following:

1. First, plot the changing popularity of the name between 1910 and 2014, using
    the state-level data.  You can calculate this by adding up the numbers of
    babies given this name in all 50 states (and DC), then dividing by the 
    total of *all* births. 

    Hint: If you can use `.pivot_table()` or another trick to create two
    DataFrames of the same dimensions, you can then divide one by the other to
    produce a third DataFrame containing the result.
    
    ![Fig. 2.8: Example solution](/images/joseph_trend.png)

2. Next, try to create a box plot of the distribution of popularity in a given
    year, such as the year you were born. This means you need the popularity
    *per state*, which is different from the previous challenge.  For each
    name, there will be 51 fractional values.  A box plot (or box-and-whisker 
    plot) shows how those popularity values are distributed.
    
    Hint: One "box" is generated for each *column* of a DataFrame.  If your
    data has years as *row* names, you may need to **transpose** the data 
    (flip rows to columns) before plotting it.  As you may guess, all
    DataFrames have a `.transpose()` method for this.
    
    ![Fig. 2.9: Example solution](/images/joseph_1yearbox.png)

3. Finally, produce a time series of box plots of your name's popularity in
    the fifty states over a 20-year period from 1995 through 2014.  This is
    the same analysis as above, but for more than one year.  See figure 2.9
    as an example.
    
    Hint:  Add the argument "`rot=90`" to the `.plot()` method if you want to
    rotate the x-axis labels as I did in this example.

    ![Fig. 2.10: Example solution](/images/joseph_trendboxes.png)

You should be able to do most of this using `pandas` functionality as 
demonstrated in the tutorial, but you may have to do some hard thinking and
trial-and-error in manipulating the data.  If you need to see the `pandas`
documentation, visit [pandas.pydata.org](
http://pandas.pydata.org/).

### Grading

If you do this as homework in my class, submit a Python script that
produces a plot like Figure 2.10 for a name of your choice.  Please do not use
my name, Joseph, and do not use a name that doesn't occur in the dataset or is
too rare to produce a result like Figure 2.10.

(You are free to embellish it or improve the style, as long as it has 
the right data. Make sure the
plot has a title that tells me which name it is based on.  I will run my own
version of the code and see if I get the same graphic for the given name.

Make sure
your name and student number are provided in a comment near the top of the
code file.

