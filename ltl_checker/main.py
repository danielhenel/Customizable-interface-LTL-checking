import os
import pandas as pd
import pm4py
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, Response, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import sympy as sp
import sympy.abc
from sympy.abc import _clash1
from sympy.core.sympify import sympify
from sympy import *
import pm4py.algo.filtering.pandas.ltl as ltl
import pdfkit

data = None
file = None
expression = None
terms_dict = None
result = None
caseIDs = None


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
    global result
    global caseIDs
    page = request.args.get("page")
    try:
        page = int(page)
        if page > 0 and page <= len(caseIDs):
            df = result.loc[result['Case ID'] == caseIDs[page-1]].reset_index().drop(columns=["index"])
            return render_template('results.html',data=json.dumps([df.to_json(),len(caseIDs),page,prepare_deviations_description(df)]))
    except:
        pass


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


@app.route("/getCSV")
def getCSV():
    return Response(
        result.head(500).to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=fitering-result.csv"})
    


@app.route("/getHTML")
def getHTML():
    return Response(
        result.head(500).to_html(),
        mimetype="text/html",
        headers={"Content-disposition":
                 "attachment; filename=fitering-result.html"})


@app.route("/getXES")
def getXES():
    log = pm4py.convert_to_event_log(result.head(500).rename(columns={"Case ID" : "case:concept:name","Activity Name":"concept:name", 
     "Time Stamp" : "time:timestamp" , "Resource" : "org:resource"}))
    pm4py.write_xes(log, 'fitering-result.xes')
    return send_file('fitering-result.xes', as_attachment=True)


@app.route("/getXLSX")
def getXLSX():
    with pd.ExcelWriter("fitering-result.xlsx") as writer:
        result.head(500).to_excel(writer, sheet_name="Filtered")
    return send_file('fitering-result.xlsx', as_attachment=True)


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
    global caseIDs

    result = None
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
    caseIDs = list(result['Case ID'].unique())
    caseIDs.sort()

def df_intersection(A, B):
    cols = list(A.columns)
    return pd.merge(A, B, how='inner', on=cols).reset_index().drop(columns=["index"])

def df_union(A,B):
    cols = list(A.columns)
    return pd.concat([A,B]).drop_duplicates(cols).reset_index().drop(columns=["index"])

def four_eyes_principle(df,activities):
    filtered_log = ltl.ltl_checker.four_eyes_principle(df,*activities).reset_index().drop(columns=["index"])
    return filtered_log

def get_rows_of_deviation_four_eyes_principle(df,activity1, activity2):
    filtered_log = ltl.ltl_checker.four_eyes_principle(df.rename(columns={"Case ID" : "case:concept:name","Activity Name":"concept:name", 
     "Time Stamp" : "time:timestamp" , "Resource" : "org:resource"}),activity1, activity2).reset_index().drop(columns=["index"])
    if filtered_log.empty:
        return (None,None)
    else:
        activities = list(filtered_log["concept:name"])
        resources = list(filtered_log["org:resource"])
        resource1 = None
        resource2 = None
        for i in range(len(activities)):
            if resource1 is None and activities[i] == activity1:
                resource1 = i
            elif resource1 is not None and resource2 is None and activities[i] == activity2 and resources[i] != resources[resource1]:
                resource2 = i
        return ([resource1,resource2], [resources[resource1], resources[resource2]])


def eventually_follows(df,activities): 
    filtered_log = ltl.ltl_checker.eventually_follows(df,activities).reset_index().drop(columns=["index"])
    return filtered_log


def get_rows_of_deviation_eventually_follows(df, params):
    activity1 = activity2 = activity3 = activity4 = None
    filtered_log = ltl.ltl_checker.eventually_follows(df.rename(columns={"Case ID" : "case:concept:name","Activity Name":"concept:name", 
     "Time Stamp" : "time:timestamp" , "Resource" : "org:resource"}),params).reset_index().drop(columns=["index"])
    if filtered_log.empty:
        return (None,None)
    else:
        result = []
        activities = list(filtered_log["concept:name"])
        for i in range(len(activities)):
            if len(params)>=1 and activity1 is None and activities[i] == params[0]:
                activity1 = i
                result.append(activity1)
            elif len(params)>=2 and activity2 is None and activity1 is not None and activities[i] == params[1]:
                activity2 = i
                result.append(activity2)
            elif len(params)>=3 and activity3 is None and activity1 is not None and activity2 is not None and activities[i] == params[2]:
                activity3 = i
                result.append(activity3)
            elif len(params)>=4 and activity4 is None and activity1 is not None and activity2 is not None and activity3 is not None and activities[i] == params[3]:
                activity4 = i
                result.append(activity4)
        return ([result],[activities[r] for r in result])


def attribute_value_different_persons(df,activities):
    filtered_log = ltl.ltl_checker.attr_value_different_persons(df, *activities).reset_index().drop(columns=["index"])
    return filtered_log


def get_rows_of_deviation_attribute_value_different_persons(df,activity):
    filtered_log = ltl.ltl_checker.attr_value_different_persons(df.rename(columns={"Case ID" : "case:concept:name","Activity Name":"concept:name", 
     "Time Stamp" : "time:timestamp" , "Resource" : "org:resource"}), activity).reset_index().drop(columns=["index"])
    if filtered_log.empty:
        return (None,None)
    else:
        activities = list(filtered_log["concept:name"])
        resources = list(filtered_log["org:resource"])
        resource1 = resource2 = None
        for i in range(len(activities)):
            if resource1 is None and activities[i] == activity:
                resource1 = i
            elif resource1 is not None and resource2 is None and activities[i] == activity and resources[resource1] != resources[i]:
                resource2 = i
        return ([resource1, resource2],[resources[resource1],resources[resource2]])


def prepare_deviations_description(df):
    global terms_dict
    
    messages = []
    highlight_rows = set()
    for term, filter in terms_dict.items():
        filterType = filter[0]
        activities = filter[1]

        if filterType == 'four_eyes_principle':
            rows, resources = get_rows_of_deviation_four_eyes_principle(df,activities[0],activities[1])
            if rows is not None:
                highlight_rows.update(rows)
                messages.append(["Four eyes principle: The activities {0} and {1} have been performed by the different resources {2} and {3} (rows {4} and {5})".format(activities[0],activities[1],resources[0],resources[1],rows[0],rows[1]),rows])

        elif filterType in['eventually_follows_2', 'eventually_follows_3','eventually_follows_4']:
            rows, activities = get_rows_of_deviation_eventually_follows(df,activities)
            if rows is not None:
                highlight_rows.update(rows)
                messages.append(["Eventually follows: The sequence of the activities {0} occurs in rows {1}".format(activities,rows),rows])

        elif filterType == 'attribute_value_different_persons':
            rows, resources = get_rows_of_deviation_attribute_value_different_persons(df,activities[0])
            if rows is not None:
                highlight_rows.update(rows)
                messages.append(["Attribute value different persons: The activity {0} has been performed by the different resources {1} and {2} (rows {3} and {4})".format(activities[0],resources[0],resources[1],rows[0],rows[1]),rows])

        highlight_rows = list(highlight_rows)
        highlight_rows.sort()
    return [messages, highlight_rows]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

    