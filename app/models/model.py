"""
from flask_pymongo import PyMongo
#from app import app
import pymongo
from pymongo import MongoClient

#app.config['MONGO_DBNAME'] = 'income' 
#app.config['MONGO_URI'] = 'mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/income?retryWrites=true&w=majority' 
#mongo = PyMongo(app)


def weekly(username):
    client = MongoClient('mongodb+srv://admin:Fdc69t6o4s5Pjx65@cluster0-rqyqd.mongodb.net/income?retryWrites=true&w=majority')
    db = client['income']
    collection = db.income
    data = list(collection.find({'username': username}))
    #list(mongo.db.income.find({'userName' : username}))
    #data = list(collection.find({'userName': username}))
    #return data
    #print(weekly("bubbly_britni"))
    #frequency = collection.find({'frequency'})
    #continuous = collection.find({'isContinuous'})
    return data
print(weekly('bubbly_britni'))

"""
def incomecalculate(amount,frequency, timeperiod, isContinuous):
    income = 0.0
    if isContinuous == 'True':
        if timeperiod == 'day':
            income += amount * float(365/frequency)
        elif timeperiod == 'week':
            income += amount * float(52/frequency)
        elif timeperiod == 'month':
            income += amount * float(12/frequency)
    else:
        income += amount
    print (income)
    #return str(income)
    return income 
        
        
        
