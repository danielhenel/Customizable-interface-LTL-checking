import unittest
import pandas as pd
import os
from main import upload, convertInput
from main import file
import pm4py

cwd = os.getcwd()




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
