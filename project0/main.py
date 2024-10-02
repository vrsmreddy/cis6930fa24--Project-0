# -*- coding: utf-8 -*-
# main.py
import argparse
import urllib.request
import tempfile
import PyPDF2
import re
import os
import sqlite3

# Function to fetch incidents from a given URL
def fetchincidents(url):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    data = response.read()
    return data

# Function to extract incidents from PDF data
def extractincidents(pdf_data):
    with tempfile.TemporaryFile() as tmp_file:
        tmp_file.write(pdf_data)
        tmp_file.seek(0)
        pdf = PyPDF2.PdfFileReader(tmp_file)
        incidents = []
        replacements = {
            "Date / Time Incident Number Location Nature Incident ORI": "",
            "Daily Incident Summary (Public)": "",
            "NORMAN POLICE DEPARTMENT": "\n",
            " \n": " "
        }
        for num in range(pdf.numPages):
            text = pdf.getPage(num).extractText()
            for old, new in replacements.items():
                text = text.replace(old, new)
            text = re.sub('\n(\\d?\\d/\\d?\\d/\\d{4} )', r'\n||\1', text)
            entries = [entry.split('\n') for entry in text.strip().split('\n||')]
            incidents.extend(entries)

    formatted_data = [entry for entry in incidents if len(entry) == 5]
    return formatted_data

# Function to create a new SQLite database
def createdb():
    resource_path = './resources'
    if not os.path.exists(resource_path):
        os.makedirs(resource_path)
    database_name = os.path.join(resource_path, 'normanpd.db')
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS incident')
        cursor.execute('CREATE TABLE incident (Time TEXT, Incident_Number TEXT, Location TEXT, Nature TEXT, Incident_ORI TEXT);')
    return database_name

# Function to populate the database with incident records
def populatedb(database_name, incident_records):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO incident VALUES (?,?,?,?,?)", incident_records)
    return len(incident_records)

# Function to generate the incident status report from the database
def status(database_name):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        query_result = cursor.execute("SELECT Nature, COUNT(*) as count FROM incident GROUP BY Nature ORDER BY Nature").fetchall()
    report = ""
    for nature, count in query_result:
        report += f"{nature}|{count}\n"
    return report

# Main function to run the process
def main(url):
    # Download data
    incident_data = fetchincidents(url)

    # Extract data
    incidents = extractincidents(incident_data)
    
    # Create new database
    db = createdb()
    
    # Insert data
    populatedb(db, incidents)
    
    # Print incident counts
    print(status(db))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary URL.")
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)

