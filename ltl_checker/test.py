import unittest
import pandas as pd
import os
from main import upload, convertInput, renameColumns, getActivities, calc_result, simplifyExpression
from main import file
import pm4py

cwd = os.getcwd()

mandatory_columns = ["case:concept:name", "concept:name", "time:timestamp" , "org:resource"]

columns_to_rename = {"Incident ID":"case:concept:name", "DateStamp":"time:timestamp",
                    "IncidentActivity_Type":"concept:name", "Interaction ID":"org:resource"}
columns_to_drop = ["Assignment Group", "KM number"]


#class calcResultTest(unittest.TestCase): 
 #   cnf = '((F1 | F2 | F3) & (F2 | F4)  &  (F1) & (F5) & (F6))'
 #   list_of_lists_of_terms = simplifyExpression(cnf)

 #   file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
 #   df = pd.read_csv(file_path)

 #   dictionary = {
 #       'F1': ('four_eyes_principle',  [r1,r2]),
 #       'F2': ('four_eyes_principle',  [r1,r2]),
 #       'F3':('eventually_follows_3',  [a,b,c]),
 #       'F4':('eventually_follows_2',  [b,c]),
 #       'F5':('attribute_value_different_persons',  [a]),
 #       'F6':('attribute_value_different_persons',  [b])
 #   }

 #   calc_result(list_of_lists_of_terms, dictionary, df)



class RenameColumns(unittest.TestCase):
    
    def testRenameColumns(self):
        file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
        df = pd.read_csv(file_path)
        
        renameColumns(columns_to_drop, columns_to_rename, df)
        cols = list(df.columns)
        for column in mandatory_columns:
            self.assertIn(column, cols, msg=None)
        for column in columns_to_drop:
            self.assertNotIn(columns_to_drop, cols, msg=None)


def isNotDuplicate(dataframe, activitiesList): 
    temp = list(set(dataframe['concept:name']))
    if len(temp) == len(activitiesList): 
        return True
    else: 
        return False


class getActivitiesTestCase(unittest.TestCase):
    def testGetActivities(self):
        file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
        df = pd.read_csv(file_path)
        renameColumns(columns_to_drop, columns_to_rename, df)
        self.assertTrue(isNotDuplicate(df, getActivities(df)))



class UploadtestCase(unittest.TestCase): 

    def testInputFormat(self): 
            file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'wrongInput.pdf')
            file = 'wrongInput.pdf'
            if file.endswith('.csv'): 
                raw_log = pd.read_csv(file)
                ret = raw_log
            elif file.endswith('.xes'): 
                pass #TODO: 
                raw_log = pm4py.read_xes(file)
                raw_log = pm4py.convert_to_dataframe(raw_log)
                ret = raw_log
            else: 
                ret = 'wrong file format'

            bool = (ret == 'wrong file format')

            self.assertTrue(bool, 'Wrong file format not recognized')






            

if __name__ == '__main__':
    unittest.main()
