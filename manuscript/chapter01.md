# Chapter 1 

{language=python,linenos=off}

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

![Fig. 1: Data.gov](/images/datadotgov.png)

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

![Fig. 2: IPython console](/images/ipython_shell.png)

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

We begin this tutorial by importing some libraries.

    In [30]: import requests
    In [31]: import json
    
    