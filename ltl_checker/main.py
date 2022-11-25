import os
import pandas as pd
import pm4py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime

data = None
file = None

app = Flask(__name__)

@app.route('/')
def start():
   return render_template('upload.html') 

@app.route('/selectColumns',methods = ['POST','GET'])
def upload():
    global data
    global file
    file = request.files['file']
    data = convertInput()
    return render_template('columns-selection.html',data=data.head(5).to_json())

@app.route('/preview',methods = ['GET'])
def preview():
    return render_template('columns-selection.html',data=data)

def convertInput():
    global file
    if file.filename.endswith('.csv'): 
        raw_log = pd.read_csv(file)
        return raw_log
    elif file.filename.endswith('.xes'): 
        pass #TODO: 
        raw_log = pm4py.read_xes(file)
        print(raw_log.head())
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)