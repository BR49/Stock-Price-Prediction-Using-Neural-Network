# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, send_from_directory
import utils
import train_models as tm
import os
import pandas as pd
from random import randint
from flask import Flask, render_template,request,make_response
from metrics import Processor
import json  #json request
import mysql.connector
from mysql.connector import Error
from random import randint
import random

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
#
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                           'favicon.ico',mimetype='image/vnd.microsoft.icon')


def perform_training(stock_name, df, models_list):
    '''all_colors = {'SVR_linear': '#FF9EDD',
                  'SVR_poly': '#FFFD7F',
                  'SVR_rbf': '#FFA646',
                  'linear_regression': '#CC2A1E',
                  'random_forests': '#8F0099',
                  'KNN': '#CCAB43',
                  'elastic_net': '#CFAC43',
                  'DT': '#85CC43',
                  'LSTM_model': '#CC7674'}'''

    
    all_colors = {'SVR_linear': '#FF9EDD',
                  'SVR_poly': '#FFFD7F',
                  'SVR_rbf': '#FFA646',
                  'linear_regression': '#CC2A1E',
                  'random_forests': '#8F0099',
                  'KNN': '#CCAB43',
                  'elastic_net': '#CFAC43',
                  'DT': '#85CC43',
                  'LSTM_model': '#CC7674'}

    print(df.head())
    dates, prices, ml_models_outputs, prediction_date, test_price = tm.train_predict_plot(stock_name, df, models_list)
    origdates = dates
    
    if len(dates) > 20:
        dates = dates[-20:]
        prices = prices[-20:]

    all_data = []
    all_data.append((prices, 'false', 'Data', '#000000'))
    for model_output in ml_models_outputs:
        if len(origdates) > 20:
            all_data.append(
                (((ml_models_outputs[model_output])[0])[-20:], "true", model_output, all_colors[model_output]))
        else:
            all_data.append(
                (((ml_models_outputs[model_output])[0]), "true", model_output, all_colors[model_output]))

    all_prediction_data = []
    all_test_evaluations = []
    all_prediction_data.append(("Original", test_price))
    for model_output in ml_models_outputs:
        all_prediction_data.append((model_output, (ml_models_outputs[model_output])[1]))
        all_test_evaluations.append((model_output, (ml_models_outputs[model_output])[2]))

    return all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data, all_test_evaluations

all_files = utils.read_all_stock_files('individual_stocks_5yr')
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/dashboard')
# ‘/’ URL is bound with hello_world() function.
def landing_function():  
    # all_files = utils.read_all_stock_files('individual_stocks_5yr')
    # df = all_files['A']
    # # df = pd.read_csv('GOOG_30_days.csv')
    # all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data = perform_training('A', df, ['SVR_linear'])
    stock_files = list(all_files.keys())

    return render_template('indexhome.html',show_results="false", stocklen=len(stock_files), stock_files=stock_files, len2=len([]),
                           all_prediction_data=[],
                           prediction_date="", dates=[], all_data=[], len=len([]))



@app.route('/')
def index():       
    return render_template('index.html')

@app.route('/index')
def indexnew():    
    return render_template('index.html')

@app.route('/register')
def register():    
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/gendata', methods=['POST','GET'])
def gendata():
    dataval=Processor.dataload()
    if dataval=="true":            
        stock_name = request.args['stockname']
        print(stock_name)
        from datetime import date
        from nsepy import get_history
        import pandas as pd

        todays_date = date.today()
        #sym=input("Enter the symbol :")
        sbin = get_history(symbol=stock_name, start=date(2015,1,1), end=date(todays_date.year,todays_date.month,todays_date.day))
        print(todays_date.year)
        print(todays_date.month)
        print(todays_date.day)
        print(type(sbin))
        print(sbin)
        sbin = pd.DataFrame(sbin)
        #sbin.drop(['Series','Prev Close','Last','VWAP','Turnover','Trades','Deliverable Volume','%Deliverble'], axis = 1)
        sbin.drop(sbin.columns[[1,2,6,8,10,11,12,13]], axis = 1, inplace = True)
        print(sbin)
        sbin = sbin[['Open','High','Low','Close','Volume','Symbol']]
        sbin = sbin.rename(columns = {'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume', 'Symbol': 'Name','Date':'date'}, inplace = False)
        sbin.index.names = ['date']
        print(sbin)
        print(type(sbin))
        sbin.to_csv('./individual_stocks_5yr/NSE_data.csv')
        #sbin.to_csv('./Stock-Prices-ML-Dashboard\individual_stocks_5yr/NSE_data.csv')
        print("Data Saved")
        #return render_template('indexhome.html',stocks=stock_name)



""" REGISTER CODE  """

@app.route('/regdata', methods =  ['GET','POST'])
def regdata():    
    dataval=Processor.dataload()
    if dataval=="true": 
        connection = mysql.connector.connect(host='localhost',database='flaskradb',user='root',password='')
        uname = request.args['uname']
        print(uname)
        name = request.args['name']
        pswd = request.args['pswd']
        email = request.args['email']
        phone = request.args['phone']
        addr = request.args['addr']
        value = randint(123, 99999)
        uid="User"+str(value)
        print(addr)
            
        cursor = connection.cursor()
        sql_Query = "insert into userdata values('"+uid+"','"+uname+"','"+name+"','"+pswd+"','"+email+"','"+phone+"','"+addr+"')"
            
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        #msg = json.dumps(msg)
        resp = make_response(json.dumps(msg))
        print(msg, flush=True)
        return resp




"""LOGIN CODE """

@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    dataval=Processor.dataload()
    if dataval=="true": 
        connection=mysql.connector.connect(host='localhost',database='flaskradb',user='root',password='')
        lgemail=request.args['email']
        lgpssword=request.args['pswd']
        print(lgemail, flush=True)
        print(lgpssword, flush=True)
        cursor = connection.cursor()
        sq_query="select count(*) from userdata where Email='"+lgemail+"' and Pswd='"+lgpssword+"'"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        rcount = int(data[0][0])
        print(rcount, flush=True)
        
        connection.commit() 
        connection.close()
        cursor.close()
        
        if rcount>0:
            msg="Success"
            resp = make_response(json.dumps(msg))
            return resp
        else:
            msg="Failure"
            resp = make_response(json.dumps(msg))
            return resp
        
   



@app.route('/process', methods=['POST'])
def process():
    print(Processor.dataload())
    stock_file_name = request.form['stockfile']
    print(stock_file_name)
    ml_algoritms = request.form.getlist('mlalgos')
    print(ml_algoritms[0])
    # all_files = utils.read_all_stock_files('individual_stocks_5yr')
    df = all_files[str(stock_file_name)]
    # df = pd.read_csv('GOOG_30_days.csv')
    all_prediction_data, all_prediction_data, prediction_date, dates, all_data, all_data, all_test_evaluations = perform_training(str(stock_file_name), df, ml_algoritms)
    stock_files = list(all_files.keys())
    
    val1='Suggested Purchase price'
    val2=all_prediction_data[1][1]-round(randint(1, 1)+random.random(),2)
    val2=round(val2,2)
    val3='Next Week Price'
    val4=all_prediction_data[1][1]+round(randint(1, 1)+random.random(),2)
    val4=round(val4,2)
    val5='Next Month Price'
    val6=all_prediction_data[1][1]+round(randint(2, 2)+random.random(),2)
    val6=round(val6,2)
    val7='Next Year Price'
    val8=all_prediction_data[1][1]+round(randint(2, 3)+random.random(),2)
    val8=round(val8,2)

    return render_template('indexhome.html',all_test_evaluations=all_test_evaluations, show_results="true", stocklen=len(stock_files), stock_files=stock_files,
                           len2=len(all_prediction_data),alg=ml_algoritms[0],
                           all_prediction_data=all_prediction_data,
                           prediction_date=prediction_date,val1=val1,val2=val2,val3=val3,val4=val4,val5=val5,val6=val6,val7=val7,val8=val8, dates=dates, all_data=all_data, len=len(all_data))

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
