import os
from app import app
from flask import render_template, request, redirect
from flask_pymongo import PyMongo
import random

app.config['MONGO_DBNAME'] = 'users' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/users?retryWrites=true&w=majority' 
mongo = PyMongo(app)

@app.route('/')
@app.route('/index')

def index():
    # connect to mongo.db and access collection known as events
    # find will find all the data
    # store collection as events and as a dictionary
    # always return message to user with template
    collection = mongo.db.users
    users = collection.find({})
    return render_template('index.html', users=users)

@app.route('/add' ,methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return "Please enter your user information"
    else:
        collection = mongo.db.users
        users = collection.find({})
        first = request.form['first']
        last = request.form['last']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        bank = request.form['bank']
        users.insert({'first': first, 'last': last, 'dob': dob, 'email': email, 'password': password, 'bank': bank})
        userId = last.charAt(0).upper() + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) 
        #+str(userCount)
        for x in users:
            if x['userId'] == userId:
                userId += random.randint(0,10)
        users.insert({'userId': userId})
# CONNECT TO DB, ADD DATA