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
`localhost:5000`

## More Information
More information about use cases, features and methodologies during our project can be found in the
following documents: 

* [Project Initiation Documents](./documentation/Project%20Initiation%20Document.pdf)
* [Requirements Engineering Document](./documentation/Requirements%20Engineering.pdf)
* [Phase Review - Sprint 1](./documentation/Phase%20Review%20-%20Sprint%201.pdf)

If there are any questions please feel free to get in touch with our communications manager
[Mohamed](amine.kooli@rwth-aachen.de)


## Sprint 1
### DONE:
* Docker configuration, project setup

* The "Upload" page
<br> Currently it works only for .csv files. The columns must be separated by commas.
 ![](ltl_checker/static/images/upload.png)

* The "Columns Selection" page
![](ltl_checker/static/images/select_columns.png)

* The "About Us" page
![](ltl_checker/static/images/about_us_1.png)
![](ltl_checker/static/images/about_us_2.png)

### TODO in the next sprint:

* Fix bugs with uploading a xes file
* Unit tests for the function convertInput()
* Help user guide
* Reload button 
* Fix page refresh errors
* cleanData() function
* The filter selection page


## Documentation: 
### Python functions:


* upload() <br> This function takes in the uploaded file 'file' from the client from the firsth html form (upload.html). Then, the file is converted into a dataframe by calling convertInput() in order to work with it as a pandas dataframe. The function returns the next html page (columns-selection.html) and it returns the dataframe to the js file called columns-selection.js, which requires the conversion of said dataframe into a _json type of file, but only the first five rows are given to the js file, because only those five will be depicted in the second frame as a overview. 

* convertInput() <br> This function checks the file type of the uploaded file (i.e. .csv or .xes file) and returns the corresponding dataframe by calling the pandas package function pd.read_csv or the pm4py functions pm4py.read_xes and pm4py.convert_to_dataframe.






 

### JS functions: 


* changeCloudColor()<br>On the first html page (upload.html) we have designed a cloud that according to its color specifies the (in)correct state of the uploaded file. In case that the uploaded file is either a .csv or a .xes type of file, the cloud will change its color to green, otherwise to red. In case the uploaded file is not of the right type, an alert notification appears stating "The file should be in 
.csv or .xes format". 

* loadDataFromFile()<br> The parameter "data" is given to the function. "data" contains the first five entries of the event log from the uploaded file and the header. Then, an "empty table" is declared in the columns-selection.html file, which later will contain the overview of the first five columns. Now, the function converts the dataframe we have generated earlier into a .html readable format. The components of the table are mainly created by usage of the js function "createElement". Through a for-loop, the rows and columns are created iteratively: First, the first row is declared as the header. The for loop also generates the specific table elements (e.g. "td", "tr", "th"...). The function also contains the definition of text input fields to change a column's name. Yet, that functionality has not been implemented yet.

* Eventlisteners <br> In the js file, we have also developped multiple Eventlisteners, for example:
        a) The first EventListener handles the "drag part": It checks whether the client drags his mouse over the screen with a file from his directory that the client     wishes to drag and drop into the main box on the upload.html page
        b) The second EventListener handles the "drop part": Once the client has dropped the file into the main box and it has been uploaded, it checks whether at most one file has been uploaded. If not, the alert "You can only upload one file!" appears.








