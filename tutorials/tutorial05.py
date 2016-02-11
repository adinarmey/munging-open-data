# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 05:34:02 2016

@author: jwclark2
"""

from flask import Flask, jsonify, request, abort
app = Flask(__name__)


# database connection
from pymongo import MongoClient
MONGO_URL = "mongodb://USERNAME:PASSWORD@SERVER.mongolab.com:PORT/DATABASE"
client = MongoClient(MONGO_URL)
db = client.get_default_database()



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
    all_profiles = list( db.flinkedin.find( {}, {"_id":1,"name":1} ) )
    return( jsonify({"profiles":all_profiles}) )

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

@app.route("/api/profile/<id>")
def fetch_one_profile(id):
    # fetch all details of one user's profile and job history
    profile = db.flinkedin.find_one({"_id":id})
    return( jsonify(profile) )

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


if __name__ == "__main__":
    app.run()