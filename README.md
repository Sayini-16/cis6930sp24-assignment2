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

The projects have below files: 

## 1. Assignment2.py

### **extract_incident_details(raw_data, incident_list)**

The function extracts incident data from a PDF, using PyPDF2 to read and extract text from each page. It refines this text, addressing formatting issues and special data structures, then categorizes incidents, particularly marking some as 'EMSSTAT' based on their content. Finally, it appends the processed data to a provided incident list.
![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/80092789-8b21-4120-8298-2033ef0f3edc)

### **find_side_of_town(lat, lon)**
This function determines a location's direction relative to a town's center using latitude and longitude. It calculates the bearing angle from the center and maps this to one of the eight cardinal directions (N, NE, E, SE, S, SW, W, NW) to represent the location's side in the town.
![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/33f84c03-c852-444e-91b8-0d51645f6689)

### **find_nature_rank(incidents)**
This function ranks incident types based on their frequency in a list of incidents. It counts occurrences, sorts the incident types by frequency (and alphabetically for ties), then assigns a rank to each, with the most frequent getting the lowest rank. The function returns a dictionary mapping each incident type to its rank.
![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/45d9db5d-7123-4288-a778-a4e3cccda22e)


### **find_loc_rank(incidents)**
This function calculates and assigns ranks to different locations based on the frequency of incidents occurring there. It counts each location's occurrences, sorts them by frequency (and alphabetically for ties), and assigns ranks, with the most frequent location being ranked the highest. The output is a dictionary mapping each location to its rank.
![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/c684053b-abcd-4761-9ac0-63eb51f5a1e1)

### **retrieve_weather_code(location, date, weather_api, hour)**
This function retrieves the weather code for a given location and date, at a specified hour, using a weather API. It constructs a query with location coordinates and date, makes an API call, then parses the response to extract the weather code for the specified hour, returning this specific code.

![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/5c2d2fce-5a37-4eaf-88fb-cc60da278758)

<br>

### **process_incident_data(incident_records)**
This function processes incident records, adding contextual information like weather conditions, geographical details, and incident rankings. It geocodes locations, retrieves weather codes for specific times, and calculates rankings for incident nature and locations. Each record is enriched with this additional data, including the day of the week, hour of the incident, weather conditions, location ranking, town side, nature ranking, and an EMS status flag, then added to a results list for analysis.
![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/dec4765c-fe21-46e6-a336-d41668a6a07f)
<be>
### **retrieve_incident_data(target_url)**
This function retrieves data from a specified URL, posing as a web browser by setting a user-agent in the request header. It fetches the data using a GET request and returns the fetched data, allowing for the retrieval of web content that might require a browser-like request for access.

![image](https://github.com/Sayini-16/cis6930sp24-assignment2/assets/81869410/a2be73d6-9548-4850-bbe3-893035bc4634)


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

