import os
import pandas as pd
import pm4py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import sympy as sp
from sympy import *
import lxml
import pm4py.algo.filtering.pandas.ltl as ltl

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
        return render_template('error.html', message = 'Your <CSV data is empty!!!')
    except lxml.etree.XMLSyntaxError:
        return render_template('error.html', message = 'Your XES data is empty!!!')




def convertInput():
    global file
    #check for file ending and then convert the uploaded log into data frame
    if file.filename.endswith('.csv'):
        raw_log = pd.read_csv(file, sep = None, engine = 'python')
        return raw_log
    elif file.filename.endswith('.xes'): 
        pass #TODO: 
        temp_path = os.path.join(os.getcwd(),'ltl_checker','uploads','raw_log.xes') #temporarily save file for conversion
        file.save(temp_path)
        raw_log = pm4py.read_xes(temp_path)
        raw_log = pm4py.convert_to_dataframe(raw_log)
        os.remove(temp_path) # delete file after conversion
        return raw_log
    else: 
       raise Exception('File Wrong format or empty')


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


def calc_result(list_of_terms, dictionary, raw_log) -> pd.DataFrame:
    #define log which is to be returned
    ret_log = raw_log.copy()
    temp = [] 
    for key in dictionary:
        #generate the symbols for sympy 
        globals()[key] = symbols('{0}'.format(key))
    # for each literal in the clause a filtered log will be generated  
    # and then saved into temp.
    for key2 in dictionary:   
        filterType = dictionary[key2]
        if filterType == 'four_eyes_principle': 
            ret_log = four_eyes_principle(ret_log,dictionary[key2])
        elif filterType == 'eventually_follows_2': 
            ret_log = eventually_follows_2(ret_log,dictionary[key2])
        elif filterType == 'eventually_follows_3': 
            ret_log = eventually_follows_3(ret_log,dictionary[key2])
        elif filterType == 'eventually_follows_4':
            ret_log = eventually_follows_4(ret_log,dictionary[key2])
        temp.append(ret_log)
    #combine all the generated filtered_logs from temp
    ret_log = pd.concat(temp)
    #delete all duplicate rows
    ret_log.drop_duplicates(keep=False)
    return ret_log
        

    

def four_eyes_principle(activites,df):
    filtered_log = ltl.ltl_checker.four_eyes_principle(df,*activites)
    return filtered_log

def eventually_follows_2(activities,df): 
    filtered_log = ltl.ltl_checker.A_eventually_B(df,*activities)
    return filtered_log

def eventually_follows_3(activities,df):
    filtered_log = ltl.ltl_checker.A_eventually_B_eventually_C(df,*activities)
    return filtered_log

def eventually_follows_4(activities,df):
    filtered_log = ltl.ltl_checker.A_eventually_B_eventually_C_eventually_D(df,*activities)
    return filtered_log





if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)