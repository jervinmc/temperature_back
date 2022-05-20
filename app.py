from flask import Response
from flask import Flask, jsonify, request,redirect
from flask_restful import Resource, Api
from flask_cors import CORS
from datetime import datetime
import smtplib
from Database import Database
import boto3
import jwt
import os
import schedule
import time
import string
import random
from decouple import config
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
now = datetime.now().date()
import datetime
app=Flask(__name__)
CORS(app)
api=Api(app)
from decouple import config

import pusher
from decouple import config
pusher_client = pusher.Pusher(
  app_id=config('app_id'),
  key=config('pusher_key'),
  secret=config('secret_key'),
  cluster=config('cluster'),
  ssl=True
)

# class Temperature(Resource):
#     def __init__(self):
#         self.db=Database()

#     # def post(self,pk=None):
#     #     data = request.get_json()
#     #     try:
#     #         self.db.insert(f"INSERT INTO users(email,password) values('{data.get('email')}','{data.get('password')}')")
#     #         return {"status":"success"}
#     #     except Exception as e:
#     #         print(e)
#     #         return {"status":"Failed Input"}

#     def get(self,pk=None):
#         data = self.db.query("SELECT * FROM thermal")
#         listitem = []
#         for x in data:
#             listitem.append({"id":x[0],"temperature":x[1]})
#         return listitem


# class Temperature(Resource):
#     def __init__(self):
#         self.db=Database()


#     def get(self,pk=None):
#         data = self.db.query("SELECT * FROM thermal")
#         listitem = []
#         for x in data:
#             listitem.append({"id":x[0],"temperature":x[1]})
        # return listitem


class Notification(Resource):
    def __init__(self):
        self.db=Database()


    def get(self,pk=None):
        data = self.db.query("SELECT * FROM notification")
        listitem = []
        for x in data:
            listitem.append({"title":x[0],"date":x[1],"isViewed":x[2]})
        return listitem

    def post(self,pk=None):
        ct = datetime.datetime.now()
        res = request.get_json()
        data = self.db.insert(f"INSERT INTO notification values('{res.get('title')}','{ct}','no')")
        pusher_client.trigger('notification', 'my-test', {'temp': res.get("temperature"),'user_id':res.get("user_id")})
        # listitem = []
        # for x in data:
        #     listitem.append({"id":x[0],"temperature":x[1]})
        return data
    
    def patch(self,pk=None):
        self.db.insert(f"UPDATE notification set isViewed='yes'")
        return ""

class Temperature(Resource):
    def __init__(self):
        self.db=Database()


    def get(self,pk=None):
        print("test")
        data = self.db.query("SELECT * FROM thermal order by id DESC")
        listitem = []
        for x in data:
            listitem.append({"id":x[0],"temperature":x[1],"date":x[2]})
        return listitem

    def post(self,pk=None):
        ct = datetime.datetime.now()
        res = request.get_json()
        data = self.db.insert(f"INSERT INTO thermal(temp,date) values({res.get('temperature')},'{ct}')")
        if(res.get('temperature')>38):
            self.db.insert(f"INSERT INTO notification values('New high temp detected ! {res.get('temperature')} at blk1 lot 35 sterling manors subd. Anabu 1-c','{ct}','no')")
            pusher_client.trigger('notification', 'my-test', {'temp': res.get("temperature"),'user_id':res.get("user_id")})
        pusher_client.trigger('temperature', 'my-test', {'temp': res.get("temperature"),'user_id':res.get("user_id")})
        # listitem = []
        # for x in data:
        #     listitem.append({"id":x[0],"temperature":x[1]})
        return data
        


class TempSend(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,pk=None):
        data = self.db.insert(f"INSERT INTO thermal(temp,date) values({pk},'{ct}')")
        pusher_client.trigger('temperature', 'my-test', {'temp': pk,'user_id':''})
        # listitem = []
        # for x in data:
        #     listitem.append({"id":x[0],"temperature":x[1]})
        return data

class UserRecord(Resource):
    def __init__(self):
        self.db=Database()


    def get(self,pk=None):
        data = self.db.query("SELECT * FROM users_record")
        listitem = []
        for x in data:
            listitem.append({"firstname":x[0],"lastname":x[1],"age":x[2],"address":x[3],"gender":x[4],"temp":str(x[5]),"date":x[6],"status":x[7]})
        return listitem

    def post(self,pk=None):
        ct = datetime.datetime.now()
        res = request.get_json()
        data = self.db.insert(f"INSERT INTO users_record values('{res.get('firstname')}','{res.get('lastname')}',{res.get('age')},'{res.get('address')}','{res.get('gender')}',{res.get('temp')},'{ct}','{res.get('status')}')")
        # pusher_client.trigger('temperature', 'my-test', {'temp': res.get("temperature"),'user_id':res.get("user_id")})
        # listitem = []
        # for x in data:
        #     listitem.append({"id":x[0],"temperature":x[1]})
        return data 
    
    def patch(self,pk=None):
        res = request.get_json()
        self.db.insert(f"update users_record set status='{res.get('status')}' where firstname='{res.get('firstname')}' and lastname='{res.get('lastname')}'")
        # pusher_client.trigger('temperature', 'my-test', {'temp': res.get("temperature"),'user_id':res.get("user_id")})
        # listitem = []
        # for x in data:
        #     listitem.append({"id":x[0],"temperature":x[1]})
        return "" 



class Dashboard(Resource):
    def __init__(self):
        self.db=Database()

    def get(self,pk=None):
        res = self.db.query("SELECT * FROM users_record where age>6 and age<25")
        return res


class Usermanagement(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        data = request.get_json()
        res = self.db.insert(f"INSERT INTO usermanagement values(1,'{data.get('email')}','{data.get('password')}','{data.get('account_type')}')")
        return res
    def get(self,pk=None):
        listitem = []
        try:
            res = self.db.query(f"SELECT * FROM usermanagement")
            for x in res:
                listitem.append({"email":x[1],"account_type":x[3]})
            return listitem 
        except Exception as e:
            print(e)
            return ""

class Logs(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        ct = datetime.datetime.now()
        data = request.get_json()
        res = self.db.insert(f"INSERT INTO logs values('{data.get('email')}','{data.get('account_type')}','{ct}')")
        return res
        
    def get(self,pk=None):
        print("okay")
        listitem = []
        try:
            res = self.db.query(f"SELECT * FROM logs")
            print(res)
            for x in res:
                listitem.append({"email":x[0],"account_type":x[1],"timestamp":str(x[2])})
            return listitem 
        except Exception as e:
            print(e)
            return ""


class Login(Resource):
    def __init__(self):
        self.db=Database()

    def post(self,pk=None):
        data = request.get_json()
        # print(data)
        print("OKAYYYY")
        try:
            res = self.db.query(f"SELECT * FROM usermanagement where email='{data.get('email')}' and password='{data.get('password')}'")
            if(res==[]):
                print(res)
                return {"status":400}
            else:
                print(res[0][0])
                return {"id":res[0][0],"email":res[0][1],"password":res[0][2],"account_type":res[0][3],"status":201}
            
        except Exception as e:
            print(e)
            return {"status":"Failed Input"}




api.add_resource(Temperature,'/api/v1/temperature')
api.add_resource(TempSend,'/api/v1/tempsend/<string:pk>')
api.add_resource(Login,'/api/v1/login')
api.add_resource(UserRecord,'/api/v1/user_record')
api.add_resource(Notification,'/api/v1/notification')
api.add_resource(Dashboard,'/api/v1/dashboard')
api.add_resource(Usermanagement,'/api/v1/usermanagement')
api.add_resource(Logs,'/api/v1/logs')



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=config("PORT"))