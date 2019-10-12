from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

import pymongo
from frontpage import *
import requests

# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json


#PayPal sandbox details
client_id = "AYSxY3_hsJ1TI8v8KbARDN0tbfmhJNn_ldWWQD-b1unGmGtLpCT7Tyq5HE5Rq9KmLdIvmmaLvz54zyn6"
secret = "EJhe5Mnw12_uxK1kGwwH64seEQWz5Gd0s6_JRou6WotFxlz_cr9NAHwI82P4-OlgfuFue4poA-RF6mCG"
redirect_url = "http://127.0.0.1:8000/redirect"


app = Flask(__name__)


# Connect to database and create database session
myclient = pymongo.MongoClient("mongodb+srv://moolaAdmin:hackathon@moola-4by6t.mongodb.net/test?retryWrites=true&w=majority")

#Connect or create moolaDatabase
mydb = myclient["moolaDatabase"]

# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# Display all things
@app.route('/')
def showMain():
    things = ["thing1", "thing2", "cat-in-the-hat"]

    return render_template('things.html', things=things)


#get authorization code and exchange for access token.
@app.route('/redirect')
def exchange_token():
    print(request.args.get('code'))
    return 'hello'

@app.route('/login')
def login():
    link = "https://www.sandbox.paypal.com/connect?flowEntry=static&client_id=" + client_id + "&scope=openid&redirect_uri=" + redirect_url
    return redirect(link)

@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        if create_user(username=request.form['username'],
                       password=request.form['password'],
                       confirmation=request.form['confirm_pass'],
                        firstName=request.form['first_name'],
                        lastName=request.form['last_name'],
                        email=request.form('email'),
                       dbclient=myclient):
            return 'hello'
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    #app.debug = True
    app.run(host='127.0.0.1', port=8000)
