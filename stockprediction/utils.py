from unicodedata import name
from urllib import request
import jwt
from pymongo import MongoClient
# from stockprediction.config import database
from django.http import HttpResponse
from django.contrib.auth import get_user
from django.utils.functional import SimpleLazyObject

from prediction.settings import DATABASES  
# DATABASES
CONNECTION_STRING = "mongodb+srv://shreya:shreya%40123@cluster0.6xbxf.mongodb.net/"
client = MongoClient(CONNECTION_STRING)
stock = client['mydb']
user_collection = stock["auth_user"]
stock_collection = stock["SearchStocks"]

def getAllUsers(search):
    result = user_collection.find({})
    stock = stock_collection.find({})
    if search != None:
        result = user_collection.find({'name' : search})
        r = []
        for i in result:
            r.append(i)
            checking = stock_collection.find_one({ "user" : i['_id'] } )
            if checking:
                r[-1]["search"] = checking["symbol"]
        # print(user)
    else:
        result = user_collection.find({})
        r = []
        for i in result:
            r.append(i)
            checking = stock_collection.find_one({ "user" : i['_id'] } )
            if checking:
                r[-1]["search"] = checking["symbol"]
    return r

def get_user_count():
    count = user_collection.count()
    return count

def get_stock_count():
    count = stock_collection.count()
    return count


def add_search(search,request):
    user = str(SimpleLazyObject(lambda: request.user))
    result = user_collection.find({ 'username': user })
    if stock_collection.find_one({ "user" : result[0]['_id'] } ) != None:
        if stock_collection.find_one({ "user" : result[0]['_id'] , 'symbol':{"$in": [search]}} ) != None:
            check = stock_collection.find_one_and_update({ "user" : result[0]['_id'] }, { '$push':{"symbol": search} })
            if check != None:
                check['symbol'].append(search)
            else:
                dict = { "user": result[0]['_id'], "symbol": [search]}
                stock_collection.insert_one(dict)
        else:
            check = stock_collection.find_one_and_update({ "user" : result[0]['_id'] }, { '$push':{"symbol": search} })
            if check != None:
                check['symbol'].append(search)
            else:
                dict = { "user": result[0]['_id'], "symbol": [search]}
                stock_collection.insert_one(dict)

    else:
        dict = { "user": result[0]['_id'], "symbol": [search]}
        stock_collection.insert_one(dict)