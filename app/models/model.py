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
def yearlyincome(amount,frequency, timeperiod, isContinuous):
    income = 0.0
    if isContinuous == 'True':
        if frequency > 0:
          if timeperiod == 'day':
            income += amount * float(365/frequency)
          elif timeperiod == 'week':
            income += amount * float(52/frequency)
          elif timeperiod == 'month':
            income += amount * float(12/frequency)
          elif timeperiod == 'year':
              income += amount * float(1/frequency)
    else:
        income += amount
    #print (income)
    #return str(income)
    return income 
        
        
def yearlyexpenses(amount,frequency, timeperiod, isContinuous):
    expenses = 0.0
    if isContinuous == 'True':
        if frequency > 0:
            if timeperiod == 'day':
             expenses += amount * float(365/frequency)
            elif timeperiod == 'week':
             expenses += amount * float(52/frequency)
            elif timeperiod == 'month':
             expenses += amount * float(12/frequency)
            elif timeperiod == 'year':
             expenses += amount * float(1/frequency)
    else:
        expenses += amount
    return expenses  
        
def monthlyincome(amount, frequency, timeperiod, isContinuous):
    income = 0.0
    if isContinuous == 'True':
        if frequency> 0:
         if timeperiod == 'day':
             income += amount * float(30/frequency)
         elif timeperiod == 'week':
             income += amount * float(4/frequency)
         elif timeperiod == 'month':
             income += amount * float(1/frequency)
         elif timeperiod == 'year':
             income += amount * float(1/(12 * frequency))
    else:
        income += amount
    return income 
        
        
def monthlyexpenses(amount,frequency, timeperiod, isContinuous):
    expenses = 0.0
    if isContinuous == 'True':
        if frequency > 0:
         if timeperiod == 'day':
             expenses += amount * float(30/frequency)
         elif timeperiod == 'week':
             expenses += amount * float(4/frequency)
         elif timeperiod == 'month':
             expenses += amount * float(1/frequency)
         elif timeperiod == 'year':
             expenses += amount * float(1/(12 * frequency))
    else:
        expenses += amount
    return expenses  
    
    
    
def weeklyincome(amount, frequency, timeperiod, isContinuous):
    income = 0.0
    if isContinuous == 'True':
        if frequency > 0:
         if timeperiod == 'day':
             income += amount * float(7/frequency)
         elif timeperiod == 'week':
             income += amount * float(1/frequency)
         elif timeperiod == 'month':
             income += amount * float(1/(4* frequency))
        elif timeperiod == 'year':
             income += amount * float(1/(52*frequency))
    else:
        income += amount
    return income 


def weeklyexpenses(amount,frequency, timeperiod, isContinuous):
    expenses = 0.0
    if isContinuous == 'True':
        if frequency > 0:
         if timeperiod == 'day':
             expenses += amount * float(7/frequency)
         elif timeperiod == 'week':
             expenses += amount * float(1/frequency)
         elif timeperiod == 'month':
             expenses += amount * float(1/(4 *frequency))
         elif timeperiod == 'year':
             expenses += amount * float(1/(52*frequency))
    else:
        expenses += amount
    return expenses  
    

        

        
