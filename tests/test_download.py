import sys
import os
import sqlite3

from project0.main import fetchincidents, createdb, extractincidents, populatedb, status

# Add the parent directory (cis6930fa24-project0) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_fetchincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-01_daily_incident_summary.pdf"
    pdf_data = fetchincidents(url)
    assert pdf_data is not None
    assert len(pdf_data) > 0  # Ensure the PDF data is fetched and not empty

def test_db_creation():
    db = createdb()
    assert db is not None

def test_extraction():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-01_daily_incident_summary.pdf"
    pdf_data = fetchincidents(url)
    incidents = extractincidents(pdf_data)
    assert len(incidents) > 0

def test_status(capsys):
    # Create an in-memory SQLite database for testing
    db = sqlite3.connect(":memory:")

    # Create the incidents table
    c = db.cursor()
    c.execute('''
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    ''')
    db.commit()

    # Sample incident data
    test_incidents = [
        ('9/1/2024 0:05', '2024-00063623', '1049 12TH AVE NE', 'Welfare Check', 'OK0140200'),
        ('9/1/2024 0:12', '2024-00063624', '2609 CHATEAU DR', 'Runaway or Lost Child', 'OK0140200'),
        ('9/1/2024 0:15', '2024-00063625', '1049 12TH AVE NE', 'Welfare Check', 'OK0140200'),
        ('9/1/2024 0:20', '2024-00063626', '800 W ROBINSON ST', 'Fire Alarm', '14005'),
    ]

    # Insert test incidents into the in-memory database
    populatedb(db, test_incidents)

    # Call the status function and capture the output
    status(db)

    # Capture printed output
    captured = capsys.readouterr()
    expected_output = "Fire Alarm|1\nRunaway or Lost Child|1\nWelfare Check|2\n"
    assert captured.out == expected_output

    # Close the database connection
    db.close()

def test_fetch_invalid_url():
    invalid_url = "https://www.invalidurl.com/nonexistent.pdf"
    try:
        pdf_data = fetchincidents(invalid_url)
        assert pdf_data is None  # This should raise an exception or return None
    except Exception:
        assert True  # Exception was raised as expected

