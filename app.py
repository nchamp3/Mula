from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, session

import pymongo
from database import *
import requests
import pprint

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

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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

    return redirect('/login')


#get authorization code and exchange for access token.
@app.route('/redirect')
def exchange_token():
    auth_code = request.args.get('code')
    params = {"grant_type": "authorization_code","code": auth_code}
    url = "https://" + client_id + ":" + secret + "@api.sandbox.paypal.com/v1/oauth2/token"

    #Get Refresh token
    api_call = requests.post(url=url, data= params)
    a = json.loads(api_call.text)
    refresh_token = a["refresh_token"]

    #Get Access Token
    params = {"grant_type": "refresh_token","refresh_token": refresh_token}
    api_call = requests.post(url=url, data=params)
    a = json.loads(api_call.text)


    #Gather user data.
    session['access_token'] = a["access_token"]
    access_token = a["access_token"]
    head = {"Authorization": "Bearer " + str(access_token)}
    url = "https://api.sandbox.paypal.com/v1/identity/oauth2/userinfo?schema=paypalv1.1"
    api_call = requests.get(url=url, headers=head)
    a = json.loads(api_call.text)
    user_id = a["user_id"].split("/")[-1]
    session['user_id'] = user_id
    create_user(user_id, myclient)
    return redirect('dashboard')

@app.route('/dashboard')
def dashboard():
    return 'dashboard here'

@app.route('/login')
def login():
    if 'access_token' in session:
        return redirect('dashboard')
    else:
        link = "https://www.sandbox.paypal.com/connect?flowEntry=static&client_id=" + client_id + "&scope=openid profile email&redirect_uri=" + redirect_url
        return redirect(link)

@app.route('/logout')
def logout():
    session.pop('access_token', None)
    session.pop('user_id', None)
    return redirect('login')

@app.route('/history')
def transactionHistory():
    access_token = session["access_token"]
    print(access_token)
    url = "https://api.sandbox.paypal.com/v1/reporting/transactions"
    head = {"Authorization": "Bearer " + str(access_token)}
    params = {"start_date": "2019-10-11T00:00:00-0700", "end_date": "2019-10-12T08:00:00-0700"}
    #requests.
    data = json.dumps(params)
    api_call = requests.get(url=url, headers=head, params = params)
    transactions = json.loads(api_call.text)
    for i in transactions["transaction_details"]:
        check_transaction(i,session['user_id'], myclient)

    return 'History'

@app.route('/payout')
def makePayout():
    access_token = session["access_token"]
    url = "https://api.sandbox.paypal.com/v1/payments/payouts"
    head = {"Authorization": "Bearer " + str(access_token)}
    data = {
  "sender_batch_header": {
    "sender_batch_id": "Payouts_2018_100007",
    "email_subject": "You have a payout!",
    "email_message": "You have received a payout! Thanks for using our service!"
  },
  "items": [
    {
      "recipient_type": "EMAIL",
      "amount": {
        "value": "9.87",
        "currency": "USD"
      },
      "note": "Thanks for your patronage!",
      "receiver": "sb-wqtt8386598@personal.example.com",
    }
  ]
}
    api_call = requests.post(url=url, headers=head, data=data)
    print(api_call.content)
    return 'payment'



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
