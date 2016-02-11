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
def new_job():
    # send a message indicating successful post
    fake_data = {"status":"OK","id":"existinguser77"}
    return( jsonify(fake_data) )

@app.route("/api/companies")
def fetch_companies():
    # retrieve all unique company names in the database
    fake_data = {"companies": [ 
                    {"name":"NYPD"},
                    {"name":"MIB"},
                    {"name":"Bag End"}
                             ] }
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
    
Create a "linkedin" like RESTful API that allows us to GET and POST user 
profiles, using Python and Flask.  Run it from the command line.
Put it up on Heroku and get a URL for
the app.  Test with Postman or curl or the Python "requests" library.  Create 
a new endpoint that allows us
to add a "job" detail to the profile.

## Homework

Implement a /companies endpoint that shows all companies in the dataset. Add
a /company/<name> endpoint that returns the list of all profiles that have 
worked for that company.  Test and check if it works.

Turn in your URL.  I will grade it by inserting a few new profiles of my own 
and checking
to see if I get the right result.


