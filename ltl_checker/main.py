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

@app.route('/aboutUs')
def aboutUs():
   return render_template('about-us.html') 

@app.route('/errorPage')
def errorPage(): 
    return render_template('error.html')

@app.route('/selectColumns',methods = ['POST','GET'])

def upload():
    try: 
        global data
        global file
        file = request.files['file']
        data = convertInput()
        return render_template('columns-selection.html',data=data.head(5).to_json())
    except pd.errors.EmptyDataError: 
        return render_template('error.html', message = 'Your data is empty!!!')




def convertInput():
    global file
    #check for file ending and then convert the uploaded log into data frame
    if file.filename.endswith('.csv'): 
        raw_log = pd.read_csv(file)
        return raw_log
    elif file.filename.endswith('.xes'): 
        pass #TODO: 
        temp_path = os.path.join(os.getcwd(),'ltl_checker','uploads','raw_log.xes') #temporarily save file for conversion
        file.save(temp_path)
        raw_log = pm4py.read_xes(temp_path)
        raw_log = pm4py.convert_to_dataframe(raw_log)
        os.remove(temp_path) # delete file after conversion
        return raw_log


def renameColumns(columns_to_drop, columns_to_rename, data):
    # we define mandatory_columns as the columns the user cannot drop and therefore
    #ignore all selections of such columns
    global mandatory_columns 
    mandatory_columns = ["case:concept:name", "concept:name", "time:timestamp" , "org:resource"]
    #rename the dataframe by handing the rename function a dictionary
    data.rename(columns=columns_to_rename, inplace = True)

    for column in columns_to_drop:
        if(column in mandatory_columns): 
            pass
        else:
            data.drop(column, axis=1, inplace = True)
    return data


def simplifyExpression(expr) -> list: #this function returns a list of all the conjunctively connected clauses in the filter expression
    #convert expression to CNF
    cnf = sp.to_cnf(expr)
    # seperate different Clauses in CNF
    clauses = cnf.args
    clause_list = tupleToList(clauses)
    #convert clauses in list to list of literals
    for i in range(0,len(clause_list)-1):
        clause_list[i] = tupleToList(clause_list[i].args)
    return clause_list

def tupleToList(tuple) -> list: 
    retList = []
    for element in tuple:
        retList.append(element)
    return retList


def evaluateCNFFilter(cnf_list):
    for clause in cnf_list:
        bool = False
        for literal in clause:
            



def getActivities(dataframe): 
    return dataframe['concept:name'].unique()

    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    