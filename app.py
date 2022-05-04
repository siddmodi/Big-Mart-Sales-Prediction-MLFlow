from flask import Flask, render_template, request, redirect, url_for
from flask_cors import cross_origin
import joblib
import numpy as np
import pandas as pd
import os
import joblib
import sklearn

pipeline = joblib.load(open('pipeline.joblib','rb'))

app = Flask(__name__)

@app.route('/')
@cross_origin()
def home():
  return render_template('home.html')

@app.route('/predict', methods=['POST','GET'])
@cross_origin()
def predict():

  Item_Weight = float(request.form["Item_Weight"])
  Item_Fat_Content = request.form["Item_Fat_Content"]
  Item_Visibility = float(request.form["Item_Visibility"])
  Item_Type	= request.form["Item_Type"]
  Item_MRP = float(request.form["Item_MRP"])
  Outlet_Size = request.form["Outlet_Size"]
  Outlet_Location_Type = request.form["Outlet_Location_Type"]
  Outlet_Type = request.form["Outlet_Type"]

  inp={
    'Item_Weight':[Item_Weight] ,
    'Item_Fat_Content':[Item_Fat_Content] ,
    'Item_Visibility':[Item_Visibility] ,
    'Item_Type':[Item_Type] ,
    'Item_MRP':[Item_MRP] ,
    'Outlet_Size':[Outlet_Size] ,
    'Outlet_Location_Type':[Outlet_Location_Type],
    'Outlet_Type':[Outlet_Type] 
    }

  df=pd.DataFrame(inp)

  prediction = np.round_(pipeline.predict(df), decimals = -2)

  return render_template('home.html',prediction_text=f"Sales is ₹{prediction[0]}")

if __name__ == "__main__":
    app.run()
