import pandas as pd
import csv
from flask import Flask

app = Flask(__name__)
df = pd.read_csv("dp_hyd_arrival_database().csv")
df.unique()
print(df)
app.run(debug=True)