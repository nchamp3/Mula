from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash

import pymongo


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

mydb = myclient["userDatabase"]

# engine = create_engine('sqlite:///flaskstarter.db')
# Base.metadata.bind = engine

# DBSession = sessionmaker(bind=engine)
# session = DBSession()


# Display all things
@app.route('/')
def showMain():
    things = ["thing1", "thing2", "cat-in-the-hat"]

    return render_template('things.html', things=things)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
