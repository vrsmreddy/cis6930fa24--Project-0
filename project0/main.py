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

# Helper function to parse the text into incident fields using regular expressions and NER
def parse_incident_data(text):
    incidents = []

    # Updated pattern to capture date/time, incident number, location, nature, and ORI
    pattern = r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) (\d{4}-\d{8}) ((?:[A-Z0-9 /]+(?:ST|AVE|BLVD|CT|PKWY|RD|HWY|PL|DR|LN|CIR|SQ|WAY|TERR|BYP|TRL|ALLEY|RAMP|INTERSTATE|OVERPASS|EXPY|RR)|[0-9.-]+;[0-9.-]+)) (.+?) (OK\d{6}|EMSSTAT|14005|14009)'

    # Find all matches in the text
    matches = re.findall(pattern, text)

    for match in matches:
        incident_time, incident_number, location_raw, nature_raw, incident_ori = match

        # Process location using regex
        location = extract_location(location_raw)
        
        # Process nature and remove any incorrect prefixes
        nature = extract_nature(nature_raw)

        # Clean up directional indicators from the nature field if mistakenly attached
        nature = clean_nature(nature)

        incidents.append((incident_time, incident_number, location, nature, incident_ori.strip()))

    return incidents

# Function to clean up nature field by removing direction prefixes (NE, NW, SE, SW)
def clean_nature(nature):
    # Remove leading/trailing spaces and lowercase
    nature = nature.strip().lower()

    # Directions to remove from nature descriptions
    directions = ["ne", "nw", "se", "sw", "grn", "/"]

    # Remove direction if it's at the beginning of the nature string
    for direction in directions:
        if nature.startswith(direction + " "):
            nature = nature[len(direction) + 1:]

    # Ensure nature is capitalized properly
    nature = ' '.join([word.capitalize() for word in nature.split()])

    return nature

# Function to extract nature by cleaning it further, handles 911 calls and other specific cases
def extract_nature(nature_raw):
    nature = nature_raw.strip()

    # Special handling for 911 calls
    if "911" in nature:
        return "911 Call Nature Unknown"
    
    return nature

# Function to extract location using regex and manual parsing
def extract_location(location_raw):
    # Clean location by stripping unnecessary characters like slashes
    location = location_raw.strip().replace("/", "").replace("RR", "Railroad")

    # Add any additional cleaning logic here if necessary
    return location

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
    
    # Print nature and count in the expected format
    for row in rows:
        print(f'{row[0]}|{row[1]}')

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

