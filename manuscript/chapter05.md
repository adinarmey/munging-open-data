# Tutorial 5 

In this tutorial we will create a data-driven web service using the Python
framework [Flask](http://flask.pocoo.org).  You'll effectively be setting
up a web server, just like the ones that run human-readable websites, 
except that this one will serve up JSON data drawn from a MongoDB database. As
your web service can receive input and provide output to anyone in the world, 
this can be considered
a complete "data product" if only a simple one.

Three categories of tolls make it possible to get a useful data "app" up and
running in no time flat:

- **Minimalistic web frameworks** enable the rapid creation of
  fully-functional web services.  These frameworks do all the under-the-hood
  networking stuff for you, so the developer only has to write the code
  that retrieves or processes data at each URL endpoint.
  
- **NoSQL databases** allow us to store and retrieve data almost exactly
  as it is communicated to and from the web service.  There is no need for
  sophisticated database queries or complex processing.
  
-  **Cloud app development platforms** allow us to deploy the database server and 
   web application servers with a few clicks, so that we don't need to learn
   how to install and configure the servers ourselves.   
   
Specifically, in this tutorial we'll use:

- The Flask web framework for Python, which can implement a functioning
  web service in about a dozen lines of code.  Similar frameworks exist
  for other programming languages.
- MongoLab.com, which provides our MongoDB database as a service, as 
  in Tutorial 3. 
- The [Heroku](http://www.heroku.com) applicaiton platform to host our code.


## A "flinkedin" web service

Our example of a data product will be an app that keeps track of profiles
of employed people and their job histories, much like a certain professional
social networking site.  Its API will allow users to view users' profiles, to
add new profiles, and to add to a user's job history.  As a homework
assignment, you'll create URL endpoints to view all companies and to see 
which users have worked for a
given company.  Figure 5.1 lists the proposed API endpoints.

![Fig. 5.1: Planned API endpoints](/images/tut05_endpoints.png)


## Flask as a web service framework

Before writing code that connects to a database, we can set up the
basic web app and simply serve fake data.  A simple Flask web service
with one URL endpoint requires only the following code.  Save this in
a file and call it `app.py`:


{title="Minimal Flask web app"}
~~~~~~~~~~
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return( "Hello world!" )

if __name__ == "__main__":
    app.run()
~~~~~~~~~~

In this code listing, the first two lines and the last two lines are
"boilerplate"---they'll be part of any Flask application.  The real
substance is in the middle, where you define what happens at any given
URL endpoint.[^endpoint]  Each function of the API consists of two parts:
a one-line "decorator" starting with `@app.route` that specifies a 
URL endpoint, and a Python function (beginning with `def`) that holds
the code that should run when that URL is accessed.

[^endpoint]: The "endpoint" is all of the URL that comes after the
    server name.  For a page located at www.mysite.com/api/, the endpoint
    is "/api/".  We generally don't include the server name itself in
    this code.

In the example, I set up one endpoint, the "/" or root URL of the
application.  Initially, the server we'll test this on is your own personal
computer, "localhost", at port 5000.  The URL therefore will be 
"http://localhost:5000/" with nothing after the slash.

You can run this code from within the Spyder IDE by clicking the "Run file"
button in the menu bar, and it will run, but won't give you much feedback. I
prefer to run this file from the system's command line.  To do so, navigate
to the folder where the file was saved, and type

    python app.py
    
If your system is configured to know where Python is, it will read the 
specified file and run it.  This is sometimes better than using an IDE
like Spyder, especially when running a program that starts a server. The
Flask application is running a web server which will keep running (and
thereby lock the console) until you force it to stop by pressing CTRL+C. Once 
you've started the app, you can test it by opening any web browser
and navigating to http://localhost:5000/.

![Fig. 5.2: Starting a Flask app from the command line](/images/tut05_cmd.png)

As you are browsing, you may notice that the terminal gives some informative
output about the HTTP requests it is responding to. The
same test server will launch if you run the file in Spyder, but Spyder 
doesn't allow it to give you any informative output, so I don't see Spyder as
the ideal way to run such a program.

Try adding more URL endpoints and test them by stopping and re-starting the
server.  For example:

    @app.route("/api")
    def api_instructions():
        return( "API instructions will be provided here" )

For each endpoint, the function name (after `def`) must be unique, so be 
careful not to forget that when copy-pasting to create new endpoints. In an
API, typically you want to be able to use parts of the URL as inputs to
be processed.  For example, a username could be part of the URL which
tells you which profile to display.  Flask makes this pretty easy. Specify
in the `@app.route` decorator which part of the URL is variable by wrapping
it in angle brackets `<>`, and then provide that variable to the function
below as an argument, so it can be used in the code.  For example:

    @app.route("/home/<username>")
    def home(username):
        return( "Hello " + username + "!" )

Try re-starting the server and visit a URL like http://localhost:5000/home/Joe.

![Fig. 5.3: Hello Joe!](/images/tut05_hello.png)

We may not win any web design awards for this, but it works.

## Faking it until we make it

Before connecting to a database or putting our code into the cloud, we ought
to prototype what we want the end result to look like.  I'm a big fan of
prototyping new systems rather than simply describing them on paper.  Our
API is going to serve JSON data, and that's easy enough for us to 
produce in Python.  Incidentally, even our POST methods will return JSON to
the users, if only a small message to tell them their data was posted
successfully.

The Flask package includes a function called `jsonify` for sending data
to the user as JSON.  Change the import line in your code to

    from flask import Flask, jsonify

And now create some URL endpoints that return fake, er, prototyped data. As
you see in the example, you can use the `@app.route` decorator to specify
different routes for the same URL when accessed by different methods. (GET
is the default method that you don't need to specify.)


{title="Mocked-up API endpoints"}
~~~~~~~~~~~
@app.route("/api/profiles")
def fetch_profiles():
    # retrieve all users' names and unique ids
    fake_data = {"profiles": [ 
                    {"name":"John McLane", "id":"jmclane"},
                    {"name":"James Edwards", "id":"j"},
                    {"name":"Samwise Gamgee", "id":"samg"}
                             ] }
    return( jsonify(fake_data) )

@app.route("/api/profiles", methods=["POST"])
def new_profile():
    # send a message indicating successful post
    fake_data = {"status":"OK","id":"newuser77"}
    return( jsonify(fake_data) )

@app.route("/api/profile/<id>")
def fetch_one_profile(id):
    # send all details of one user's profile and job history
    fake_data = {"name": "John McLane",
                 "id": "jmclane",
                 "jobs": [ {"employer":"NYPD",
                            "position":"Lieutenant",
                            "start":"1988"} ]
                }
    return( jsonify(fake_data) )

@app.route("/api/profile/<id>/jobs", methods=["POST"])
def new_job(id):
    # send a message indicating successful post
    fake_data = {"status":"OK","id":"olduser123"}
    return( jsonify(fake_data) )

@app.route("/api/companies")
def fetch_companies():
    # retrieve all unique company names in the database
    fake_data = {"companies": [ "NYPD", "MIB", "Bag End" ] }
    return( jsonify(fake_data) )

@app.route("/api/company/<name>")
def fetch_one_company(name):
    # retrieve list of all profiles who work(ed) for a company
    fake_data = {"name": "NYPD",
                 "profiles": [ {"name":"John McLane", "id":"jmclane"},
                               {"name":"James Edwards", "id":"j"} ]
                }
    return( jsonify(fake_data) )
~~~~~~~~~~~


## Testing the API's POST methods

It's easy to test the GET methods we've coded.  Run the code file again and 
use your browser to navigate to the URLs; your browser sends GET requests
and you should be able to see the response as JSON.  Some browsers have
add-ons that allow you to see the JSON in a clearer way: for example, I use
the JSONView extension to Chrome.

Testing the POST methods is a little more difficult.  Three ways we could
do it are:

1. Write custom Python code (using the `requests` package) to access our API.
2. Use the command-line `curl` utility.
3. Use a specialized program for testing HTTP requests.

The Python approach would be recommended if we were writing automated tests,
that is, code which would be used to test a live system in production.  You 
can bet that professional web companies like Facebook and Amazon have plenty
of automated tests, but it's overkill for our purposes.

`curl` is a command-line utility that should be available on Windows as well
as on Mac and Unix systems.  With the Flask app running, try this in your
terminal:

    curl -i http://locahost:5000

With the "`-i`" option, `curl` provides the full HTTP response, including
the response code and headers, as well as the body of the message ("Hello
world!").  This is the response to a GET request by default.  To send a POST
request, add `-X POST` to the command.  

    curl -i http://localhost:5000/api/profiles -X POST

That's enough to test our POST endpoints and see if they provide the correct
responses, however, it can be a very clunky way to test the actual posting of
data.  To specify HTTP headers, you'd use the `-H` option and provide them as
text, and to specify the message body, you'd use the `-d` option and the full
text of the data you want to upload.  This could span multiple lines and 
heaven help you if you forget a quotation mark.

I would strongly recommend getting a good API testing tool.  The one I like
is a Chrome extension called Postman, and there's a free version of it.  The
basic function is pretty intuitive: type a URL, pick a method (GET, POST, PUT,
DELETE, or any other), and click "Send".  You can also specify headers and
a message body, and inspect the response in a few different ways
    
![Fig. 5.4: Testing an API with Postman](/images/tut05_postman.png)
   
Confirm now that all of the following API endpoints work, referring back to
Figure 5.1.

## Making it real: a database-driven API

The next step is to replace the fake data with a real database.  For this
exercise we'll use a MongoDB back end, for which you should already have
credentials.  Insert the MongoDB connection code into your Flask app 
somewhere near the top of the file before the first `@app.route` decorator.

    # database connection
    from pymongo import MongoClient
    MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER.mongolab.com:PORT/DATABASE"
    client = MongoClient(MONGO_URL)
    db = client.get_default_database()

### Implementing the POST methods
    
We could do the POST methods first, because we'll need them to load some
data before testing the GET methods.  For this, we'll need a couple more of
Flask's capabilities.  The `request` object lets us inspect the message body
of the POST request, and the `abort()` function allows us to send error
messages to the user. Update your first line to

    from flask import Flask, jsonify, request, abort

This is the basic structure of Flask code to handle a POST request, to replace
the "fake" code for our second endpoint:

    @app.route("/api/profiles", methods=["POST"])
    def new_profile():
        # error checking: JSON required; "_id", "name" required
        if not request.json:
            abort(400) # error 400: bad request
        if not "_id" in request.json.keys():
            abort(400)
        if not "name" in request.json.keys():
            abort(400)
        # insert into database
        db.flinkedin.insert_one(request.json)
        return( jsonify({"status":"OK","id":request.json["_id"]}) )

This function is longer, but most of it is error checking and optional
for something you're just doing in the classroom.  The biggest changes
here are in the last two lines.  We insert the JSON data exactly into
MongoDB exactly as it was received.  (That's why we make sure that the
input contains MongoDB's required "_id" attribute.)  This is about as
easy as interacting with a database can be---and now you begin to see
why NoSQL options like MongoDB are so popular with web developers. In the 
following line, I construct the "OK" message using the unique id
of the data just inserted.  That's all there is to it.  

Test it with Postman or curl.

To add a new job to a profile's job history, in MongoDB we're doing an
update to an existing record and will use the `$push` operator... in 
computer science terms we're "pushing" new data on to the end of a list.

    @app.route("/api/profile/<id>/jobs", methods=["POST"])
    def new_job(id):
        # error checking. input requires "employer", "position", "start"
        if not request.json:
            abort(400) # error 400: bad request
        if not "employer" in request.json.keys():
            abort(400)
        # add job to list for existing profile
        db.flinkedin.update({"_id":id},
                            {"$push": {"jobs": request.json} })
        return( jsonify({"status":"OK","id":id}) )

The other difference here is that we're getting the unique id from the URL
instead of from the JSON of the request, because it's not a new profile.

One note: for a real web application to be used in production, we'd do a lot
more error checking.  With this simple code, there are a lot of ways you could
mess up, for example, by trying to insert two profiles with the same unique
`id`.  If you need to recover from an error, you might go directly to your
database (for example, MongoLab.com's web dashboard) and fix or delete the
data manually.

### Implementing the GET methods

The basic structure of a GET method handler is to execute a database query
and return the result as JSON.  That gives us the following:

@app.route("/api/profiles")
def fetch_profiles():
    # retrieve all users' names and unique ids
    all_profiles = list( db.flinkedin.find( {}, {"_id":1,"name":1} ) )
    return( jsonify({"profiles":all_profiles}) )

If you inspect the `all_profiles` variable you'll see that it's a list, and
although JSON may contain lists, the top-level data structure for JSON must
be a "dict" (actually a JavaScript object).  So when I feed the data to
`jsonify()`, I wrap it in a dict with just one key, "profiles".

The code to fetch just one profile is even simpler, using the MongoDB
`find_one()` method and matching the `id` part of the URL.
    
@app.route("/api/profile/<id>")
def fetch_one_profile(id):
    # fetch all details of one user's profile and job history
    profile = db.flinkedin.find_one({"_id":id})
    return( jsonify(profile) )
    
## Hosting a web app in the Cloud

TBD


## Homework

To complete the API we designed, implement the "/api/companies" and 
"api/company/<name>" endpoints for your API.  The primary challenge is
figuring out how to execute the queries in MongoDB.

You'll find the first one is more difficult than the second.  To get the
list of all companies named in the database, you may want to use the
`db.collection.distinct()` method found in the MongoDB documentation
[here](https://docs.mongodb.org/v3.0/reference/method/db.collection.distinct/).

Turn in the root URL for your web app in the cloud.  All endpoints should
be working and connected to a database. I will grade it by inserting a few 
new profiles of my own and checking to see if I get the right results.


