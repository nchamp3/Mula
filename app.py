from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

import pymongo
from frontpage import *

# from sqlalchemy import create_engine, asc, desc, \
#     func, distinct
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.serializer import loads, dumps

# from database_setup import Base, Things

import random
import string
import logging
import json


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

@app.route('/register', methods=['POST', 'GET'])
def login():
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
    create_user(username='abc',
                password='xyz',
                confirmation='xyz',
                firstName='bla',
                lastName='bla',
                email='xax',
                dbclient=myclient)
    #app.debug = True
    #app.run(host='127.0.0.1', port=8000)
