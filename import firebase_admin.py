# #start of json to firebase

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# import json

# # Get the JSON file
# with open('data.json') as f:
#     data = json.load(f)

# # with open('dxbarr.json') as f:
# #     datadxb = json.load(f)

# # Get your Firebase credentials file
# cred = credentials.Certificate('atfm-5c750-firebase-adminsdk-4gr64-226e7d7b2b.json')

# # Initialize the app with a service account, granting admin privileges
# firebase_admin.initialize_app(cred, {
#     # 'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com/'
#     'databaseURL': 'https://atfm-5c750-default-rtdb.firebaseio.com/'
    
#     # 'databaseURL': 'https://console.firebase.google.com/project/atfm-5c750/database/atfm-5c750-default-rtdb/data/~2F'
# })

# # Get a database reference
# ref = db.reference()

# # Set the data in the Real-time Database
# users = ref.child('users')
# users.set(data)


# # end of json to firebase

from flask import Flask, render_template, request,flash
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
import json
from datetime import datetime
import csv
# import openpyxl
# import streamlit as st
# import xlrd
# import chardet

import pandas as pd
import MySQLdb as mysql
import mysql.connector
import haversine as hs
from sklearn.preprocessing import OneHotEncoder
import pickle

dbcur = mysql.connector.connect(user='root',password='',host='localhost',database='codingthunder')
cursor = dbcur.cursor() 

# xlrd.xlsx.ensure_elementtree_imported(False,None)
# xlrd.xlsx.Element_has_iter = True

# hyd_ar = pd.read_csv("hydairport_arrivals.csv",encoding='windows-1252',low_memory=False)
# hyd_ar.to_html('hyd_Arv.html')

# exl = xlrd.open_workbook("Airport_Arrival_Departure_Data.xlsx")
# df = exl.sheet_by_index(0)
# excel_file = "Airport_Arrival_Departure_Data.xlsx"
# sheet_name = 'hyd_arrival'

# df = pd.read_excel("Airport_Arrival_Departure_Data.xlsx")
# new = df.to_html()

# df = pd.read_excel(excel_file,sheet_name=sheet_name,usecols='B:D',header = 3)
# st.dataframe(df)
# print(st)
# print(df)

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD=  params['gmail-password']
# )

# mail = Mail(app)
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db = SQLAlchemy(app)

from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials, db

# Get your Firebase credentials file
cred = credentials.Certificate('atfm-5c750-firebase-adminsdk-4gr64-226e7d7b2b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    # 'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com/'
    'databaseURL': 'https://atfm-5c750-default-rtdb.firebaseio.com/'
    
    # 'databaseURL': 'https://console.firebase.google.com/project/atfm-5c750/database/atfm-5c750-default-rtdb/data/~2F'
})

@app.route("/",methods=['GET','POST'])
def index():
    ref = db.reference('/dxbarr')
    data = ref.get()
    print(type(data))
    print(data)
    # headers = data[0].keys()
    # dat=data[0].values()
    headers = data[0].keys()
    # return render_template('ind.html', headers=headers, data=data)
    return render_template('ind.html', data=data)

app.run(debug=True)
