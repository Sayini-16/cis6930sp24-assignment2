import pytest
import os
import io
import sqlite3

from assignment2 import extract_incident_details,retrieve_incident_data,find_side_of_town,find_nature_rank,process_incident_data

@pytest.fixture
def url():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-03/2024-03-01_daily_incident_summary.pdf"
    return url

@pytest.fixture
def incidents():
    incidents = []
    incidents.append(['3/1/2024 9:08', '2024-00014887', '911 W MAIN ST', 'Parking Problem', 'OK0140200'])
    incidents.append(['3/1/2024 9:04', '2024-00014894', '400 26TH AVE NW', 'Parking Problem', 'OK0140200'])
    incidents.append(['3/1/2024 9:02', '2024-00004401', '901 N PORTER AVE', 'Transfer/Interfacility', 'EMSSTAT'])
    incidents.append(['3/1/2024 9:00', '2024-00014886', '1005 W BROOKS ST', 'Parking Problem', 'OK0140200'])
    incidents.append(['3/1/2024 8:55', '2024-00014891', '511 156TH AVE NE', 'Animal Trapped', 'OK0140200'])
    incidents.append(['3/1/2024 8:51', '2024-90000079', '4420 132ND AVE SE', 'Harassment / Threats Report', 'OK0140200'])
    incidents.append(['3/1/2024 8:43', '2024-00014884', '3104 WOODCREST CREEK DR', 'Extra Patrol', 'OK0140200'])
    incidents.append(['3/1/2024 8:31', '2024-00014883', '1601 MCGEE DR', 'Parking Problem', 'OK0140200'])
    return incidents

def test_retrieve_incident_data(url):
    file_data = retrieve_incident_data(url)
    assert isinstance(file_data, bytes)

def test_extract_incident_details(url):
    reader = retrieve_incident_data(url)
    data = extract_incident_details(reader,[])
    assert len(data) == 326

def test_find_side_of_town():
    test_lat = 35.271186091975
    test_lon = -97.441293679881
    expected_output = 'N'
    actual_output = find_side_of_town(test_lat, test_lon)
    assert actual_output == expected_output

def test_find_nature_rank(incidents):
    nature_dict = find_nature_rank(incidents)
    nature = 'Parking Problem'
    assert nature_dict[nature] == 1

def test_process_incident_data(incidents):
    result = process_incident_data(incidents)
    expected = [6, 8, 1, 2, 'SW', 1, 'Parking Problem', False]
    assert expected in result
