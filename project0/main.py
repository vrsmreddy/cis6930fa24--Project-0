import urllib.request
from pypdf import PdfReader
import sqlite3
import io
import re
import argparse

# Function to fetch the PDF data from the provided URL
def fetchincidents(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    return response.read()

# Function to extract incidents from the PDF data
def extractincidents(pdf_data):
    reader = PdfReader(io.BytesIO(pdf_data))
    incidents = []

    for page in reader.pages:
        text = page.extract_text()
        incidents.extend(parse_incident_data(text))
    return incidents

# Helper function to parse the text into incident fields using regular expressions
def parse_incident_data(text):
    incidents = []

    # Updated pattern to capture date/time, incident number, location (ends with specified suffix or lat/long),
    # nature, and ORI
    pattern = r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) ' \
              r'(\d{4}-\d{8}) ' \
              r'((?:[A-Z0-9 /]+(?:DR|AVE|NE|RR|P|PL|ST|SW|BLVD|CIR|PKWY|RD|HWY|CT|SE|NW|RAMP|LN|BOARDWALK|WAY|GRN|OK-9|TER|SB I|AV|LN|UNIT 1201|Interstate|SQ|CT|CITY|Robinson|STREET|NB I|- GOLDSBY)|[0-9.-]+;[0-9.-]+)) ' \
              r'(.+?) ' \
              r'(OK\d{6}|EMSSTAT|14005|14009)'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    for match in matches:
        incident_time, incident_number, location, nature, incident_ori = match

        # Post-process location to handle unexpected characters
        location = location.strip()
        nature = nature.strip()

        # Handle common edge cases, e.g. "911 Call Nature" or unknown values
        if "911" in nature:
            nature = "911 Call Nature Unknown"
        elif not nature:
            nature = "Unknown"

        # Append the parsed tuple (incident_time, incident_number, location, nature, incident_ori)
        incidents.append((incident_time, incident_number, location, nature, incident_ori.strip()))

    return incidents

# Function to create (and overwrite) the SQLite database and table
def createdb():
    conn = sqlite3.connect('resources/normanpd.db')  # Create or connect to the database
    c = conn.cursor()  # Create a cursor object
    # Drop the incidents table if it exists to ensure fresh data
    c.execute('DROP TABLE IF EXISTS incidents')
    # Create the incidents table
    c.execute('''
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    conn.commit()  # Commit the transaction
    return conn

# Function to insert the parsed incident data into the database
def populatedb(db, incidents):
    c = db.cursor()
    c.executemany('''
        INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
        VALUES (?, ?, ?, ?, ?)
    ''', incidents)  # Insert the incidents into the table
    db.commit()  # Commit the transaction

# Function to print a summary of incidents grouped by their nature
def status(db):
    c = db.cursor()
    # Query to group the incidents by their nature and count the occurrences
    c.execute('SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC')
    rows = c.fetchall()  # Fetch all rows from the result
    for row in rows:
        print(f'{row[0]}|{row[1]}')  # Print nature and count

# Main function to orchestrate the process
def main(url):
    pdf_data = fetchincidents(url)  # Download the PDF
    incidents = extractincidents(pdf_data)  # Extract incidents from the PDF
    db = createdb()  # Create the SQLite database, overwriting if it exists
    populatedb(db, incidents)  # Insert the incidents into the database
    status(db)  # Print the summary of incidents

# Entry point of the script
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL")
    args = parser.parse_args()
    main(args.incidents)

