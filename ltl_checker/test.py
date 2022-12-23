import unittest
import pandas as pd
import os
from main import upload, convertInput, renameColumns, getActivities, calc_result, simplifyExpression, four_eyes_principle, eventually_follows, attribute_value_different_persons
from main import file
import pm4py
import main as m



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
        renameColumns2(columns_to_drop, columns_to_rename, df)
        columns_to_rename_vals = list(columns_to_rename.values())
        cols = list(df.columns)
        for column in mandatory_columns:#check whether mandatory columns are in final dataframe
            self.assertIn(column, cols, msg=None)
        for column in columns_to_drop:#check whether dropped columnsare excluded from final dataframe
            self.assertNotIn(columns_to_drop, cols, msg=None)
        for column in columns_to_rename_vals: #check whether columns to be renamed are in final dataframe
            self.assertIn(column, cols, msg=None)


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
        renameColumns2(columns_to_drop, columns_to_rename, df)
        self.assertTrue(isNotDuplicate(df, getActivities2(df)))


class convertInputTestcase(unittest.TestCase):
    def testConvertInput(self):
        legit_files = {"detail_incident_activity.csv" : (466737,7), "BPI_Challenge_2013_incidents.xes": (65533,12),"semicolons.csv" :(5,17) }
        #We still have to replace the Error placeholders with the real placeholders but that can be done in the testing phase
        bad_files = {"wrong_csv_3.csv" : "Error1", "NaN_values.csv": "Error2", "empty_csv.csv" : "Error3", "empty_xes.xes" : "Error4", "wrongInput.pdf": "Error5","wrong_xes_2.xes": "Error6"}
        for check_file in legit_files:
            m.file = open(os.path.join("test_input", check_file),"r")
            m.file.filename = check_file
            df = m.convertInput()
            nrRows = getRowsNumber(df)
            nrCols = getColsNumber(df)
            row_col = (nrRows,nrCols)
            expected = legit_files[check_file]
            self.assertEquals(row_col,expected,"Data was lost during conversion")
        for check_file in bad_files:
            m.file = open(os.path.join("test_input", check_file),"r")
            m.file.filename = check_file
            current_error = bad_files[check_file]
            self.assertRaises(current_error, m.convertInput())


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

#same functions as in main.py but with an extra parameter
def renameColumns2(columns_to_drop, columns_to_rename,df):
    # we define mandatory_columns as the columns the user cannot drop and therefore
    #ignore all selections of such columns

    mandatory_columns = ["case:concept:name", "concept:name", "time:timestamp" , "org:resource"]
    #rename the dataframe by handing the rename function a dictionary
    df.rename(columns=columns_to_rename, inplace = True)

    for column in columns_to_drop:
        if(column in mandatory_columns): 
            pass
        else:
            df.drop(column, axis=1, inplace = True)
    return df

def getActivities2(df): 
    return (df['concept:name'].unique()).tolist()
<<<<<<< HEAD

def getRowsNumber(df) -> int:
    return len(df)

def getColsNumber(df) -> int: 
    return len(list(df.columns))
=======
>>>>>>> Amine_dev


class Four_eyes_principle(unittest.TestCase):
    def testfour_eyes_principle(self):
        file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
        df = pd.read_csv(file_path)

        #expression = 'four_eyes_principle(df,["Open","Closed"])'

        temp = four_eyes_principle(df,["Open","Closed"])
        temp.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)
        self.assertIsInstance(temp, pd.DataFrame)
        with self.assertRaises(ValueError):
            four_eyes_principle(df, ["Closed"])


<<<<<<< HEAD
=======
class Eventually_follows(unittest.TestCase):
    def testeventually_follows(self):
        file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
        df = pd.read_csv(file_path)
        
        #expression = 'eventually_follows(df,["Update","Closed"])'
        temp1 = eventually_follows(df,["Update","Closed"])
        temp1.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)
        self.assertIsInstance(temp1, pd.DataFrame)
        
        #expression = 'eventually_follows(df,["Update","Reassignment","Closed"])'
        temp2 = eventually_follows(df,["Update","Reassignment","Closed"])
        temp2.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)
        self.assertIsInstance(temp2, pd.DataFrame)
        
        #expression = 'eventually_follows(df,["Open","Update","Reassignment","Closed"])'
        temp3 = eventually_follows(df,["Open","Update","Reassignment","Closed"])
        temp3.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)
        self.assertIsInstance(temp3, pd.DataFrame)
        
        with self.assertRaises(ValueError):
            eventually_follows(df, ["Closed"])
            

class Attribute_value_different_persons(unittest.TestCase):
    def testattribute_value_different_persons(self):
        file_path = os.path.join(cwd,'ltl_checker', 'test_input', 'detail_incident_activity.csv')   
        df = pd.read_csv(file_path)
        #expression = 'attribute_value_different_persons(df,["Update"])'
        temp = attribute_value_different_persons(df,["Update"])
        temp.rename(columns={"case:concept:name" : "Case ID", "concept:name" : "Activity Name", "time:timestamp" : "Time Stamp" , "org:resource" : "Resource"}, inplace = True)
        self.assertIsInstance(temp, pd.DataFrame)
        
        with self.assertRaises(ValueError):
            attribute_value_different_persons(df, ["Update"])
>>>>>>> Amine_dev

if __name__ == '__main__':
    unittest.main()
