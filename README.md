# Interactive LTL Checker in Python

Process Conformance Checking - Project Group 2

### Our project Team
Daniel Henel, Teodora Staneva, Ugo Detaille, 
Mohammed Amine Kooli, 
Vishisht Choudhary

## Task
The objective during this project is to implement an interactive
LTL Checker with which a user can upload, process and filter raw event logs in accordance
with constraints of his or her choice. The constraints can vary in complexity. E.g. the user can drop certain
drop certain columns from the raw data but also filter entries deviating from Linear temporal rules. 

## How to run the application
* Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [docker]() on your machine
* Clone the reqository<br>
`git clone https://git.rwth-aachen.de/teodora.staneva99/customizable_interface_ltl_checking.git`
* Go to the ltl_checker directory<br>
`cd customizable_interface_ltl_checking/ltl_checker`
* Build a docker image<br>
`docker build -t ltl_checker .`
* Run the docker image<br>
`docker run -p 5000:5000 -d ltl_checker`
* Open the application in your browser<br>
`localhost:500`

## More Information
More information about use cases, features and methodologies during our project can be found in the
following documents: 

* [Project Initiation Documents](./documentation/Project%20Initiation%20Document.pdf)
* [Requirements Engineering Document](./documentation/Requirements%20Engineering.pdf)


If there are any questions please feel free to get in touch with our communications manager
[Mohamed](amine.kooli@rwth-aachen.de)



##Documentation: 
Python functions:  

## Sprint 1
1) def: upload -- this function takes in the uploaded file 'file' from the client from the firsth html form (upload.html). Then, the file is converted into a dataframe by calling convertInput() in order to work with it as a pandas dataframe. The function returns the next html page (columns-selection.html) and it returns the dataframe to the js file called columns-selection.js, which requires the conversion of said dataframe into a _json type of file, but only the first five rows are given to the js file, because only those five will be depicted in the second frame as a overview. 

2) def: convertInput -- this function checks the file type of the uploaded file (i.e. .csv or .xes file) and returns the corresponding dataframe by calling the pandas package function pd.read_csv or the pm4py functions pm4py.read_xes and pm4py.convert_to_dataframe.

## Sprint 2 
* simplifyExpression() <br> This function takes a logical formula as a parameter and uses the sympy library to convert the formula into CNF. Further, the clauses of said CNF formula are separated and all those clauses are saved in a list individually. Now, within this list, the literals of all clauses are now saved in the variable clauses_list and are returned (Hence, the function returns a list of literals of a CNF).

* tupleToList() <br> is a simple helper function that converts a dataset of the type tuple into the type list

* calcResult() <br> This function takes in 3 parameters: list_of_terms is basically what simplifyExpression() returns (a list of literals), dictionary contains the assignment of the keys (letters in our case) to their respective filter function, raw_log is an event log. The function creates dynamically variables for all keys in the dictionary that the sympy library can work with. The value type is a tuple, with the first component being the filter itself, and the second one the parameters for the filter. Then, the function iterates through the dictionary by the key component and checks what filter function should be called and applies the filter. Note that the basic pm4py filter functions take in the events explicitily, which is hard for us to encode. Rather, we defined helper functions "four_eyes_principle(param1, param2) ..." that are called in calcResult, which separate lists of activities into explicit activities, that are then passed to the pm4py filter functions. For each iteration through the for loop, the filtered raw_log is saved as an array entry, which is then combined to a final output as a dataframe. Note that in the final output all duplicate entries are omitted.

* four_eyes_principle(param1, param2), eventually_follows_2(param1,param2)
eventually_follows_3(param1,param2), eventually_follows_4(param1,param2) : helper functions, see explanation above.

* renameColumns(param1, param2, param3) <br> This function takes in three parameters: param1 is a list of columns the client wishes to drop, the second one a list of columns the client wishes to change the names of, and the third one is a dataframe. We define a list of mandatory columns, which cannot be dropped (e.g. case id) where the names fit the standard of the pm4py library. Now, first, the dataframe's columns are automatically renamed to the standard names and the other columns to the name the client has entered. Then, in a for loop, the function drops all columns, making sure that none of the columns is one of the mandatory ones.

* getActivites(df) : returns the unique set of all activites of the dataframe passed to it.



 

JS functions: 

## Sprint 1
1) function changeCloudColor -- on the first html page (upload.html) we have designed a cloud that according to its color specifies the (in)correct state of the uploaded file. In case that the uploaded file is either a .csv or a .xes type of file, the cloud will change its color to green, otherwise to red. In case the uploaded file is not of the right type, an alert notification appears stating "The file should be in 
.csv or .xes format". 

2) loadDataFromFile -- The parameter "data" is given to the function. "data" contains the first five entries of the event log from the uploaded file and the header. Then, an "empty table" is declared in the columns-selection.html file, which later will contain the overview of the first five columns. Now, the function converts the dataframe we have generated earlier into a .html readable format. The components of the table are mainly created by usage of the js function "createElement". Through a for-loop, the rows and columns are created iteratively: First, the first row is declared as the header. The for loop also generates the specific table elements (e.g. "td", "tr", "th"...). The function also contains the definition of text input fields to change a column's name. Yet, that functionality has not been implemented yet.

3) In the js file, we have also developped multiple Eventlisteners, for example:
        a) The first EventListener handles the "drag part": It checks whether the client drags his mouse over the screen with a file from his directory that the client     wishes to drag and drop into the main box on the upload.html page
        b) The second EventListener handles the "drop part": Once the client has dropped the file into the main box and it has been uploaded, it checks whether at most one file has been uploaded. If not, the alert "You can only upload one file!" appears.


## Sprint 2










