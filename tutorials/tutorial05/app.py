# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 05:34:02 2016

@author: jwclark2
"""

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return( "Hello world!" )

if __name__ == "__main__":
    app.run()