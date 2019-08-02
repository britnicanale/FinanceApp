
import os
import datetime
from app import app
from flask import render_template, session, url_for, request, redirect, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app.models import model, formopener

app.config['MONGO_DBNAME'] = 'users' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/users?retryWrites=true&w=majority' 
mongo = PyMongo(app)

app.secret_key = os.urandom(32)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if "username" in session:
        flash("You are already logged in")
        return redirect(url_for("home"))
    return render_template("login.html") 
    
    
@app.route("/logout")
def logout():
    if 'username' in session:    
        flash("You have successfully logged out")
        session.clear()
    return redirect(url_for("login"))


@app.route('/', methods  = ["POST", "GET"])
def home():
    users = mongo.db.users
    if "username"not in session:
        if "uname" not in request.form:
            flash("You are not logged in")
            return redirect(url_for("login"))
        un = request.form["uname"]                
        pw = request.form["pword"]
        user = list(users.find({'userName' : un}))
        #print(users)
        #print(un)
        #print(pw)
        if len(user)==1 and user[0]['password'] == pw:               
            session["username"] = un
            first = user[0]['first']
            flash("You have successfully logged in")
            if request.method == "GET" and "time" in request.args:
                if request.args['time'] == "monthly":
                    income = monthlyIncome()
                    savings = monthly()
                    time = "monthly"
                if request.args['time'] == "yearly":
                    income = yearlyIncome()
                    savings = yearly()
                    time = "yearly"
                if request.args['time'] == "weekly":
                    income = weeklyIncome()
                    savings = weekly()
                    time = "weekly"
            else:
                income = monthlyIncome()
                savings = monthly()
                time = "monthly"
            expenses = float(income) -float(savings)
            expenses = round(expenses,2)
            #print(savings)
            return render_template("home.html", first = first, income = income, savings = savings, expenses = expenses, time = time)
        flash("Your Credentials Are Incorrect")
        return redirect(url_for("login"))  
    if request.method == "GET" and "time" in request.args:
        if request.args['time'] == "monthly":
            income = monthlyIncome()
            savings = monthly()
            time = "monthly"
        if request.args['time'] == "yearly":
            income = yearlyIncome()
            savings = yearly()
            time = "yearly"
        if request.args['time'] == "weekly":
            income = weeklyIncome()
            savings = weekly()
            time = "weekly"
    else:
        income = monthlyIncome()
        savings = monthly()
        time = "monthly"
    expenses = float(income) -float(savings)
    expenses = round(expenses,2)
    first = users.find({'userName': session['username']
    })[0]['first']
    #print(savings)
    return render_template("home.html", first = first, income = income, savings = savings, expenses = expenses, time = time)
    
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
        if len(request.form['userName']) < 8 and len(request.form['password']) < 8 :
            flash("Make sure to have a username and password that exceeds 8 characters")
            return redirect(url_for("register"))
        if request.form['userName'].find(" ") != -1 and request.form['password'].find(" ") != -1 :
            flash("Make sure your username and password has no spaces")
            return redirect(url_for("register"))
        collection = mongo.db.users
        #users = collection.find({})
        first = request.form['first']
        last = request.form['last']
        if first.find(" ") != -1 or last.find(" ") != -1:
            first = request.form['first'].strip() 
            last = request.form['last'].strip()
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        userName = request.form['userName']
        #userId = collection.find_one({'_id': ObjectId(userName)})
        collection.insert({'first': first, 'last': last, 'dob': dob, 'email': email, 'password': password, 'userName': userName})
        flash("You have successfully created an account")
        return redirect(url_for('login'))

    else:
        flash("This username is already taken")
        return redirect(url_for("register"))
    return redirect(url_for("login"))
       
@app.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        flash("You are already logged in")
        return redirect(url_for("home"))
    return render_template('register.html')

app.config['MONGO_DBNAME'] = 'income' 
app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/income?retryWrites=true&w=majority' 
@app.route('/addincome', methods = ['GET'])
def income(): 
    if "username" not in session:
        return redirect(url_for("login"))
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
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("addexpense.html")
  

@app.route('/addexpense/execute', methods = ['GET', 'POST'])
def expenseexecute():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == 'GET':
        flash("You cannot access this route")
        return redirect(url_for("home"))
    if request.method == 'POST':
        collection = mongo.db.expenses
        #expenses = collection.find({})
        if request.form['isContinuous']:
            collection.insert({'amount': request.form['amount'], 'item': request.form['item'], 'frequency': request.form['frequency'], 'isContinuous': request.form['isContinuous'], 'timeperiod': request.form['timeperiod'], 'username': session['username'], 'date': request.form['date']})
        else:
             collection.insert({'amount': request.form['amount'], 'item': request.form['item'],  'isContinuous': request.form['isContinuous'], 'username': session['username'], 'date': request.form['date']})
        flash("You have successfully added an expense")
        return redirect(url_for("home"))
    

    
@app.route('/addincome/execute', methods = ['GET', 'POST'])
def incomeexecute():
    if "username" not in session:
        return redirect(url_for("login"))
    if request.method == 'GET':
        flash("You cannot access this route")
        return redirect(url_for("home"))
    if request.method == 'POST':
        collection = mongo.db.income
        if request.form['isContinuous']:
            #amount = request.form['amount']
            #print (isinstance(amount, float))
            collection.insert({'amount': request.form['amount'] , 
                                'source' : request.form['source'], 
                                'isContinuous': request.form['isContinuous'], 
                                'frequency': request.form['frequency'], 
                                'timeperiod': request.form['timeperiod'], 
                                'username': session['username'], 
                                'date': request.form['date']})
           
        else:
            collection.insert({'amount': request.form['amount'] , 
                                'source' : request.form['source'], 
                                'isContinuous': request.form['isContinuous'], 
                                'frequency': request.form['frequency'], 
                                'username': session['username'], 
                                'date': request.form['date']})
            
        flash("You have successfully added an income")
        return redirect(url_for("home"))
        

@app.route("/itemlist", methods = ['GET','POST'])
def items():
    if "username" not in session:
        return redirect(url_for("login"))
    expenses =list(mongo.db.expenses.find({"username":session['username']}))
    income = list(mongo.db.income.find({"username":session['username']}))
    #print(expenses)
    #print(income)
    return render_template("itemlist.html", income = income, expenses = expenses)

@app.route("/delete", methods = ["GET", "POST"])
def delete():
    if "username" not in session:
        flash("You are not logged in")
        return redirect(url_for("login"))
    if request.method == "GET":
        flash("This method is not allowed")
        return redirect(url_for("home"))
    if request.form["type"] == "expenses":
        expenses = mongo.db.expenses
        expenses.find_one_and_delete({"_id":ObjectId(request.form["id"])})
    else:
        income = mongo.db.income
        income.find_one_and_delete({"_id":ObjectId(request.form["id"])})
    return redirect(url_for("items"))
                           
@app.route("/account", methods = ["GET", "POST"])    
def account():
    if "username" not in session:
        flash("You are not logged in")
        return redirect(url_for("login"))
    collection = mongo.db.users
    user = list(collection.find({"userName":session["username"]}))[0]
    #print(user)
    return render_template("account.html", first = user['first'], last = user['last'], userName = user['userName'], password = user['password'], email = user['email'], dob = user['dob'])               


def yearly():
    collection = mongo.db.income
    #userdata = collection.find_one({'username': session['username']})
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.yearlyincome(amount, frequency, timeperiod, isContinuous)
    
    collection1 = mongo.db.expenses
    userdata1 = collection1.find({'username': session['username']})
    value1 = 0
    for entry in userdata1:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value1 += model.yearlyincome(amount, frequency, timeperiod, isContinuous)
    balance = value - value1 
    balance = round(balance,2)
    return str(balance)
    
    
def yearlyIncome():
    collection = mongo.db.income
    #userdata = collection.find_one({'username': session['username']})
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.yearlyincome(amount, frequency, timeperiod, isContinuous)
    value = round(value,2)
    return str(value)
    
    
def monthly():
    collection = mongo.db.income
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.monthlyincome(amount, frequency, timeperiod, isContinuous)
     
    collection1 = mongo.db.expenses
    userdata1 = collection1.find({'username': session['username']})
    value1 = 0
    for entry in userdata1:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value1 += model.monthlyincome(amount, frequency, timeperiod, isContinuous)
    balance = value - value1 
    balance = round(balance,2)
    return str(balance)
    
    
    
    
    
def monthlyIncome():
    collection = mongo.db.income
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.monthlyincome(amount, frequency, timeperiod, isContinuous)
    value = round(value,2)        
    return str(value)
    
def weekly():
    collection = mongo.db.income
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.weeklyincome(amount, frequency, timeperiod, isContinuous)
     
    collection1 = mongo.db.expenses
    userdata1 = collection1.find({'username': session['username']})
    value1 = 0
    for entry in userdata1:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value1 += model.weeklyincome(amount, frequency, timeperiod, isContinuous)
    balance = value - value1 
    balance = round(balance,2)
    return str(balance)

    
def weeklyIncome():
    collection = mongo.db.income
    userdata = collection.find({'username': session['username']})
    value = 0
    for entry in userdata:
        if entry['isContinuous'] == 'True':
            frequency = int(entry['frequency'])
            timeperiod = entry['timeperiod']
        else:
            frequency = 0
            timeperiod = ''
        amount = float(entry['amount'])
        isContinuous = entry['isContinuous']
        value += model.weeklyincome(amount, frequency, timeperiod, isContinuous)
    value = round(value,2)
    return str(value)







"""
@app.route("/calculate")
def calculateexpenses():
    collection1 = mongo.db.expenses
    #userdata = collection.find_one({'username': session['username']})
    userdata1 = collection1.find({'username': session['username']})
    value1 = 0
    for entry in userdata1:
        frequency = int(entry['frequency'])
        amount = float(entry['amount'])
        timeperiod = entry['timeperiod']
        isContinuous = entry['isContinuous']
        value1 += model.expensescalculate(amount, frequency, timeperiod, isContinuous)
    print(value1)
    return str(value1)
""" 


    
"""    
    frequency = int(userdata['frequency'])
    amount = float(userdata['amount'])
    timeperiod = userdata['timeperiod']
    isContinuous = userdata['isContinuous']
    print (isinstance(frequency, int))
    print(isinstance(amount, float))
    #print(timeperiod)
    #print(isContinuous)
    return model.incomecalculate(amount, frequency, timeperiod, isContinuous)
    #return render_template with float of income
"""
    
    #for key in userdata:
       # print(key)
       #if userdata[key] == 'frequency':
           #frequency = userdata[key]
          # print(frequency)
       # if userdata[key] == 'timeperiod' == 'day':
        # val = frequency * 7
        #if userdata[key] == 'timeperiod' == 'week':
         #val = frequency 
      # if userdata[key] == 'timeperiod' == 'month':
         #val = float(frequency / 4)
       # if userdata[key] == 'amount':
        # amount = userdata[key]
         #val *= amount
 