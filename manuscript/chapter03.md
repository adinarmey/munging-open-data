# Tutorial 3 

## Munging your data into a database

In tutorial 2, we loaded quite a lot of data from CSV files into active
memory (or RAM).  If your personal computer is an older one, that analysis
might have strained its limits.  As we go on to work with larger and larger 
data sets, we will need to be
able to work with the data where it is stored---on disk (in persistent
memory) rather than in the computer's active memory.  A database is a
powerful data management tool for storing, retrieving, and analyzing
data that's too large for active memory.

In this tutorial, we're going to work with data from Google Maps, one of
the most feature-rich data web services out there, but instead of loading
data from Google right into Python data structures, we're going to store
it in a popular new database: MongoDB.  MongoDB is a document store, a
modern non-relational database that stores data in binary JSON.  That
means you don't need much training in data modeling: just structure the
data in the way you want to use it, and MongoDB can store it that way.

## Provisioning a database in the cloud

MongoDB is meant to run as a server, and therefore is not as easy to set
up as a consumer-oriented personal database like, e.g., Microsoft 
Access.  From experience, MongoDB is a pain in the neck to try to install,
especially on Windows, and after a couple of hours messing around with its
configuration, you'll probably be scratching your head wondering why you
decided you wanted to be a database administrator.  Let's consider that
question: *do* you want to be a DBA?

I sure don't.

In fact, we want to *use* a database, not to install and configure 
one, and it is our good fortune to live in the era of "the cloud".  The
cloud is actually a marketplace for computing infrastructure, software
platforms, and other services in which you can "pay by the drink". Where
ten years ago you might have had to buy your own server and set up the
software yourself, today Amazon or Microsoft or Google or Rackspace has
abundant excess capacity in its well-managed computer centers, so you
can simply "provision" a server or a cluster of servers and start
building your application on it.  They pay for the air conditioning, deal
with repairs and upgrades, and you just focus on your code.

At the time of writing, the best way to provision a MongoDB database seems
to be to use the platform-as-a-service (PaaS) company 
[MongoLab](https://mongolab.com)[^iaas].  They offer several levels of
service including a free "sandbox" database which should be sufficient for
this tutorial.[^prov]  You can create an account and deploy a sandbox database
without being asked for a credit card.

[^iaas]: MongoLab in turn runs its MongoDB server instances on computing
    infrastructure provided by one of the big infrastructure-as-a-service 
    (IaaS) companies such as Amazon Web Services.  There is a somewhat
    blurry line between the concepts of PaaS and IaaS.

[^prov]: See MongoLab's website for up-to-date instructions.  The free
    offering is a "single-node" deployment in the "standard line" of service
    with a limit of 500MB at the time of this writing.
    
Once you've provisioned a database from MongoLab, you can check the website
for the details on how to connect to the database.  There are two types
of connection strings: one you can use from MongoDB's command line client,
**mongo**, and one that you can copy and paste into your own code project,
as we will do in this tutorial.  Before we begin, you'll also need to create
a *database* user: a username and password that will have access to this 
sandbox data but *not* to your MongoLab account.  (These should be 
"disposable" credentials because other people working on your code are
going to be able to see them.  Don't give the database user the same 
credentials you use for your e-mail or online banking, please!)

![Fig. 3.1: MongoLab connection code](/images/mongolabconnection.png)

## Querying MongoDB with Python

In Python, you can use the **`pymongo`** package to connect to a MongoDB
server.  This package doesn't come installed with the Anaconda Python
distribution, so you may need to install it manually.  Anaconda comes with
its own updater, `conda`, which can be used at your system's command
prompt[^prompt] by typing:

    conda install pymongo

If you aren't using Anaconda, you can probably use the updater that comes
native with Python, `pip`, which works in the same way:

    pip install pymongo
    
If you have trouble using these command-line updaters, you may need to correct
your `PATH` so that it includes the directory where `conda` or `pip` is 
found.  See the preface entitled "Setting Things Up" for more on the `PATH`.

[^prompt]: On Windows, try opening the "Anaconda Prompt" from your Start
    menu.  On Mac or Linux, your regular Terminal will be fine.
    
Once `pymongo` is installed on your computer, the following four lines of
code will set up the database connection.  In the second line,
of course, paste the connection URI from MongoLab's site, and substitute
in your database user's username and password.

    from pymongo import MongoClient
    MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER/DATABASE"
    client = MongoClient(MONGO_URL)
    db = client.get_default_database()

MongoDB's data model is very simple.  You can define any number of 
"collections" (analogous to "tables" in other databases), and a collection
can hold any number of documents, records, or "rows" of data. A document
is basically a JSON object or a Python dict, and may contain nested
objects/dicts or lists.  No action is needed to create a new collection,
just initiate it by inserting some data:

    In [1]: db.mycollection.insert_one({"answer":42})
    Out[1]: <pymongo.results.InsertOneResult at 0x9bfafc0>
    
To confirm that this creates a new collection called `mycollection`, try
the `collection_names()` method of `db`.  You may want to ignore the
ignore those collections automatically created and managed by the database:

    In [2]: db.collection_names(include_system_collections=False)
    Out[2]: ['mycollection']

Retrieving data can be quite simple, too.  The `find_one()` method retrieves
one result for our query, or we may use the `find()` method to retrieve a list
of all matching data.

    In [3]: db.mycollection.find_one()
    Out[3]: {'_id': ObjectId('56b50ab830e1ef0adcedb79f'), 'answer': 42}

What's that messy-looking `ObjectID` in the result?  Well, a document-oriented
database, as it is a kind of key-value store, needs a unique "key" by which it
can address each document.  Since we inserted a document without assigning
the `_id` value, it created this unique-by-design object to serve as the 
key.  When building a real database, you need to decide whether to use a
key of your own, a unique "natural key" like a social security or phone
number, or a key automatically generated by the database.

When we inserted our first document, you may have noticed that the command
produced a result, a `pymongo.results.InsertOneResult` object.  If we had
wanted, we could have assigned this to a variable, and inspected its
`inserted_id` to fetch the newly-generated key.

    In [4]: x = db.mycollection.insert_one({"question":"to be or not to be"})

    In [5]: x.inserted_id
    Out[5]: ObjectId('56b5119730e1ef0adcedb7a4')

This becomes useful if we want to use the key to retrieve the data later. The
way you specify query criteria in MongoDB is to pass a dict of keys and
values as the first argument to the `find()` or `find_one()` methods.  The
simplest usage merely specifies a value that you want the results to match:

    In [6]: db.mycollection.find_one({"_id":x.inserted_id})
    Out[6]: {'_id': ObjectId('56b5119730e1ef0adcedb7a4'), 
             'question': 'to be or not to be'}
             
The second argument to the query method is a "projection parameter" dict 
that tells the database 
which *parts* of
the result to return.  For example, if you don't want to see the `_id`,
assign the value `False` (or zero) to that key.

    In [7]: db.mycollection.find_one({"_id":x.inserted_id},{"_id":False})
    Out[7]: {'question': 'to be or not to be'}

### More advanced queries

To demonstrate a few more of MongoDB's query capabilities, you can use this
somewhat silly list of superhero data, or create your own.  

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

Because I have
created it as a list of dicts, it can be inserted directly into a new
database collection with the `insert_many()` method:

    In [8]: db.heroes.insert_many(heroes)
    Out[8]: <pymongo.results.InsertManyResult at 0x9c2a1f8>

We can retrieve a result, as before, with an exact match.  In this example,
again, we exclude the `_id`.

    In [9]: db.heroes.find_one({"name":"Aquaman"},{"_id":0})
    Out[9]: 
    {'name': 'Aquaman',
     'portrayals': [{'actor': 'Jason Momoa', 'year': 2016}],
     'secret identity': 'Arthur Curry'}

But instead of an exact match, we could use a comparison.  MongoDB supports
the `$gt` and `$lt` operators for "greater than" and "less than", and several
others.  To query for all heroes except those whose names start with A,
specify that you want `name` "greater than or equal to" the letter B.

    In [10]: db.heroes.find({"name":{"$gte":"B"}},{"_id":0})
    Out[10]: <pymongo.cursor.Cursor at 0x9c389e8>
    
The `find()` method returns a database cursor.  This is a data structure like
a list that you can iterate through, but only once.  If you'd like to keep it
in memory, you can convert it to a Python list with the built-in `list()`
function.  In the last step, I didn't assign the query result to a variable,
so I ought to do the query again.  However, a nice feature of the IPython
console (not present in plain Python), is that you can refer back to the
output of previous commands simply using an underscore and the output 
index.  In this case, we want the data we saw labeled `Out[10]` so we can
just type

    In [11]: list(_10)

Here are some other queries to try.

Let's say you want to query for matching values in an embedded structure,
such as the name of an actor who portrayed a hero.

    db.heroes.find({"portrayals.actor":"Christopher Reeve"},{"_id":0})

You can also make more than one comparison at the same time, for example,
you might want to find which heroes had been seen in film in a particular
decade.

    db.heroes.find({"portrayals.year":{"$gte":2000,"$lt":2010}},{"_id":0})
    
You may notice that this query returns data on both heroes (Superman and 
Batman) including *all* the film portrayals for each---even those not in
the specified decade---but it excludes characters with no portrayals in
that decade.  MongoDB is meant to store and retrieve documents as wholes
and not filter their sub-structures, so this is normal behavior.  It is
possible to use the projection parameter, though, to do this filtering
by using the projection parameter in this way:

    db.heroes.find({"portrayals.year":{"$gte":2000,"$lt":2010}},
                   {"_id":0,"name":1,"portrayals.$":1})

You can also apply a projection to the entire collection, without any 
query criteria, by simply passing an empty dict `{}` as the first argument
to the `find()` method:

    db.heroes.find({},{"_id":0,"name":1,"secret identity":1})

Once you have finished experimenting with database queries, you might want to
delete ("drop") the two collections we created---especially if, like me, you're 
using a
free but very limited sandbox deployment.

    db.heroes.drop()
    db.mycollection.drop()

You can confirm that these collections are gone by running `collection_names()`
again.
    
## Getting to know the Google Maps APIs

In Tutorial 1, we used a free web service API from NOAA in part because it was
easy; we didn't need any kind of account to access it.  Most APIs that you will
want to use, even if free, require a little bit of setup.  To get started,
browse to [Google Developers](https://developers.google.com/) and explore the
product directory.  In this tutorial, we'll use the [Google Maps Distance
Matrix API](https://developers.google.com/maps/documentation/distance-matrix/), 
which calculates distance and driving time between given 
addresses.  Explore the information and samples on the web to learn about
how to use this API and what the data looks like.  To enable the API, 
you'll need to do three steps, assuming you already have a Google or Gmail 
account of some kind:

1. Create a project.  It doesn't matter what' it's called.  You might create 
   one generic project for all your
   work in these tutorials.
2. Activate the Google Maps Distance Matrix APIs.  Google has lots of APIs
   and you have to manually specify which one(s) your project should have 
   access to.
3. Create an "API key".  This is a unique code that identifies you to the
   API, so Google can enforce data rate limits.  (At time of writing, they
   allow 2500 API requests per day for free; for more, you'd have to pay.)
   
Once that's done, you should be able to access the API via a simple Python
program similar to what we used in Tutorial 1.  In this case, the main
request parameters that go into the URL are "origins", "destinations", and 
"key".

    import requests
    import json
    mykey="YOUR GOOGLE MAPS API KEY"
    fro="Tempe, AZ"
    to="Disneyland"
    re = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json?"
        "origins="+fro+"&destinations="+to+"&key="+mykey)
    r = json.loads(re.content.decode())
    # pretty-print the output
    print(json.dumps(r,indent=2))

Just like on the Google Maps website, Google can generally work with partial
addresses like a city name or zip code, or even something like "Disneyland",
which I see is only five and a half hours away from where I'm sitting.

## Loading our database with Distance Matrix data

Along with this tutorial, I've provided a CSV file of zip codes in Arizona, 
also available [on the GitHub site for this book](https://github.com/joeclark-phd/munging-open-data/blob/master/tutorials/AZ_zipcodes.csv. 

What I want to do is find the driving time to my office
from each zipcode, and analyze them to see which towns and cities 
would offer the 
most time-efficient commutes (that is, the greatest distance covered in the
least time).  There are 567 zip codes, which means I'll call the Google Maps
API 567 times, and I definitely don't want to re-do that work every time I
iterate on this code.  Therefore, the plan is to load each result into
a database, and analyze it by querying the database.

Because we can only hit the API up to 2500 times per day, we've got to get
this right in the first few tries.  Using the results of the test request,
above, you can see that the response structure has some pretty complex
nesting, and we don't need all of it.  For our purposes, we can create
a new document by picking and choosing some values out of the response 
data, which I called "`r`":

    d = {"origin":r["origin_addresses"][0],
         "duration":r["rows"][0]["elements"][0]["duration"]["value"],
         "distance":r["rows"][0]["elements"][0]["distance"]["value"] }

Now, we load the zip codes from the CSV file, using `pandas` as in Tutorial 2.

    import pandas as pd
    zips = pd.read_csv("AZ_zipcodes.csv",names=["zip"],dtype="str")

Now, we'll loop through the zip codes and for each one, request data from the
Google API, reformat it into the simpler structure as above, and then insert
it into a new collection called "routes" in the database.  I'll take this step
by step because there are some changes.

First, load the required libraries and make the database connection:

    from pymongo import MongoClient
    import requests
    import json

    MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER.mongolab.com:PORT/DATABASE"
    client = MongoClient(MONGO_URL)
    db = client.get_default_database()

Initialize the fixed parts of the URLs we'll be generating.  Only the zip code
will change with each API request.

    to="300 E Lemon St, Tempe AZ" # the author's office building
    mykey="YOUR GOOGLE MAPS API KEY"

I like to put
a line in my code that empties the database, so that if I subsequently
fix a mistake and re-run the code, I don't end up with double the
data.

    db.routes.drop()

The loop begins as you might expect:

    for z in zips.zip:
        # get the data from Google
        re = requests.get(
        "https://maps.googleapis.com/maps/api/distancematrix/json?"
        "origins="+z+"&destinations="+to+"&key="+mykey)
        r = json.loads(re.content.decode())

Now I like to add a little error check before loading the database.  If the
result doesn't contain a "distance" element, then Google may have made a 
mistake or perhaps I might have sent it an invalid zip code.  Either way,
I want to skip it.  This `if` statement seems to be a filter for empty
responses:

        if "distance" in r["rows"][0]["elements"][0].keys():

From each valid response I construct a nice little data item as above, but
with one addition: I store the zip code itself.

            d = {"zip":z,
                 "origin":r["origin_addresses"][0],
                 "duration":r["rows"][0]["elements"][0]["duration"]["value"],
                 "distance":r["rows"][0]["elements"][0]["distance"]["value"] }
            db.routes.insert_one(d)

Finally, I want each iteration of this process to print a message to the
screen so that I can see the progress.  Without this, the program may run
fine but all I may see is a frozen screen for several minutes.

        print("processed zip code "+z+"...")

The complete code for this process is as follows:


{title="Complete code to load data from Google into MongoDB"}
~~~~~~~~
import pandas as pd
zips = pd.read_csv("AZ_zipcodes.csv",names=["zip"],dtype="str")

from pymongo import MongoClient
import requests
import json

MONGO_URL = "mongodb://joe:root@ds051933.mongolab.com:51933/cis355sandbox"
client = MongoClient(MONGO_URL)
db = client.get_default_database()

to="300 E Lemon St, Tempe AZ" # the author's office building
mykey="AIzaSyCEqH1F0f7kHhVvn8YqBgMVMFi6x4Fb_4g"

db.routes.drop()

for z in zips.zip:
    re = requests.get(
    "https://maps.googleapis.com/maps/api/distancematrix/json?"
    "origins="+z+"&destinations="+to+"&key="+mykey)
    r = json.loads(re.content.decode())
    if "distance" in r["rows"][0]["elements"][0].keys():
        d = {"zip":z,
             "origin":r["origin_addresses"][0],
             "duration":r["rows"][0]["elements"][0]["duration"]["value"],
             "distance":r["rows"][0]["elements"][0]["distance"]["value"] }
        db.routes.insert_one(d)
    print("processed zip code "+z+"...")
~~~~~~~~

## Querying our data

First, let's make some checks to see if our data was loaded properly.  The
`count()` method will tell me how many *valid* records I found, and I can 
query one as a sample to see whether it has the intended structure.

    In [12]: db.routes.count()
    Out[12]: 524

    In [13]: db.routes.find_one()
    Out[13]: 
    {'_id': ObjectId('56b5350030e1ef0adcedb7a9'),
     'distance': 19381,
     'duration': 1217,
     'origin': 'Phoenix, AZ 85001, USA',
     'zip': '85001'}

To retrieve all the data, we need a pretty simple `find()` query.  Use `list()`
to convert it to a normal Python list, just in case we want to loop through
it more than once.

    thecursor = db.routes.find({},{"_id":0})  # thecursor is a database "cursor"
    thedata = list(thecursor)  # thedata is a normal Python list

The data is conceptually very much like a spreadsheet or relational database
table: it consists of a list of "rows", each with the same four elements. With
the `pandas` package, we can very easily convert this to a DataFrame and take
advantage of a DataFrame's affordances for plotting, finding the maxima, and
more.

    import pandas as pd
    thedf = pd.DataFrame(thedata)  # thedf is a DataFrame

The goal is an XY scatter plot of distance and duration.  This is a good
type of data visualization to show the relationship between two variables.

    thedf.plot(kind="scatter",x="duration",y="distance")

![Fig. 3.2: Output of first plot command](/images/tut03_m_s.png)

Already you can see, as you'd expect, that mileage is tightly correlated with 
driving time.  We can improve this visualization in several ways, 
however. First, let's convert those distances from meters to miles, and
the driving time from seconds to minutes.

    thedf.distance = thedf.distance/1609.34  # meters to miles
    thedf.duration = thedf.duration/60  # seconds to minutes

We can also increase the size of the plot, and set the limits of the X and Y
axes so that we aren't displaying the space below zero on either axis.  In 
addition, by importing the `pypplot` package that we used in Tutorial 1,
we can tweak various aspects of the plot like the title and labels.

    import matplotlib.pyplot as plt
    thedf.plot(kind="scatter",x="duration",y="distance",
               xlim=[0,600],ylim=[0,600],figsize=[7,4])
    plt.title("Time and distance of Arizona commutes to Tempe", fontsize=14)
    plt.xlabel("driving time (minutes)", fontsize=14)
    plt.ylabel("distance (miles)", fontsize=14)

Also, I'd like to highlight the most efficient commute, that is, the one that
allows me to drive the fastest!  We're going to plot a single point on top
of the existing graph at (x,y) where x is the duration and y is the distance
of the fastest commute.  We first calculate the ratio of distance to time
for the whole DataFrame, then use the `idxmax()` method to find the index
of the row that has the maximum value:

    thedf["speed"] = thedf.distance/thedf.duration
    i = thedf.speed.idxmax()
    x = thedf.duration[i]
    y = thedf.distance[i]

The `plt.plot()` function takes as its first two arguments a list of x values
and list of y values.  To draw a single dot, we can give it single values.  The
parameter "ro" specifies a red circle, and "ms" (marker size) makes it larger
than the other dots:

    plt.plot(x,y,"ro",ms=12)

The dot is nice, but I'd also like to annotate the plot with a note.  First,
draw a red line from the center of the dot to a point over to the right.  This
is essentially a data series of two points:

    plt.plot([x,325],[y,y],"r")

The following command adds a note at the right end of the red line we just
drew, including the address with the fastest commute and the speed in miles
per hour.

    plt.text(325,y,
             "Fastest commute:\n"+thedf.origin[i]+"\n"+
              str(thedf.speed[i]*60)+"mph",
             fontsize=14,verticalalignment="center")

The complete visualization code and the finished plot are as follows:

{title="Complete visualization code"}
~~~~~~~~
# find the best commute (fastest miles/minute)
thedf["speed"] = thedf.distance/thedf.duration
i = thedf.speed.idxmax()
x = thedf.duration[i]
y = thedf.distance[i]

# plotting
import matplotlib.pyplot as plt
thedf.plot(kind="scatter",x="duration",y="distance",
           xlim=[0,600],ylim=[0,600],figsize=[9,6])
plt.title("Time and distance of Arizona commutes to Tempe", fontsize=14)
plt.xlabel("driving time (minutes)", fontsize=14)
plt.ylabel("distance (miles)", fontsize=14)
plt.plot(x,y,"ro",ms=12)
plt.plot([x,325],[y,y],"r")
plt.text(325,y,
         "Fastest commute:\n"+thedf.origin[i]+"\n"+
          str(thedf.speed[i]*60)+"mph",
         fontsize=14,verticalalignment="center")
~~~~~~~~
             
![Fig. 3.3: Completed XY plot](/images/tut03_mi_min.png)
    
    
## Extending this exercise 

These are some extensions you can do to develop your skills:

1. Google also offers a "Google Places API" which lets you look up businesses
   and other public places around a map location.  Explore this API and find
   out how to request a list of all bookstores within 50km of my office.  My
   office is at latitude 33.417, longitude -111.934.

2. The Google Places API also offers a "details" mode that gives you more 
   information about one business at a time.  Use this API to load all the
   *reviews* that Google provides for each bookstore.  Calculate the average
   review score.
   
3. Now use the Google Maps Distance Matrix API to get the driving distance
   from each bookstore to my office.  Now store all this data in a MongoDB
   database; for each record, store the name, address, average rating, and
   driving distance.
   
4. Retrieve the data from the database and create an XY plot of distance (x)
   and average rating (y) for all the bookstores you found.  Place an
   annotation on the highest-rated one, with its name and the distance.
   
### Grading

For homework in my class, submit a Python script that queries your database
and generates the data visualization described in #4.  The style, colors,
annotations, etc. do not need to be exactly the same.  Also, do not include
the code that queries the Google APIs and loads the database.  (This should
already be done and not need repeating.  You may keep the code but comment
it out, if you'd like me to be able to see your work.)

An example of the output will be provided soon.

Note that Google estimates driving time based on current conditions and the
time of day, so your data may not be exactly the same as mine.


   
## Essential References

- PyMongo tutorial in the MongoDB documentation: 
  [Link](http://api.mongodb.org/python/current/tutorial.html)
- MongoDB documentation on the `find()` method 
  [Link](https://docs.mongodb.org/manual/reference/method/db.collection.find/)
  gives lots of examples of MongoDB queries and projection parameters. Be 
  aware that MongoDB has a JavaScript shell so some details will be 
  different when using `pymongo` as the middleman. For example, Python
  is stricter about requiring quotation marks around keys.