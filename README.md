## Asignment2 - CIS 6930 Spring 2024 

## Author: Anirudh Sayini

## Description

In this assignment, we will perform a subsequent task for the data pipeline. We will will take records from several instances of pdf files and augment the data. You will also create a Datasheet for the dataset I am creating. Reviewing the discussion from the lecturee to guide my creation of the data sheet.

The website contains three types of summaries arrests, incidents, and case summaries. Your assignment is to build a function that collects only the incidents. To do so, you need to write Python (3) function(s) to do each of the following:

- Download the data given one incident pdf
- Extract the fields:
  - Date / Time
  - Incident Number
  - Location
  - Nature
  - Incident ORI
- Data Augmentation
  - Day of Week: The day of week is a numeric value in the range 1-7. Where 1 corresponds to Sunday and 7 corresonds of Saturday.
  - Time of Data: The time of data is a numeric code from 0 to 24 describing the hour of the incident.
  - Weather: Determine the weather at the time and location of the incident. The weather is determined by the WMO CODE. The code is an integer that represents a weather position..
  - Location Rank: Sort all listed locatiions. Give an integer ranking of the frequency of locations with ties preserved. For instance, if there is a three-way tie for the most popular location, each location will be         ranked 1; the next most popular location should be ranked 4. You can use the exact text of the location.
  - Side of Town: The side of town is one of eight items {N, S, E, W, NW, NE, SW, SE}. Side of town is determined by approximate orientation of the center of town 35.220833, -97.443611. You can use the geopy library for      assistance.
  - Incident Rank: Sort all of the Natures. Give an integer ranking of the frequency of natures with ties preserved. For instance, if there is a three-way tie for the most popular incident, each incident will be ranked 1; the next most popular nature should be ranked 4.
  - Nature: The Nature is the direct text of the Nature from the source record.
  - EMSSTAT: This is a boolean value that is True in two cases. First, if the Incident ORI was EMSSTAT or if the subsequent record or two contain an EMSSTAT at the same time and locaton.

## Setting up the Initial installations 
In the project's virtual environment, we execute the following installations. 
~~~
pipenv install pypdf
~~~
The rest of the packages are part of the standard library, so there's no need for separate installations; they only need to be imported into the script.


## Packages Required:

- request
- tempfile
- PyPDF2
- geopy.geocoders import ArcGIS
- openmeteo_requests
- requests_cache
- retry_requests import retry


\
## Video Link : https://github.com/rajeshuppala1449/cis6930sp24-assignment0/assets/48644047/54e895e9-a13d-403a-8a50-45f801182985
The projects have below files: 
## 1. main.py 
 
assignment0.py is imported into this file.
This file will get the url as argument. 
Functions for extracting data, parsing data and printing the data is present in assignment0 module. These functions are called from this file.

## 2. Assignment0.py

### **fetchincidents(url)**

This function downloads a PDF document from a given URL
Makes an HTTP GET request to the specified URL to retrieve the PDF, then reads the PDF into a PdfReader object for processing.

### **extractincidents(incident_data)**

Extracts incident information from all pages of the provided PDF document.
Iterates through each page of the PDF, extracting text and processing it through parsePage to compile a comprehensive list of incidents.

On the first page and last page of pdf, some unnecessary text is removed using following logic

![image](https://github.com/rajeshuppala1449/EPAM_git/assets/48644047/adb1b3fb-5b13-40e9-8431-ce467812d23b)

Entire page is coverted to lines, these lines are passed to parsePage() function to get incidnets list.

### **parsePage(text,incidentList)**

The **parsePage** function is designed to parse through lines of text from a document, extracting specific information about incidents to populate an incident list. Each line is analyzed to identify and extract key pieces of information based on patterns defined by regular expressions. The extracted details include the time of the incident, the incident number, the location (address), the nature of the incident, and the Originating Agency Identifier (ORI). These details are then compiled into a list that represents a single incident record. The function operates as follows:

**Time Extraction:** Searches each line for a time pattern (e.g., "HH:MM") using a regular expression. If a match is found, the time is recorded.

**Nature of Incident:** If the time is not found (indicating the line doesn't contain the time of an incident), the function then looks for the nature of the incident. This search is based on a pattern that expects one or more capital letters followed by lowercase letters, possibly separated by spaces or slashes, indicating the type of incident (e.g., "Theft", "Assault").

**Incident Number Extraction:** Independently of the time and nature, searches for an incident number formatted as "YYYY-NNNNNNNN".

**Address Extraction:** After identifying an incident number, it looks for the address or location of the incident. This could be a specific format (numbers, letters, slashes, dashes, spaces) or a placeholder ("<UNKNOWN>") if the location is not specified.

**Nature of Incident:** If the initial nature search was not successful, it conducts a more focused search for the nature of the incident based on specific keywords ("COP", "MVA", "EMS", "911"), followed by additional descriptive text.

**ORI Extraction:** Searches for specific ORI codes within the line, which are unique codes assigned to agencies.

Constructs a list with the extracted time, incident number, address, nature, and ORI, and appends this list to incidentList, which accumulates all incident records.
This function systematically breaks down each line of text to extract and organize critical information about incidents into a structured format, facilitating further analysis or record-keeping.



**Handling missing files**
<br>
In some cases, the address and nature fields in the incident data rows are missing. When these fields are identified as empty through regex extraction, they are then assigned an empty string to ensure consistency in the data format.

### **createdb(path)**


The createdb function is designed to create a new SQLite database for storing incident records. It takes a file path as its argument, which specifies where the SQLite database file should be created or opened if it already exists. Here's a step-by-step breakdown of what the function does:
-Connect to the SQLite Database
-Create Cursor Object
-Drop Existing Table (if exists)
-Create incidents Table
-Return Connection

![image](https://github.com/rajeshuppala1449/EPAM_git/assets/48644047/da903d11-bb11-4ccc-bf31-f04dc4e6ad19)
<br>

The function then executes a multi-line SQL command to create a new table named incidents if it does not already exist. The table is structured with five columns to store the incident time (incident_time), incident number (incident_number), incident location (incident_location), the nature of the incident (nature), and the Originating Agency Identifier (incident_ori).

### **populatedb(conn, incidentList)**

The populatedb function is designed to insert a list of incident records into an existing SQLite database table named incidents. It takes two parameters: conn, a SQLite connection object representing an open connection to the database, and incidentList, a list of tuples where each tuple contains data for a single incident record. 

![image](https://github.com/rajeshuppala1449/EPAM_git/assets/48644047/dbc2bd1a-7741-4ab9-8bf6-01c2f4344cff)
<br>

This function returns conn.total_changes, which is an attribute of the SQLite connection object that indicates the total number of database rows that have been modified, inserted, or deleted since the database connection was opened. In the context of this function, it reflects the number of incident records successfully inserted into the database by this operation.

### **status(conn)**

The status function queries an SQLite database to summarize the occurrence frequency of different incident natures within the incidents table. It accomplishes this by creating a cursor from the given connection (conn), executing a SQL query to group incidents by their nature and count the occurrences of each group, then fetching the results. These results are sorted in descending order by count and, if counts are equal, alphabetically by nature. After sorting, the function formats these grouped counts into a list of strings, each representing a unique incident nature followed by its occurrence count, separated by a pipe symbol (|). Finally, the database connection is closed, and the formatted list is returned, providing a concise summary of incident data grouped by nature.
![image](https://github.com/rajeshuppala1449/EPAM_git/assets/48644047/347b2ac1-d98c-40bf-8438-8d6356c5187a)
<br>

## To run the Pytest : 
Run the following command ro run the tests
~~~
 pipenv run python -m pytest
~~~

## 4.Assumptions/Bugs:

- In this project we assumed that only location and nature columns have missing values in the pdf document and we handled only the missing values in those columns, if any other column has the missing values in the pdf the code will fail. 
- After splitting the data by date the maximum length of the list we observed is 7, if the length of list is > 7 then the code may fail in this case.
- I assumed that among location and nature, if my data gives only list of length 4 then nature column is missing, this assumption is made after looking into the files, but if location is missed instead of nature then this code will fail.


## Steps to Run Assignment0


- **Step1** \
Navigate to directory that we cloned from git and run the below command to install dependencies

> pipenv install

- **Step2** \
Then run the below command by providing URL

> pipenv run python assignment0/main.py --incidents **URL**

- **Step3** 

Then run the below command to test the testcases. 

> pipenv run python -m pytest -v

