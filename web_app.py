import pandas as pd
#import matplotlib.pyplot as plt
#import psycopg2 #### conda install psycopg2
#from datetime import datetime, timedelta
#import os
from flask import Flask, abort, jsonify, request, send_file
from flask import url_for, render_template
from jinja2 import Template
import time, datetime
#from rate_engine import get_input, get_prediction
# from v3_calculator_gamma_demo import get_result, ordertable

MWautos = pd.read_csv("./Montway2018.csv")[['autoyear', 'automake', 'automodel']].copy()
MWautos['autoyear'] = MWautos['autoyear'].apply(lambda x: int(x.replace(',','')))
makes = sorted(list(MWautos['automake'].unique()))

# makes.sort()# MWautos.info()
# ford_models = list(MWautos[MWautos['automake'] == 'Ford']['automodel'].unique())
# ford_models.sort()
# ford_models

#http://flask.pocoo.org
app = Flask(__name__)

this_year = datetime.date.today().year

@app.route("/", methods = ['GET', 'POST'])
def main_page():
    # dfcars, df_raw = ordertable()#get_input()
    dict_raw = {'op': 'Y', 'ship': 'O'}
    #convert dfcars to dictionary
    # dict_raw = {k:v[0] for k, v in df_raw.to_dict().items()}
    years = range(1990, this_year+1)
    return render_template('input.html',
                            dict_cars=dict_raw,
                            makes=makes,
                            years=years)

@app.route("/price", methods = ['POST'])
def result():
    fpd = request.form.get("fpd")
    from_zip = int(str(request.form.get("from_zip")))
    to_zip = int(str(request.form.get("to_zip")))
    n_cars = int(str(request.form.get("nCars")))

    rows = []
    for i in range(1, n_cars+1):
        make_str = "make" + str(i)
        model_str = "model" + str(i)
        year_str = "year" + str(i)
        make = str(request.form.get(make_str))
        model = str(request.form.get(model_str))
        year = int(str(request.form.get(year_str)))
        price = 800.0
        rows.append([i, make, model, year, price])
    # print(rows)

    # df_order, df_raw = ordertable(date_str=fpd, fromzip=from_zip, tozip=to_zip)
    # price, price_ad, price_up, df_show, adjusted_ratio, adjusted_upsell_ratio = get_result(fpd, from_zip, to_zip)
    total_price = sum([row[4] for row in rows])
    discount = 100 #% price_ad
    price_dis = total_price - discount #% price_up


    # dict_raw = {k:v[0] for k, v in df_raw.to_dict().items()}
    return render_template('output.html',
                            # dict_cars=dict_raw,
                            fpd=fpd,
                            from_zip=from_zip,
                            to_zip=to_zip,
                            n_cars=n_cars,
                            rows=rows,
                            total_price=total_price,
                            discount=discount,
			                price_dis=price_dis,
                            )

@app.route('/get_models/<make>')
def get_models(make):
    # https://stackoverflow.com/questions/44646925/flask-dynamic-dependent-dropdown-list
    # https://stackoverflow.com/questions/42886965/flask-dropdown-values-based-on-prior-selection
    makes = list(MWautos['automake'].unique())
    if make not in makes:
        return jsonify([])
    else:
        models = sorted(list(MWautos[MWautos['automake'] == make]['automodel'].unique()))
        return jsonify(models)

if __name__ == "__main__":
    #https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use
    app.run(host="0.0.0.0")
