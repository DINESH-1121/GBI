
# start of excel to json code

import pandas
import json

# Read excel document
dxbarrexcel = pandas.read_csv('DXB_ARRIVAL_DB.csv')
dxbdepexcel = pandas.read_csv('DXB_DEPARTURE_DB.csv')
hydarrexcel = pandas.read_csv('HYD_ARRIVAL_DB.csv')
hyddepexcel = pandas.read_csv('HYD_DEPARTURE_DB.csv')
# dxbdepexcel = pandas.read_excel('dxbairport_departure.xlsx', sheet_name='sheet1')

# Convert excel to string 
# (define orientation of document in this case from up to down)
dxbarrstring = dxbdepexcel.to_json(orient='records')
dxbdepstring = dxbarrexcel.to_json(orient='records')
hydarrstring = hydarrexcel.to_json(orient='records')
hyddepstring = hyddepexcel.to_json(orient='records')

# Print out the result
# print('Excel Sheet to JSON:\n', dxbdepstring)

# Make the string into a list to be able to input in to a JSON-file
dxbarrjson = json.loads(dxbarrstring)
dxbdepjson = json.loads(dxbdepstring)
hydarrjson = json.loads(hydarrstring)
hyddepjson = json.loads(hyddepstring)

# Define file to write to and 'w' for write option -> json.dump() 
# defining the list to write from and file to write to
with open('dxbarr.json', 'w') as json_file:
    json.dump(dxbarrjson, json_file)
with open('dxbdep.json', 'w') as json_file:
    json.dump(dxbdepjson, json_file)
with open('hydarr.json', 'w') as json_file:
    json.dump(hydarrjson, json_file)
with open('hyddep.json', 'w') as json_file:
    json.dump(hyddepjson, json_file)

# end of excel to json code

#start of json to firebase

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json

# Get the JSON file
with open('dxbarr.json') as f:
    dxbarrdata = json.load(f)
with open('dxbdep.json') as f:
    dxbdepdata = json.load(f)
with open('hydarr.json') as f:
    hydarrdata = json.load(f)
with open('hyddep.json') as f:
    hyddepdata = json.load(f)

# Get your Firebase credentials file
cred = credentials.Certificate('atfm-5c750-firebase-adminsdk-4gr64-226e7d7b2b.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    # 'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com/'
    'databaseURL': 'https://atfm-5c750-default-rtdb.firebaseio.com/'
    
    # 'databaseURL': 'https://console.firebase.google.com/project/atfm-5c750/database/atfm-5c750-default-rtdb/data/~2F'
})

# Get a database reference
ref = db.reference()

# Set the data in the Real-time Database
# ref.set(data)
dxbarrref = ref.child('dxbarr')
dxbarrref.set(dxbarrdata)
dxbdepref = ref.child('dxbdep')
dxbdepref.set(dxbdepdata)
hydarrref = ref.child('hydarr')
hydarrref.set(hydarrdata)
hyddepref = ref.child('hyddep')
hyddepref.set(hyddepdata)


# end of json to firebase
