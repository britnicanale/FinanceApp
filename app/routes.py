import os
from app import app
from flask import render_template, session, url_for, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import random

app.config['MONGO_DBNAME'] = 'users' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/users?retryWrites=true&w=majority' 
mongo = PyMongo(app)


@app.route('/login')
def login():
    if "username" not in session:
        return render_template("login.html")
    return redirect(url_for("home"))
    
@app.route("/logout")
def logout():
    if 'username' in session:                
        session.clear()
    return redirect(url_for("login"))

"""@app.route("/welcome")
@app.route("/welcome", methods=["POST"])     
def welcome():
    if "username"not in session:              
        un = request.form["uname"]                
        pw = request.form["pword"]
        uncorrect = un == uname                   
        pwcorrect = pw == pword
        if uncorrect and pwcorrect:               
            session["username"] = uname     
            return render_template("welcome.html", uname = un)
        return render_template("error.html", username = uncorrect, password = pwcorrect)     
    return render_template("welcome.html", uname = uname)"""



@app.route('/')
def home():
    # connect to mongo.db and access collection known as events
    # find will find all the data
    # store collection as events and as a dictionary
    # always return message to user with template
    collection = mongo.db.users
    users = collection.find({})
    return render_template('home.html', users=users)

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
        #userId = last.charAt(0).upper() + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(userCount) 
        #for x in users:
            #if x['userId'] == userId:
            #userId += str(random.randint(0,10))
            
# song = collection.find_one
        
# CONNECT TO DB, ADD DATA