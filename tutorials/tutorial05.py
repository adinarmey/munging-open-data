# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 05:34:02 2016

@author: jwclark2
"""

from flask import Flask, jsonify
app = Flask(__name__)

# tutorial routes

@app.route("/")
def hello():
    return( "Hello world!" )

@app.route("/api")
def api_instructions():
    return( "API instructions will be provided here" )

@app.route("/home/<username>")
def home(username):
    return( "Hello " + username + "!" )


# API routes

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


if __name__ == "__main__":
    app.run()