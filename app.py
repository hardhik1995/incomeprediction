from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
#from flask.ext.bootstrap import Bootstrap
#from flask_material import Material
#from sklearn.externals import joblib
#import traceback
#import pandas as pd
import numpy as np
import sys
import os
import pickle

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        age           =request.form['age']
        w_class       =request.form['w_class']
        education     =request.form['edu']
        martial_status=request.form['martial_stat']
        occupation    =request.form['occup']
        relation      =request.form['relation']
        race          =request.form['race']
        gender        =request.form['gender']
        capital_gain  =request.form['c_gain']
        capital_loss  =request.form['c_loss']
        hours_per_week=request.form['hours_per_week']
        native_country=request.form['native-country']

        model_choice  =request.form['model_choice']

        sample_data=[age, w_class, education, martial_status, occupation, relation, race, gender, capital_gain,
                     capital_loss, hours_per_week, native_country]

        clean_data = list(map(int, sample_data))
        to_predict_data = np.array(clean_data).reshape(1,12)

        if model_choice == 'logistic_model':
            with open('model/model_lr.pkl', 'rb') as f:
                logit_model = pickle. load(f)
            prediction=logit_model.predict(to_predict_data)

            if int(prediction) == 1:
                result_prediction = 'Income more than 50K'
            else:
                result_prediction = 'Income less that 50K'

        elif model_choice=='RandomForest_model':
            with open('model/model_rf.pkl', 'rb') as f:
                rf_model = pickle. load(f)
            prediction=rf_model.predict(to_predict_data)

            if int(prediction) == 1:
                result_prediction = 'Income more than 50K'
            else:
                result_prediction = 'Income less that 50K'

        elif model_choice == 'DecisionTree_model':
            with open('model/model_dt.pkl', 'rb') as f:
                dt_model = pickle. load(f)
            prediction=dt_model.predict(to_predict_data)

            if int(prediction) == 1:
                result_prediction = 'Income more than 50K'
            else:
                result_prediction = 'Income less that 50K'

    return render_template('result.html',
                           age=age,
                           w_class=w_class,
                           education=education,
                           martial_status=martial_status,
                           relation=relation,
                           race=race,
                           gender=gender,
                           capital_gain=capital_gain,
                           capital_loss=capital_loss,
                           hours_per_week=hours_per_week,
                           native_country=native_country,
                           model_selected=model_choice,
                           prediction=prediction,
                           result_prediction=result_prediction)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
