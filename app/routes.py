import os
from app import app
from flask import render_template, session, url_for, request, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app.config['MONGO_DBNAME'] = 'users' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/users?retryWrites=true&w=majority' 
mongo = PyMongo(app)


app.secret_key = os.urandom(32)

@app.route('/login', methods = ['POST', 'GET'])
def login():
#    if "userName" not in session:
#         un = request.form['username']
#         pw = request.form['password']
#         uncorrect = un == username                   
#         pwcorrect = pw == password
#         if uncorrect and pwcorrect:
#           session['username'] = un
#           return render_template("login.html", username = un)
#         return render_template("error.html")
    return render_template("login.html") 
    
    
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


#uname = "fintech"
#pword = "focus"

@app.route('/', methods  = ["POST", "GET"])
def home():
    if "username"not in session:
        if "uname" not in request.form:
            return redirect(url_for("login"))
        un = request.form["uname"]                
        pw = request.form["pword"]
        users = mongo.db.users
        user = list(users.find({'userName' : un}))
        print(users)
        print(un)
        print(pw)
        if "userName" in user[0] and user[0]['password'] == pw:               
            session["username"] = un
            return render_template("home.html", uname = un)
        flash("Your Credentials Are Incorrect")
        return redirect(url_for("login"))    
    return render_template("home.html", uname = session['username'])
    
    """
    #flash("HELLO WHAT'S GOING ON")
    # connect to mongo.db and access collection known as events
    # find will find all the data
    # store collection as events and as a dictionary
    # always return message to user with template
    collection = mongo.db.users
    users = collection.find({})
    return render_template('home.html', users=users)
"""



@app.route('/register/execute', methods=['GET', 'POST'])
def registerexecute():
    if request.method == 'GET':
        return redirect(url_for("register"))
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'userName' : request.form['userName']})
    if existing_user is None:
        collection = mongo.db.users
        #users = collection.find({})
        first = request.form['first']
        last = request.form['last']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        userName = request.form['userName']
        #userId = collection.find_one({'_id': ObjectId(userName)})
        collection.insert({'first': first, 'last': last, 'dob': dob, 'email': email, 'password': password, 'userName': userName}) #, 'userId': userId})
        return redirect(url_for('login'))
    return redirect(url_for("login"))
       
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template('register.html')

app.config['MONGO_DBNAME'] = 'income' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/income?retryWrites=true&w=majority' 
@app.route('/addincome', methods = ['GET'])
def income(): 
    #if request.method == 'GET':
       # return "Please use the homepage"
    #collection = mongo.db.income
    #income = collection.find({})
    #income.insert({'amount': request.form['amount'] ,'type': request.form['type'], 'source' : request.form['source'], session['userName']})
    return render_template("addincome.html")


app.config['MONGO_DBNAME'] = 'expenses' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/expenses?retryWrites=true&w=majority' 
@app.route("/addexpense", methods = ['POST', 'GET'])
def expense():
    if request.method == 'GET':
        return "Please login"
    collection = mongo.db.expenses
    expenses = collection.find({})
    expenses.insert({'amount': request.form['amount'], 'item': request.form['item'], 'type': request.form['type']})
    return render_template("addexpense.html")
    
    
    

    



