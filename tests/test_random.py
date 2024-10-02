import sys

import sqlite3
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../project0')))

import main  # Now Python can find the main module

def test_createdb():
    # Create a database and check if the file exists
    db_name = main.createdb()
    assert os.path.exists(db_name)  # Ensure that the database file is created
    
    # Check if the incident table exists in the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incident';")
    table_exists = cursor.fetchone()
    assert table_exists is not None  # Verify the table is created
    conn.close()

def test_populatedb():
    # Create a temporary database for testing
    db_name = main.createdb()

    # Sample incident data to insert
    incident_records = [
        ("10/01/2024 14:00", "12345", "Main St", "Theft", "OK12345"),
        ("10/01/2024 15:00", "12346", "2nd Ave", "Robbery", "OK12346")
    ]
    
    # Populate the database with sample data
    num_records = main.populatedb(db_name, incident_records)
    
    # Check if the correct number of records were inserted
    assert num_records == len(incident_records)

def test_status():
    # Create and populate the database
    db_name = main.createdb()
    incident_records = [
        ("10/01/2024 14:00", "12345", "Main St", "Theft", "OK12345"),
        ("10/01/2024 15:00", "12346", "2nd Ave", "Robbery", "OK12346")
    ]
    main.populatedb(db_name, incident_records)
    
    # Check the status report
    report = main.status(db_name)
    
    # Ensure the report contains correct data
    assert "Theft|1" in report
    assert "Robbery|1" in report

