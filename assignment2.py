import urllib.request
import tempfile
import PyPDF2
import re
from collections import defaultdict
from pypdf import PdfReader
from datetime import datetime
from geopy.geocoders import ArcGIS
import pandas as pd
import argparse
import csv
from math import atan2, pi
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Define a function to extract incident details from raw data.
def extract_incident_details(raw_data, incident_list):
    # Create a temporary file to store PDF data.
    temp_file = tempfile.TemporaryFile()
    # Write the raw data to the temporary file.
    temp_file.write(raw_data)
    # Set the file's current position at the beginning.
    temp_file.seek(0)
    # Initialize a PDF reader for the temporary file.
    pdf_reader = PyPDF2.PdfFileReader(temp_file)
    # Get the total number of pages in the PDF.
    total_pages = pdf_reader.getNumPages()
    # Initialize a list to hold extracted data.
    extracted_data = []

    # Define a function to refine the extracted content.
    def refine_content(content):
        # Clean up the content by replacing certain patterns.
        content = content.replace(" \n", " ")
        content = re.sub('\n(\\d?\\d/\\d?\\d/\\d{4} )', lambda x: f'\n||{x.group(1)}', content)
        # Split the content into lines and return the result.
        return [line.split('\n') for line in str.strip(content).split('\n||')]

    # Loop through each page in the PDF.
    for page in range(total_pages):
        # Extract text from the current page.
        page_content = pdf_reader.getPage(page).extractText()
        # Perform specific replacements on the first page to clean up headers.
        if page == 0:
            page_content = page_content.replace("Date / Time\nIncident Number\nLocation\nNature\nIncident ORI\n", "")
            page_content = page_content.replace("\nNORMAN POLICE DEPARTMENT\nDaily Incident Summary (Public)\n", "")
        # Refine the page content and extend the extracted data list.
        refined_data = refine_content(page_content)
        extracted_data.extend(refined_data)

    # Handle special cases based on the number of elements in each extracted data item.
    special_case1 = [[elements[0], elements[1], '', '', elements[2]] for elements in extracted_data if len(elements) == 3]
    special_case2 = [[elements[0], elements[1], elements[2], '', elements[3]] for elements in extracted_data if len(elements) == 4]
    # Combine the standard and special case items.
    extracted_data = [elements for elements in extracted_data if len(elements) == 5] + special_case1 + special_case2

    # Post-process the extracted data to label certain incidents as 'EMSSTAT'.
    indicator = 0
    for item in reversed(extracted_data):
        if item[-1] == 'EMSSTAT':
            indicator = 2
        else:
            if indicator > 0:
                item[-1] = 'EMSSTAT'
                indicator -= 1

    # Extend the main incident list with the extracted data and return it.
    incident_list.extend(extracted_data)
    return incident_list

import math

def find_side_of_town(lat, lon):
    """
    Determines the side of the town based on the given latitude and longitude coordinates.

    Args:
        lat (float): The latitude coordinate.
        lon (float): The longitude coordinate.

    Returns:
        str: A string representing the side of the town (N, NE, E, SE, S, SW, W, NW).
    """
    # Define the center point coordinates
    CENTER_LAT = 35.220833
    CENTER_LON = -97.443611

    # Calculate the differences in coordinates
    delta_lon = lon - CENTER_LON
    delta_lat = lat - CENTER_LAT

    # Calculate the bearing angle in degrees
    bearing = (math.atan2(delta_lon, delta_lat) * 180 / math.pi + 360) % 360

    # Determine the corresponding direction based on the bearing angle
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    index = int(round(bearing / 45)) % 8
    side_of_town = directions[index]

    return side_of_town

def find_nature_rank_loc_rank(incidents):
    """
    Ranks the nature types and locations based on their frequency in the given incidents.

    Args:
        incidents (list): A list of incidents, where each incident is a list containing information about the incident.
                          The nature type is expected to be at index -2, and the location at index 2.

    Returns:
        tuple: A tuple containing two dictionaries:
            1. nature_ranks: A dictionary mapping nature types to their ranks based on frequency.
            2. loc_ranks: A dictionary mapping locations to their ranks based on frequency.
    """
    # Rank nature types by frequency
    nature_freq = defaultdict(int)
    for incident in incidents:
        nature_freq[incident[-2]] += 1  # Count occurrences of each nature type

    sorted_natures = sorted(nature_freq.items(), key=lambda x: (-x[1], x[0]))
    nature_ranks = _assign_ranks(sorted_natures)

    # Rank locations by frequency
    loc_freq = defaultdict(int)
    for incident in incidents:
        loc_freq[incident[2]] += 1  # Count occurrences of each location

    sorted_locations = sorted(loc_freq.items(), key=lambda x: (-x[1], x[0]))
    loc_ranks = _assign_ranks(sorted_locations)

    return nature_ranks, loc_ranks

def _assign_ranks(sorted_items):
    """
    Assigns ranks to the given items based on their frequency.

    Args:
        sorted_items (list): A list of (item, frequency) tuples, sorted by frequency in descending order.

    Returns:
        dict: A dictionary mapping each item to its rank based on frequency.
    """
    ranks = {}
    prev_freq = None
    rank = 0
    freq_count = 0

    for item, freq in sorted_items:
        if freq != prev_freq:
            rank += freq_count  # Update rank based on previous group of items with the same frequency
            freq_count = 0
            prev_freq = freq

        freq_count += 1
        ranks[item] = rank + freq_count  # Assign rank to the current item

    return ranks


# Define a function to retrieve the weather code for a specific location and time.
def retrieve_weather_code(location, date, weather_api, hour):
    # Define the API URL for retrieving weather data.
    api_url = "https://archive-api.open-meteo.com/v1/archive"
    # Set up the query parameters with the location, date, and desired data.
    query_params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "start_date": date,
        "end_date": date,
        "hourly": "weather_code"
    }
    # Make the API call to get weather data.
    api_responses = weather_api.weather_api(api_url, params=query_params)
    first_response = api_responses[0]
    hourly_data = first_response.Hourly()
    # Extract the weather code from the response.
    weather_codes = hourly_data.Variables(0).ValuesAsNumpy()
    specific_weather_code = int(weather_codes[hour])
    return specific_weather_code

# Define a function to process incident data, enrich it with additional information, and prepare for analysis.
def process_incident_data(incident_records):
    results = []
    # Initialize a geolocator to find geographic information.
    geolocator = ArcGIS()
    # Set up a cached session to reduce repeated API calls.
    cache_session = requests_cache.CachedSession('.cache', expire_after=-1)
    retried_session = retry(cache_session, retries=5, backoff_factor=0.2)
    # Initialize a client for the Open Meteo service.
    meteo_client = openmeteo_requests.Client(session=retried_session)
    # Rank the nature and location of incidents.
    nature_ranking,location_ranking= find_nature_rank_loc_rank(incident_records)

    # Process each record to enrich it with additional contextual data.
    for record in incident_records:
        temp_row = []
        # Parse the date and time from the record.
        date_str, time_str = record[0].split(' ')
        date_obj = datetime.strptime(date_str, "%m/%d/%Y")
        # Calculate the day of the week, adjusting it to start from 1.
        week_day_idx = date_obj.weekday()
        adjusted_week_day = (week_day_idx + 1) % 7 + 1
        # Extract the hour of the incident.
        hour_of_incident = int(time_str.split(':')[0])
        # Geocode the location to get latitude and longitude.
        location = geolocator.geocode(','.join(record[2].split('/')) + ', Norman, OK')
        # Default the side of town to 'X' and update if location is found.
        town_side = 'X'
        if location:
            town_side = find_side_of_town(location.latitude, location.longitude)
        # Default weather condition code to 1 and update if location is available.
        weather_condition_code = 1
        if location:
            current_date = date_obj.strftime("%Y-%m-%d")
            weather_condition_code = retrieve_weather_code(location, current_date, meteo_client, hour_of_incident)

        # Compile the enriched data into a row and add it to the results.
        temp_row.extend([adjusted_week_day, hour_of_incident, weather_condition_code, location_ranking[record[2]], town_side, nature_ranking[record[-2]], record[-2], record[-1] == 'EMSSTAT'])
        results.append(temp_row)
        #print(temp_row)
    return results

# Define a function to retrieve incident data from a given URL.
def retrieve_incident_data(target_url):
    # Define the user-agent to mimic a web browser for the HTTP request.
    request_headers = {}
    request_headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    # Fetch the data from the URL and return it.
    fetched_data = urllib.request.urlopen(
        urllib.request.Request(target_url, headers=request_headers)).read()
    return fetched_data

# Define a function to orchestrate the entire processing of incident data given a file with URLs.
def run_process(file_path):
    # Initialize a list to hold incident URLs.
    incident_urls = []
    # Open and read the file containing the URLs.
    with open(file_path, 'r') as file:    
        csv_reader = csv.reader(file)
        for row in csv_reader:
            # Clean and extract the URL from each row.
            processed_url = row[0].strip()
            processed_url = processed_url[processed_url.find('https://'):]
            incident_urls.append(processed_url)
    
    # Initialize a list to collect all incident data.
    collected_incidents = []
    # Retrieve and process data for each incident URL.
    for incident_url in incident_urls:
        incident_data = retrieve_incident_data(incident_url)
        collected_incidents = extract_incident_details(incident_data, collected_incidents)
    # Process and print the collected incident data.
    processed_data = process_incident_data(collected_incidents)
    data_labels = ["Day of the Week","Time of Day","Weather","Location Rank","Side of Town","Incident Rank","Nature","EMSSTAT"]
    print('\t'.join(data_labels))
    for data_row in processed_data:
        print('\t'.join(map(str, data_row)))

# Entry point of the script: parse command-line arguments and trigger the processing.
if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--urls", type=str, required=True, help="URLs file path.")
    parsed_args = argument_parser.parse_args()
    if parsed_args.urls:
        run_process(parsed_args.urls)


