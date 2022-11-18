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


