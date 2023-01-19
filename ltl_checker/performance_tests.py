import unittest
import pandas as pd
import os
import pm4py
import sympy as sp
import main as m
import sympy.abc
from sympy.abc import _clash1
from sympy.core.sympify import sympify
from datetime import datetime
import matplotlib.pyplot as plt
cwd = os.getcwd()

def renameColumns(columns_to_drop, columns_to_rename):
    # we define mandatory_columns as the columns the user cannot drop and therefore
    #ignore all selections of such columns
    global mandatory_columns
    mandatory_columns = ["case:concept:name", "concept:name", "time:timestamp" , "org:resource"]
    #rename the dataframe by handing the rename function a dictionary
    m.data.rename(columns=columns_to_rename, inplace = True)

    for column in columns_to_drop:
        if(column in mandatory_columns): 
            pass
        else:
            m.data.drop(column, axis=1, inplace = True)
    #data = data.drop_duplicates(list(data.columns))
    return m.data



class durationTest(unittest.TestCase):
    
    def test_detail_incident_activity(self):
        m.renameColumns = renameColumns
        number_of_rows = []
        timedelta_ms = []

        file_path = os.path.join(cwd, 'test_input', 'detail_incident_activity.csv') 
        temp = pd.read_csv(file_path)
        print(temp.head(4))
        
        columns_to_rename = {"Incident ID":"case:concept:name", "DateStamp":"time:timestamp",
                    "IncidentActivity_Type":"concept:name", "Assignment Group":"org:resource"}
        columns_to_drop = []#["Interaction ID", "KM number","IncidentActivity_Number"]
        
        for x in range(1,42,5):
            m.data = pd.concat([temp for i in range(x)])
            number_of_rows.append(len(m.data.index))
            m.renameColumns(columns_to_drop, columns_to_rename)
            expression = "((A | F) | E & (A | E) & (F | E)) & (A & E | F & (E | A))"
            m.expression = sympify(expression,_clash1)
            m.terms_dict = { "A" : ("four_eyes_principle", ["Open", "Closed"]),
            "F" : ("eventually_follows_2", ["Open","Update"]),
            "E" : ("attribute_value_different_persons",["Update"])}
            
            start=datetime.now()
            m.calc_result()
            end=datetime.now()
            

            duration=(end-start).total_seconds() * 1000
            print(x, len(m.data.index),duration)
            timedelta_ms.append(duration)
        
        data = {'Number of rows' : number_of_rows, 'Duration [ms]':timedelta_ms}
        df = pd.DataFrame(data=data)
        df.plot(x='Number of rows', y='Duration [ms]',)
        plt.savefig('test-detail_incident_activity.png')
        df.to_csv('test-detail_incident_activity.csv')



    def test_BPIC15_5(self):
        m.renameColumns = renameColumns
        number_of_rows = []
        timedelta_ms = []

        file_path = os.path.join(cwd, 'test_input', 'BPIC15_5.xes') 
        raw_log = pm4py.read_xes(file_path)
        temp = pm4py.convert_to_dataframe(raw_log)
        print(temp.head(4))

        for x in range(1,287,5):
            m.data = pd.concat([temp for i in range(x)])
            number_of_rows.append(len(m.data.index))
            expression = "((A | F) | E & (A | E) & (F | E)) & (A & E | F & (E | A))"
            m.expression = sympify(expression,_clash1)
            m.terms_dict = { "A" : ("four_eyes_principle", ["Open", "Closed"]),
            "F" : ("eventually_follows_2", ["Open","Update"]),
            "E" : ("attribute_value_different_persons",["Update"])}
            
            start=datetime.now()
            m.calc_result()
            end=datetime.now()
            

            duration=(end-start).total_seconds() * 1000
            print(x, len(m.data.index),duration)
            timedelta_ms.append(duration)
        
        data = {'Number of rows' : number_of_rows, 'Duration [ms]':timedelta_ms}
        df = pd.DataFrame(data=data)
        df.plot(x='Number of rows', y='Duration [ms]',)
        plt.savefig('test-BPIC15_5.png')
        df.to_csv('test-BPIC15_5.csv')


    def test_BPI_Challenge_2017(self):
        m.renameColumns = renameColumns
        number_of_rows = []
        timedelta_ms = []

        file_path = os.path.join(cwd, 'test_input', 'BPI Challenge 2017.xes') 
        raw_log = pm4py.read_xes(file_path)
        temp = pm4py.convert_to_dataframe(raw_log)
        print(temp.head(4))

        for x in range(1,17,5):
            m.data = pd.concat([temp for i in range(x)])
            number_of_rows.append(len(m.data.index))
            expression = "((A | F) | E & (A | E) & (F | E)) & (A & E | F & (E | A))"
            m.expression = sympify(expression,_clash1)
            m.terms_dict = { "A" : ("four_eyes_principle", ["Open", "Closed"]),
            "F" : ("eventually_follows_2", ["Open","Update"]),
            "E" : ("attribute_value_different_persons",["Update"])}
            
            start=datetime.now()
            m.calc_result()
            end=datetime.now()
            

            duration=(end-start).total_seconds() * 1000
            print(x, len(m.data.index),duration)
            timedelta_ms.append(duration)
        
        data = {'Number of rows' : number_of_rows, 'Duration [ms]':timedelta_ms}
        df = pd.DataFrame(data=data)
        df.plot(x='Number of rows', y='Duration [ms]',)
        plt.savefig('test-BPI_Challenge_2017.png')
        df.to_csv('test-BPI_Challenge_2017.csv')


if __name__ == '__main__':
    unittest.main()