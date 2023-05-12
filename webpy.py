
# start of excel to json code

from flask import Flask, render_template, request, flash
import pickle
from sklearn.preprocessing import OneHotEncoder
import haversine as hs
import pandas as pd
import csv
from firebase_admin import db as dbf
from firebase_admin import credentials
import firebase_admin
import pandas
import json
from flask import session
from flask_session import Session

from datetime import datetime
from datetime import date
dt = datetime.now()

# Read excel document
if(dt.weekday() % 2 == 0):
    gbiarrexcel = pandas.read_excel('GBIarrivalmonday.xlsx')
    gbidepexcel = pandas.read_excel('GBIdeparturemonday.xlsx')
else:
    gbiarrexcel = pandas.read_excel('GBIarrivalsaturday.xlsx')
    gbidepexcel = pandas.read_excel('GBIdeparturesaturday.xlsx')
# dxbdepexcel = pandas.read_excel('dxbairport_departure.xlsx', sheet_name='sheet1')

# Convert excel to string
# (define orientation of document in this case from up to down)
gbiarrstring = gbiarrexcel.to_json(orient='records')
gbidepstring = gbidepexcel.to_json(orient='records')

# Print out the result
# print('Excel Sheet to JSON:\n', dxbdepstring)

# Make the string into a list to be able to input in to a JSON-file
gbiarrjson = json.loads(gbiarrstring)
gbidepjson = json.loads(gbidepstring)

# Define file to write to and 'w' for write option -> json.dump()
# defining the list to write from and file to write to
with open('gbiarr.json', 'w') as json_file:
    json.dump(gbiarrjson, json_file, default=str)
with open('gbidep.json', 'w') as json_file:
    json.dump(gbidepjson, json_file, default=str)

# end of excel to json code

# start of json to firebase


# Get the JSON file
with open('gbiarr.json') as f:
    gbiarrdata = json.load(f)
with open('gbidep.json') as f:
    gbidepdata = json.load(f)

# Get your Firebase credentials file
cred = credentials.Certificate(
    'projectk-18b95-firebase-adminsdk-cpkw4-65caedc756.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    # 'databaseURL': 'https://<DATABASE_NAME>.firebaseio.com/'
    # 'databaseURL': 'https://atfm-5c750-default-rtdb.firebaseio.com/'
    'databaseURL': 'https://projectk-18b95-default-rtdb.firebaseio.com/'
    # 'databaseURL': 'https://console.firebase.google.com/project/atfm-5c750/database/atfm-5c750-default-rtdb/data/~2F'
})

# Get a database reference
ref = dbf.reference()

# Set the data in the Real-time Database
# ref.set(data)
gbiarrref = ref.child('gbiarr')
gbiarrref.set(gbiarrdata)
gbidepref = ref.child('gbidep')
gbidepref.set(gbidepdata)

# end of json to firebase


local_server = True
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

global temp
temp = 0


@app.route("/", methods=['GET', 'POST'])
def home():
    # global temp
    temp = 100
    ref1 = dbf.reference('/gbiarr')
    data = ref1.get()
    headers = data[0].keys()
    if request.method == 'POST':
        session['username'] = temp
        if request.form.get('gbiarrhtml') == "0":
            temp = 1
            session['username'] = temp
            ref1 = dbf.reference('/gbiarr')
        elif request.form.get('gbidephtml') == "1":
            # cursor.execute("Select *from dubai_departure;")
            temp = 2
            session['username'] = temp
            ref1 = dbf.reference('/gbidep')
        else:
            return render_template('index.html')

        data = ref1.get()
        headers = data[0].keys()
        return render_template('index.html', headers=headers, res=data)
        # return render_template('index.html',headers=headers, params=params, res = data)
    else:
        return render_template('index.html', headers=headers, res=data)
        # return render_template('index.html',headers=headers, params=params,res=data)


@app.route("/redirect", methods=['GET', 'POST'])
def redirect():
    if request.method == 'POST':

        temp = session['username']
        # print(type(request.form.get('insubmit')))
        # print(request.form.get('insubmit'))
        # print(type(request.form.get('insubmitcontent')))
        # print(request.form.get('insubmitcontent'))
        # print(datetime.strptime(request.form.get('insubmitcontent'),'%H:%M:%S').time())
        # print(type(datetime.strptime(request.form.get('insubmitcontent'),'%H:%M:%S').time()))

        sno = int(request.form.get('insubmit'))
        print(type(sno))
        print(sno)

        str1 = 'insubmitcontent'+str(sno)
        # atd = datetime.strptime(request.form.get(str1),'%H:%M:%S').time()
        atd = request.form.get(str1)
        # print(temp)
        print(atd)
        # print(t)
        if temp == 0 or temp == 1:
            ref3 = dbf.reference('/gbiarr')
            loaded_model = pickle.load(open("bayesgbiarr_file", 'rb'))
            dff = pd.read_csv("gbiarrflask.csv")
        elif temp == 2:
            # ref3 = dbf.reference('/gbidep')
            ref4 = dbf.reference('/gbidep')
            loaded_model = pickle.load(open("lingbidep_file", 'rb'))
            dff = pd.read_csv("gbidepflask.csv")

        # updating referenced database atd value
        db_sno = str(sno-1)
        atd_update = {
            'ATD': atd
        }
        # ref2.update({'ATD': '%(atd)s'})
        if temp == 0 or temp == 1:
            ref3.child(db_sno).update(atd_update)
            # retreiving dxbarr dataframe of edited atd
            # data = ref2.get()
            df_sno = ref3.child(db_sno).get()
        elif temp == 2:
            ref4.child(db_sno).update(atd_update)
            # retreiving dxbarr dataframe of edited atd
            # data = ref2.get()
            df_sno = ref4.child(db_sno).get()
        # print(dxbarr_df_sno)

        # # updating referenced database pta value
        # pta_update = {
        #     'PTA' : pta
        # }
        # ref3.child(db_sno).update(pta_update)
        # # ref2.update({'PTA':'%(pta)s'})
        # # retreiving dxbarr data
        # dxbarr_data = ref3.get()

        # cursor.execute(sql, { 'atd': atd,'sno': sno })
        # cursor.execute(query,{'sno':sno})
        # res=cursor.fetchall()
        # print(type(res))
        # df= pd.DataFrame(res)
        # print(dxbarr_df_sno)

        df = pd.DataFrame(df_sno, index=[0])
        ap = pd.read_csv("airports.csv")
        # df.columns=['SNO','DATE','FLIGHTS','AIRCRAFT','STA','STD','FROM','TO','ATD','PTA']
        # print(df.columns)
        # print(df)

        column_headers = list(df.columns.values)
        for column in column_headers:
            if(column == "Unnamed: 12"):
                df.drop(["Unnamed: 12"], axis=1, inplace=True)
            else:
                df = df[df[column] != "—"]
                df = df[df[column] != "——"]
                df = df[df[column] != "———"]
        df[["AIRCRAFT", "REGISTRATION"]
           ] = df.AIRCRAFT_TYPE.str.split(expand=True)
        # df[["FROM","ORIGIN"]] = df.FROM.str.split(expand=True)
        # df[["TO","DESTINATION"]] = df.TO.str.split("\xa0",expand=True)
        df["REGISTRATION"] = df["REGISTRATION"].astype(
            str).apply(lambda x: x.strip("(").strip(")"))
        # df["ORIGIN"] = df["ORIGIN"].apply(lambda x:x.strip("(").strip(")"))
        # df["DESTINATION"] = df["DESTINATION"].apply(lambda x:x.strip("(").strip(")"))
        print(date.today().strftime('%d-%b-%y'))
        df["DATE"] = date.today().strftime('%d-%b-%y')

        df["STD_DT"] = pd.to_datetime(
            df.DATE.astype(str) + ' ' + df.STD.astype(str))
        df["ATD_DT"] = pd.to_datetime(
            df.DATE.astype(str) + ' ' + df.ATD.astype(str))
        df["STA_DT"] = pd.to_datetime(
            df.DATE.astype(str) + ' ' + df.STA.astype(str))
        # df['STA_DT']=df.apply(lambda x:x['STA_DT']+pd.Timedelta(days=1) if(int(str(x['STD'])[0:2]) > int(str(x['STA'])[0:2])) else x['STA_DT'],axis=1)
        # df['ATD_DT']=df.apply(lambda x:x['ATD_DT']+pd.Timedelta(days=1) if((int(str(x['STD'])[0:2]) - int(str(x['ATD'])[0:2]))>6) else x['ATD_DT'],axis=1)
        df['STD_MIN'] = df.apply(lambda x: int(
            round(int(x['STD_DT'].timestamp())))/60, axis=1)
        df['STA_MIN'] = df.apply(lambda x: int(
            round(int(x['STA_DT'].timestamp())))/60, axis=1)
        df['ATD_MIN'] = df.apply(lambda x: int(
            round(int(x['ATD_DT'].timestamp())))/60, axis=1)

        # print(df)

        ap = ap[ap['iata_code'].notna()]
        ap_iata = ap[['iata_code', 'latitude_deg', 'longitude_deg']]
        ap_iata = ap_iata.drop_duplicates()
        ap_iata.rename(columns={'iata_code': 'ORIGIN'}, inplace=True)
        Cordinated_data = pd.merge(df, ap_iata, on='ORIGIN', how='inner')
        ap_iata.rename(columns={'ORIGIN': 'DESTINATION'}, inplace=True)
        Cordinated_data.rename(
            columns={'latitude_deg': 'ORIGIN_LAT'}, inplace=True)
        Cordinated_data.rename(
            columns={'longitude_deg': 'ORIGIN_LON'}, inplace=True)
        Cordinated = pd.merge(Cordinated_data, ap_iata,
                              on='DESTINATION', how='inner')
        Cordinated.rename(columns={'latitude_deg': 'DEST_LAT'}, inplace=True)
        Cordinated.rename(columns={'longitude_deg': 'DEST_LON'}, inplace=True)
        Cordinated['Distance_km'] = Cordinated.apply(lambda x: hs.haversine(
            (x['ORIGIN_LAT'], x['ORIGIN_LON']), (x['DEST_LAT'], x['DEST_LON'])), axis=1)
        # print(Cordinated)

        if temp == 0 or temp == 1:
            df1 = Cordinated[["AIRCRAFT", "ORIGIN", "STD_MIN",
                              "STA_MIN", "ATD_MIN", "Distance_km"]].copy()
            finaldf = pd.merge(
                df1, dff, on=['AIRCRAFT', 'ORIGIN'], how='inner')
            finaldf.drop(['AIRCRAFT', 'ORIGIN', 'STD_MIN_y', 'STA_MIN_y',
                         'ATD_MIN_y', 'Distance_km_y', 'Unnamed: 0'], axis=1, inplace=True)
        elif temp == 2:
            df1 = Cordinated[["AIRCRAFT", "DESTINATION", "STD_MIN",
                              "STA_MIN", "ATD_MIN", "Distance_km"]].copy()
            finaldf = pd.merge(
                df1, dff, on=['AIRCRAFT', 'DESTINATION'], how='inner')
            finaldf.drop(['AIRCRAFT', 'DESTINATION', 'STD_MIN_y', 'STA_MIN_y',
                         'ATD_MIN_y', 'Distance_km_y', 'Unnamed: 0'], axis=1, inplace=True)

        print(finaldf.columns)
        X = finaldf.loc[[0]].values
        print(finaldf)
        print(X)
        # y=df1.iloc[:,[-1]].values
        # finaldf.to_csv("sad.csv")

        # loaded_model = pickle.load(open("bayesdxbarr_file",'rb'))
        y = loaded_model.predict(X)
        print(y[0])
        y = y.flatten()
        min = y[0]-df['STA_MIN']
        # print(datetime.fromtimestamp(int(y*60)))
        from datetime import datetime
        pta = datetime.fromtimestamp(y[0]*60)
        pta = df['STA_DT'][0]+pd.Timedelta(minutes=float(min))
        # print(min)
        print(pta)
        pta = str(pta)
        # pta[1] = r
        print(pta)
        # updating referenced database pta value
        pta_update = {
            'ETA': pta[0:19]
        }
        str_sno = str(sno-1)
        if temp == 0 or temp == 1:
            ref3.child(str_sno).update(pta_update)
            print(1111111111)
            print(temp)
            data = ref3.get()
        elif temp == 2:
            ref4.child(str_sno).update(pta_update)
            data = ref4.get()
            print(222222222222222)

        # ref2.update({'PTA':'%(pta)s'})
        # retreiving dxbarr data
        # data_redirect = ref3.get()

        # cursor.execute(ptaquery, { 'pta': pta,'sno': sno })

        # cursor.execute(select_stmt)
        # # query="select *from dubai_arrival where SNO = 1;"
        # # cursor.execute(query)
        # res = cursor.fetchall()

        # data = ref3.get()
        headers = data[0].keys()
        return render_template('index.html', headers=headers, res=data)
        # return render_template('index.html',headers=headers, params=params, res = data)
        # return render_template('index.html', params=params)

# @app.route("/redirect",methods=['GET','POST'])
# def redirect():
#     if request.method == 'POST':
#         df = pd.read_csv("dxb_arrival.csv")
#         if request.form.get('airport')=="1" and request.form.get('aircraft') == "1":
#             # f='hydairport_arrivals.csv'
#             # f='aircraftschedule.csv'
#             # xls_to_csv("Airport_Arrival_Departure_Data.xlsx",df)
#             # f=df
#             # data=[]
#             # print(f)
#             # with open(f,newline="") as file:
#             #     csvfile = csv.reader(file,delimiter="|")
#             #     for row in csvfile:
#             #         data.append(row)
#             # data = pd.DataFrame(data)
#             # df = pd.read_excel("dxbairport_arrival.xlsx")
#             df = pd.read_csv("dxb_arrival.csv")
#             # df.to_html('dxb_Arv.html')
#             df.to_html('D:\\Flask-Workspace\\templates\\dxb_Arv.html')
#         elif request.form.get('airport')=="1" and request.form.get('aircraft') == "0":
#             df = pd.read_csv("dxb_departure.csv")
#             df.to_html('D:\\Flask-Workspace\\templates\\dxb_Dep.html')
#         elif request.form.get('airport')=="0" and request.form.get('aircraft') == "1":
#             df = pd.read_csv("hyd_arrival.csv")
#             df.to_html('D:\\Flask-Workspace\\templates\\hyd_Arv.html')
#         elif request.form.get('airport')=="0" and request.form.get('aircraft') == "0":
#             df = pd.read_csv("hyd_departure.csv")
#             df.to_html('D:\\Flask-Workspace\\templates\\hyd_Dep.html')
#         else :
#             return render_template('index.html')
#             # return "Select the Options"
#             # flash("Please Select the options")
#             # return render_template('index.html')
#         df=df.drop(['FLIGHT_BAD'],axis=1)
#         return render_template('data.html',data=df.to_html())
#     else :
#         return render_template('index.html')

# @app.route("/csvfile",methods=['GET','POST'])
# def csvfile():
#     return render_template('csvfile1.html')

# @app.route("/data",methods=['GET','POST'])
# def data():
#     if request.method == 'POST' :
#         f = request.form['csvfile']
#         data = []
#         with open(f) as file:
#             csvfile = csv.reader(file)
#             for row in csvfile:
#                 data.append(row)
#         data = pd.DataFrame(data)
#         return render_template('data.html',data=data.to_html())
#     else :
#         return "Page Not Available!!"

# @app.route("/post/<string:post_slug>", methods=['GET'])
# def post_route(post_slug):
#     post = Posts.query.filter_by(slug=post_slug).first()
#     return render_template('post.html', params=params, post=post)


@app.route("/about")
def about():
    return render_template('about.html')
    # return render_template('about.html', params=params)


@app.route("/dashboard")
def dashboard():
    return render_template("login.html")
    # return render_template("login.html", params=params)

# @app.route("/contact", methods = ['GET', 'POST'])
# def contact():
#     if(request.method=='POST'):
#         name = request.form.get('name')
#         email = request.form.get('email')
#         phone = request.form.get('phone')
#         message = request.form.get('message')
#         entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
#         db.session.add(entry)
#         db.session.commit()
#     return render_template('contact.html', params=params)


# app.run(debug=True)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
