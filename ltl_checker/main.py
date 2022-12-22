import os
import pandas as pd
import pm4py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import sympy as sp
import sympy.abc
from sympy.abc import _clash1
from sympy.core.sympify import sympify
from sympy import *
import pm4py.algo.filtering.pandas.ltl as ltl

data = None
file = None
expression = None
terms_dict = None
result = None

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

@app.route('/selectColumns/message', methods = ['POST'])
def afterColumnsSelection():
    global data
    message = json.loads(request.data)
    drop_cols = message[0]
    new_names = message[1]
    renameColumns(drop_cols,new_names)
    return "success"

@app.route('/selectFilters')
def loadSelectFiltersPage():
    return render_template('filters-selection.html',data=getActivities())

@app.route('/selectFilters/message', methods = ['POST'])
def afterFilterSelection():
    global expression
    global terms_dict
    global result
    message = json.loads(request.data)
    terms_dict = message[0]
    expression = message[1]
    expression = sympify(expression,_clash1)
    calc_result()
    return 

@app.route('/selectColumns2',methods = ['POST','GET'])
def goBackToSelectColumns(): 
    return render_template('columns-selection.html',data=data.head(5).to_json())

@app.route('/results',methods = ['POST','GET'])
def results(): 
    return render_template('results.html',data=json.dumps([result.head(6).to_json(),len(result.index)]))

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
        raw_log = pd.read_csv(file, sep = None, engine = 'python')
        return raw_log
    elif file.filename.endswith('.xes'): 
        temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'uploads','raw_log.xes') #temporarily save file for conversion
        file.save(temp_path)
        raw_log = pm4py.read_xes(temp_path)
        raw_log = pm4py.convert_to_dataframe(raw_log)
        os.remove(temp_path) # delete file after conversion
        return raw_log
    else: 
       raise Exception('File Wrong format or empty')

def renameColumns(columns_to_drop, columns_to_rename):
    # we define mandatory_columns as the columns the user cannot drop and therefore
    #ignore all selections of such columns
    global mandatory_columns
    global data
    mandatory_columns = ["case:concept:name", "concept:name", "time:timestamp" , "org:resource"]
    #rename the dataframe by handing the rename function a dictionary
    data.rename(columns=columns_to_rename, inplace = True)

    for column in columns_to_drop:
        if(column in mandatory_columns): 
            pass
        else:
            data.drop(column, axis=1, inplace = True)
    data = data.drop_duplicates(list(data.columns))
    return data

def get_args(cnf_expr):
    cnf_str = str(cnf_expr)
    if cnf_str.find("(") == -1:
        if cnf_str.find("&") != -1:
            return (cnf_expr.args,"&")
        elif cnf_str.find("|") != -1:
            return (tuple([cnf_expr]),"|")
        else:
            return ([cnf_expr],None)
    else:
        return (cnf_expr.args,None)

def simplifyExpression(expr) -> list: #this function returns a list of all the conjunctively connected clauses in the filter expression
    #convert expression to CNF
    cnf = sp.to_cnf(expr, True)

    # seperate different Clauses in CNF
    clauses, operator = get_args(cnf)
    clause_list = tupleToList(clauses)
    #convert clauses in list to list of literals
    for i in range(0,len(clause_list)):
        if(len(clause_list[i].args) != 0):
            clause_list[i] = tupleToList(clause_list[i].args)
        else:
            if operator == "&":
                clause_list[i] = [clause_list[i]]
            elif operator == "|":
                clause_list[i] = tupleToList(clause_list[i].args)
            else:
                clause_list[i] = [clause_list[i]]
    return clause_list


def tupleToList(tuple) -> list: 
    retList = []
    for element in tuple:
        retList.append(element)
    return retList

def getActivities(): 
    global data
    return (data['concept:name'].unique()).tolist()

def calc_result():
    global data
    global terms_dict
    global expression
    global result

    for terms in simplifyExpression(expression):
        temp = None
        for term in terms:
            key = str(term)
            filterType = terms_dict[key][0]
            if temp is None:
                if filterType == 'four_eyes_principle': 
                    temp = four_eyes_principle(data,terms_dict[key][1])
                elif filterType in['eventually_follows_2', 'eventually_follows_3','eventually_follows_4']:
                    temp = eventually_follows(data,terms_dict[key][1])
                elif filterType == 'attribute_value_different_persons':
                    temp = attribute_value_different_persons(data,terms_dict[key][1])
            else:
                if filterType == 'four_eyes_principle': 
                    temp = df_union(temp,four_eyes_principle(data,terms_dict[key][1]))
                elif filterType in['eventually_follows_2', 'eventually_follows_3','eventually_follows_4']:
                    temp = df_union(temp,eventually_follows(data,terms_dict[key][1]))
                elif filterType == 'attribute_value_different_persons':
                    temp = df_union(temp,attribute_value_different_persons(data,terms_dict[key][1]))        
        if result is None:
            result = temp
        else:
            result = df_intersection(temp, result)

    result.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)   

def df_intersection(A, B):
    cols = list(A.columns)
    return pd.merge(A, B, how='inner', on=cols).reset_index().drop(columns=["index"])

def df_union(A,B):
    cols = list(A.columns)
    return pd.concat([A,B]).drop_duplicates(cols).reset_index().drop(columns=["index"])

def four_eyes_principle(df,activities):
    filtered_log = ltl.ltl_checker.four_eyes_principle(df,*activities).reset_index().drop(columns=["index"])
    if len(activities)!=2:
        raise ValueError("The filter requires exactly two parameters")
    return filtered_log

def eventually_follows(df,activities): 
    filtered_log = ltl.ltl_checker.eventually_follows(df,activities).reset_index().drop(columns=["index"])
    if len(activities)<2:
        raise ValueError("The filter requires at least two parameters")
    return filtered_log

def attribute_value_different_persons(df,activities):
    filtered_log = ltl.ltl_checker.attr_value_different_persons(df, *activities).reset_index().drop(columns=["index"])
    if len(activities)!=1:
        raise ValueError("The filter requires exactly one parameter")
    return filtered_log

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    