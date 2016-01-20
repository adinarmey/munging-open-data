# Tutorial 1 

## Where can we find open data?

The world is full of data made available to the public by governments, 
universities, businesses and nonprofits.  You may find you want to use this 
data for research, analysis, to develop a data driven application or even to 
start a business.  Beginning with this tutorial, we're going to leverage 
open data to practice some Python-based tools for data munging.

Data is being opened up to the public at a rate too fast for any one index
to keep up with it, however, the U.S. government has made a good start by
organizing links to thousands of datasets created by various 
agencies into a search engine and directory called 
[http://www.data.gov](http://www.data.gov).

![Fig. 1.1: Data.gov](/images/datadotgov.png)

Take some time now to browse through the catalog of data available.  We may
find ourselves munging several of these data sources before we're through 
with fifteen tutorials.  If you're not from the U.S., your home country 
probably has something similar.  Two good examples are 
[Canada's open data portal](http://open.canada.ca/en/open-data) 
and [Britain's](https://www.data.gov.uk/).

### Tutorial 1 Data Source: NOAA's Tides and Currents API

[NOAA](http://www.noaa.gov/), the U.S. National Oceanographic and Atmospheric 
Administration is a 
federal agency that collects all sorts of data on weather and the oceans.
Their [Center for Operational Oceanographic Products and 
Services](http://tidesandcurrents.noaa.gov/) (CO-OPS)
happens to have a very easy-to-use data 
[API](http://tidesandcurrents.noaa.gov/api/) (application programming 
interface) that doesn't require any kind of account or key, making it
great for learning the ropes.

We'll write a Python program today that obtains data from this API, over the
Web, and plots a line graph of the changing water levels at CO-OPS stations
on the east and west coasts.  As an extension, you'll extend the time series
to a full month and superimpose the phases of the moon.

## First steps into Python

Python can be used in a number of ways.  You can use it in an 
**interactive mode** in which each line of code is evaluated and run as you 
type it into the terminal.  Alternatively, you can write a **script** in a 
text editor and then
tell Python to read the script and run all of the instructions it contains.
Both modes have their uses; typically you will use the interactive mode to
test things out and, once you have them working, put the code into a script 
so that it can be saved and re-run later.

There are also some integrated development environments (IDEs) that combine a 
text editor for writing scripts with an interactive console for testing and
executing code.  If you installed the Anaconda Python distribution I 
recommended, an excellent free IDE called Spyder should be included with it.

Another compromise between interactive and scripted modes is the IPython
Notebook.  This tool (also included in the Anaconda distribution) is an
interactive interpreter with an HTML (web page) interface that allows you to
annotate and even go back and edit your interactive session in order to
produce a report that can be saved or printed.  This might be useful when 
giving a presentation, to show the audience your step by step process.

We'll start today by using the interactive mode, but instead of the basic
Python interpreter we'll use **IPython**, an enhanced console with some extras
that are very helpful for data analytics applications.

![Fig. 1.2: IPython console](/images/ipython_shell.png)

### Basic interaction with Python

The Python console (or terminal, shell, or command line interface (CLI) if you 
prefer those terms) has a **REPL** or read-evaluate-print loop.  Very simply, 
Python reads whatever you type, executes the instructions (if any), and shows
you the results.  If you type an expression which contains no instructions, it
simply tells you its interpretation of what you typed.  For example:

    In [1]: 2+2
    Out[1]: 4

We could raise 2 to the 10th power:

    In [2]: 2**10
    Out[2]: 1024

We can assign a value to a **variable**.  A variable is simply a name that
points to some data stored in memory.  Remember all those years you spent in
high school looking for "x" and "y"?

    In [3]: x = 3
    In [4]: y = "spam"

You can then use the variable names as expressions to retrieve and print
their values:
    
    In [5]: x
    Out[5]: 3
    
    In [6]: y
    Out[6]: 'spam'
    
Unlike some other programming languages, Python doesn't require you to specify
what type of data is held by a variable (such as integer, decimal, text string,
date/time or other types).  It simply tries to infer what you want to do during
the course of execution, and tries to avoid crashing even if you ask it to do 
something a little odd, like multiplying an integer by a string:

    In [7]: x*y
    Out[7]: 'spamspamspam'
    
Notice that numbers can be typed without decoration, but text must be marked
off with quotation marks, either double-quotes (`""`) or single-quotes (`''`).
That's so text data isn't mistaken for a variable name, function name, or some
other reserved word in the language.
    
### Python lists and dictionaries

Two of the most common data structures you'll see in Python are lists and
dicts (or dictionaries).

A Python **list** is a sequence of items of the same kind of thing.  Use 
`[` square brackets `]` to denote a list. For example:

    In [8]: mylist = [1,2,3,4,5]
    In [9]: yourlist = ["ham","eggs","cheese"]
    
To access a specific item in a list, you need to know its **index** or numeric
position.  

    In [10]: yourlist[0]
    Out[10]: 'ham'

Indexes start with zero, not one, so you might be caught off guard
by something like this:

    In [11]: mylist[3]
    Out[11]: 4

A very important thing you can do with lists is to **loop** through them, that
is, to apply some piece of code to each and every element in the list.  The
simplest way to do this is something like the following.

    In [12]: for i in mylist:
       ....:     print(i)
       ....:
    1
    2
    3
    4
    5
    
If you're having trouble with the above, note that the second line must be
indented; that's how Python knows it's to be repeated at every iteration of
the loop. You must hit enter twice after the second line, so Python knows that 
you're done writing indented code. And `print()` is just the Python function 
(more on functions below) that outputs data to the user's console.
    
A **dictionary** is a data structure to hold items that are (a) not necessarily
the same kind of thing, and (b) indexed by **keys** rather than numeric order.
In essence, every item in a dict has a unique "name" you can use to retrieve
it. A dict is denoted by `{` curly braces `}`. For example:

    In [13]: bob = { "name":"Robert", "age":35, "sign":"Virgo" }

Because Python doesn't care about the sequence of the items in a dict, it will
not necessarily present them in the order you added them.  For example, you
might see:

    In [14]: bob
    Out[14]: {'age': 35, 'name':'Robert', 'sign': 'Virgo'}

To access an element, you use its key:

    In [15]: bob["age"]
    Out[15]: 35
    
You can get very complex data structures by storing lists within lists, dicts
within dicts, dicts within lists, or lists within dicts.  Here's an example of 
the latter:

    In [16]: bob["children"]=["sarah","tom","scooter"]

    In [17]: bob
    Out[17]: {'age': 35,
              'children': ['sarah', 'tom', 'scooter'],
              'name': 'Robert',
              'sign': 'Virgo'}

To access nested items, chain the indexes together.
              
    In [18]: bob["children"][0]
    Out[18]: 'sarah'
    
We can even loop through a nested list.

    In [19]: for c in bob["children"]:
       ....:     print(c)
       ....:
    sarah
    tom
    scooter
    
Some of the data we'll be working with will have deep and complex nesting of 
lists and dicts, and knowing how to navigate them will be key to extracting 
just what we want and preparing it for analysis.
    
### Python functions

A **function** or subroutine is a reusable piece of code that can be called
upon to do some transformation or sequence of steps that the programmer doesn't
want to have to re-write and clutter up his programs.  A function, like a 
variable, has a name.  To call the function, type the name of the function
followed by parentheses, possibly containing one or more **arguments**.

For example, the `print` function takes almost any kind of variable as an
argument, and prints it to the console.

    In [20]: print("hello world")
    hello world
    
Some functions, like `sum`, `min`, and `max` take lists as arguments:

    In [21]: sum(mylist)
    Out[21]: 15
    
    In [22]: max(yourlist)
    Out[22]: 'ham'
    
Only a few functions are "built-in" to Python.  For most other kinds of things
you want to do, such as statistics, data manipulation, or visualization, you
can import **packages** of additional functions.  For example, to take a square
root, import the `math` package:

    In [23]: import math
    In [24]: math.sqrt(x)
    Out[24]: 1.7320508075688772
    
Alternatively, you could import just one function from a package, so you can
call it by its name without the package name as prefix.
    
    In [25]: from math import sqrt
    In [26]: sqrt(x)
    Out[26]: 1.7320508075688772

You can also create your own functions in Python and re-use them.  Use the 
`def` keyword to define a new function, indent the code that will be run when
the function is called, and end it by using the `return` keyword to specify 
the result that's sent back to the program that called it.  In this example,
I define a simple function to return the cube of a number:
    
    In [27]: def cube(y):
       ....:     ycubed = y*y*y
       ....:     return ycubed
    
    In [28]: cube(2)
    Out[28]: 8
    
    In [29]: cube(3)
    Out[29]: 27
    
## Munging the Tides

In the next part of the tutorial, we're going to write Python code to acquire,
prepare, and then do some simple analysis of the data.  This is the kind of 
work you don't want to have to type and re-type every time you need to fix a 
typo, so we're going to switch from the interactive console to an environment
where our code can be edited and saved.  

For my two cents, the best choice is
the Spyder IDE that comes with the Anaconda Python distribution. It gives us
a good text editor, on the left, an interactive IPython console in the bottom
right corner, and other panels and tabs for inspecting objects in memory, the
history of our console sessions, data graphics we've created, and other useful
features.

![Fig. 1.3: Spyder IDE](/images/spyder.png)

We begin this tutorial by importing some libraries.  The `requests` library
contains functions for sending HTTP requests over the web. We'll use it to
request data from NOAA's servers.  The data is formatted in JavaScript Object
Notation, or **JSON** for short, so we'll need a function from the `json`
library to load it into a Python data structure.

    import requests
    import json
    
The way I do this in Spyder is to type those two lines of code into a new code
file, highlight those two lines, and then click the toolbar icon for "Run
current cell".  At right, I see that the two lines are executed in the IPython
console, and on the left, I can click "Save" so that I don't lose my work.

In a Python script file, one of the most useful things you can do is write
**comments**. These are text notes that are ignored by Python so you can 
use them to explain your code to other devlopers or just to serve as 
reminders to yourself.  In Python, everything that follows a `#` is a
comment, so a comment can be placed at the end of a line of code or on 
a line by itself.  Amend the code above to remind yourself what it does.

    import requests    # to get data from the web service
    import json        # to parse JSON into Python data structures
    
### A web service API
    
NOAA's Tides and Currents data is available through a **web service** API; 
that's essentially a server using the same technology that powers a website 
but serving up machine-readable data instead of human-readable web pages.
Each piece of data has a URL and we access it by making HTTP "GET" requests 
over the Internet, just like your browser would.  For more information and 
documentation, visit the [CO-OPS 
website](http://tidesandcurrents.noaa.gov/api/).

The data we want is at a URL that begins with 
"http://tidesandcurrents.noaa.gov/api/datagetter?" and that we complete by 
specifying several parameters separated by `&`. The parameters I want to use
for this tutorial are:

- product=water_level
- datum=MLLW *(the measurement of "mean lower low water")*
- date=recent *(this gives you the last 72 hours of data)*
- units=english *(not metric!)*
- time_zone=gmt
- format=json *(XML and CSV are also available)*
- station=9410170 *(San Diego)* and station=8443970 *(Boston)*

Because I want to get data from two different CO-OPS stations, I'll need two
URLs.  Why not test them out in a web browser and see if I actually
get the JSON data that I want?  Try [this link](http://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&datum=MLLW&date=recent&units=english&time_zone=gmt&format=json&station=9410170) and [this one](http://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&datum=MLLW&date=recent&units=english&time_zone=gmt&format=json&station=8443970).  

To get a better handle on the structure of this data, you might try 
running it through any of a number of free JSON viewers like the one at 
http://jsonviewer.stack.hu.  I use a free Chrome plugin called JSONView
which lets me navigate the data's structure right in the browser.  One
thing you may notice right away is that it uses the same kinds of data
structures you just saw in Python, lists and dicts, and the same symbols
to denote them.  We can load this data into our Python session with just
two steps:

    # Get San Diego data and parse the JSON
    san = requests.get("http://tidesandcurrents.noaa.gov/api/datagetter?"    
                       "product=water_level&datum=MLLW&date=recent"
                       "&units=english&time_zone=gmt&format=json"
                       "&station=9410170")
    sandata = json.loads(san.content.decode())
    
That first instruction could have been one long line, by the way, but I 
broke it up to make it more readable.  Text strings (marked off by 
quotation marks, remember) are automatically concatenated by Python when
the code is interpreted. As far as the `requests.get()` function is
concerned, it received just one argument: the complete URL.

We could do the same sort of thing for the Boston data, but the first
rule of being a good programmer is that a good programmer is lazy.  As soon
as it looks like he's got to do the same thing twice, a programmer thinks
about automating it.  Here's a way we could get the data from two CO-OPS
stations without typing that whole URL twice:

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
  
Better run this code in the console to make sure you don't get any error
messages.  It may take a few iterations to find all the typos, but that's
fine---that's why the console is there!

### Exploring the data

Before we try to make something with this data, it's a good idea to poke
around and see what it contains.  If you used a JSON viewer of some kind
you probably saw that at the top level, it's a dict with two elements:
"data" and "metadata".  Spyder also has a Variable explorer (in the upper
right panel by default) which you can use to explore the San Diego and 
Boston datasets.  The "metadata" item indeed contains **metadata**, that
is, a bit of information to tell us more about the data it accompanies.

    In [10]: sandata["metadata"]
    Out[10]: {'id': '9410170', 
              'lat': '32.7142', 
              'lon': '-117.1736', 
              'name': 'San Diego'}

The "data" item is a list of dicts, one for each sea level measurement over
the past 72 hours.  If you inspect the first item in the list, you'll see
that it contains a few elements of its own: "v" (value?) seems to be the 
measurement we want, "t" is the time of the measurement, and we'd have to
look at the API documentation to figure out what the other codes mean.

    In [11]: bosdata["data"][0]
    Out[11]: {'f': '1,0,0,0',
              'q': 'p',
              's': '0.138',
              't': '2016-01-11 04:30',
              'v': '10.845'}

I've decided that what I want to do is plot the sea level data as a line
graph with two lines: one for Boston and one for San Diego.  I'm not an
astronomer, but I expect that something about the moon's position will
mean that the east and west coast tides will be different in a predictable
way.  For each station, what I'll need is a simple python list of sea level
measurements, that is, just the "v" values.

The easy way to munge this data is to loop through the 700+ data points
in each data set.  The loop for San Diego should start with a line like
`for i in sandata["data"]:` but what goes inside the loop?  Well, what
we're going to want to do is start with a new, empty list and append each
data point to the end of it.

    sanmllw = []  # an empty list
    for i in sandata["data"]:
        sanmllw.append(i["v"])
        
But wait! Another personality trait of good programmers (in addition to
laziness) is constant anxiety.  The code looks right, is right, but I have
a nagging feeling that it might be wrong.  Is `i["v"]` the correct way to
reference the number I want?  A simple trick to give myself
some confidence in it is to `print()` a little message to the console 
showing me the data from each step.  Here's the loop with a `print()` 
statement for "debugging"; it's a bit more wordy but makes me feel a lot
better.  The print statement can be commented out later, once I know I've
got the loop working right.

    sanmllw = []  # an empty list
    for i in sandata["data"]:
        sanmllw.append(i["v"])
        print("I just appended " + i["v"])  # for debugging

Do the same for the Boston data; store it in a list called `bosmllw`.

### Visualizing the data

This is time series data, and is naturally very well suited to a line graph.
The most popular data visualization package for Python is `matplotlib`, and
yes, it's included in the Anaconda distribution.  In this case we're going 
to import just a part of it called `pyplot` and we're even going to give it
a shorter nickname so we can save some keystrokes when using it.  The import
statement looks like this:

    import matplotlib.pyplot as plt
    
You've come a long way in these few pages, from entering "2+2" at the console
to see what would happen, to accessing data over the Internet, exploring it,
and transforming it into time series.  I think, then, we'll take it easy with
this last task.  Here's a one-liner that produces a line graph with our two
series: San Diego in red and Boston in blue.

    plt.plot(sanmllw,"r",bosmllw,"b")
    
To spruce it up, I'll add a title and a y-axis label.  Be aware that all
three of these lines must be run together, as a block, in order to produce
the graph.

    plt.plot(sanmllw,"r",bosmllw,"b")
    plt.title("San Diego and Boston tides")
    plt.ylabel("MLLW")

The output looks like Figure 1.4 for me.  (It'll look different for you, 
because you've got a different 72 hours of sea level data.)

![Fig. 1.4: San Diego and Boston Tides](/images/tut01_graph1.png)

## Extending this exercise

These are some extensions you can do to develop your skills:

1. Add two more stations to our line chart: Charleston, SC and San 
    Francisco. Plot their data in green and purple (hint: "magenta"), 
    respectively.
    
2. I'd like to see a longer time span of data.  Rewrite the script so that
    it acquires and plots all data from December 11, 2015 through January 
    10, 2016.

3. I might like to see if the phase of the moon has anything to do with 
    the tides.  (It probably doesn't, but like I said, I'm not an 
    astronomer.)  It happens that 12/11/2015 and 1/10/2015 each had a
    new moon, with the full moon occurring on Christmas Day, 
    12/25/2015. To help me investigate, please add to this data 
    visualization a second subplot that indicates the phase of the 
    moon.  Essentially this should be a line graph that increases linearly
    from 0 to 100% on 12/15 and then decreases back to 0.  It should be 
    below, and therefore
    parallel in time to, the plot of the tide data.

You may find the documentation at matplotlib.org helpful, such as the
[Pyplot tutorial](http://matplotlib.org/1.3.1/users/pyplot_tutorial.html)
found there.  You can also generally find help from places like Stack
Overflow but *not* if you enter homework problems directly. They flame you
for that.
    
### Grading

If you do this as homework in my class, submit a Python script that
produces a graph like Figure 1.5, below.  (You are free to embellish it or
play around with the style, as long as it has two subplots with the 
right data and line colors. I will run your code on my own system
and, if it gives me the desired outcome, give you full credit.  Make sure
your name and student number are provided in a comment near the top of the
code file.

![Fig. 1.5: The Desired Outcome](/images/tut01_solution1.png)
