import random
import sqlite3
from project0.main import createdb, populatedb, status

def test_random_incident_generation():
    # This test randomly generates incidents and inserts them into the database
    db = sqlite3.connect(":memory:")  # Use an in-memory database for testing
    c = db.cursor()

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
    db.commit()

    # Generate random incidents data
    random_incidents = [
        (
            f"{random.randint(1, 12)}/{random.randint(1, 31)}/2024 {random.randint(0, 23)}:{random.randint(0, 59):02d}",
            f"2024-{random.randint(10000000, 99999999)}",
            f"{random.randint(100, 999)} RANDOM AVE NE",
            random.choice(["Welfare Check", "Traffic Stop", "Fire Alarm", "Suspicious", "Burglary"]),
            random.choice(["OK0140200", "14005", "EMSSTAT"])
        )
        for _ in range(10)  # Generate 10 random incidents
    ]

    # Insert the random incidents into the database
    populatedb(db, random_incidents)

    # Check if the data was inserted
    c.execute("SELECT COUNT(*) FROM incidents")
    row_count = c.fetchone()[0]
    assert row_count == 10  # Ensure 10 incidents were inserted

    # Test the status function
    status(db)

    # Close the database connection
    db.close()

def test_incident_data_length():
    db = sqlite3.connect(":memory:")  # Use an in-memory database for testing
    c = db.cursor()

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
    db.commit()

    # Insert a single incident with large text fields
    large_incident = [
        (
            "9/1/2024 0:05",
            "2024-00063623",
            "12345 EXTREMELY LONG AVE NE WITH SOME UNUSUALLY LONG NAME THAT DOESN'T END",
            "This is a nature with an extremely long description for testing purposes",
            "OK0140200"
        )
    ]

    populatedb(db, large_incident)

    # Test if the large incident was inserted properly
    c.execute("SELECT * FROM incidents WHERE incident_number='2024-00063623'")
    result = c.fetchone()
    assert result is not None  # Ensure the incident exists in the database

    # Test the length of the fields
    assert len(result[2]) > 50  # Location field should be long
    assert len(result[3]) > 50  # Nature field should also be long

    # Close the database connection
    db.close()

def test_random_nature_counts(capsys):
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

    # Insert multiple random incidents
    random_incidents = [
        ('9/1/2024 0:05', '2024-00063623', '1049 RANDOM AVE NE', 'Welfare Check', 'OK0140200'),
        ('9/1/2024 0:12', '2024-00063624', '2609 RANDOM DR', 'Runaway or Lost Child', 'OK0140200'),
        ('9/1/2024 0:15', '2024-00063625', '800 RANDOM BLVD', 'Traffic Stop', '14005'),
        ('9/1/2024 0:20', '2024-00063626', '800 RANDOM BLVD', 'Fire Alarm', '14005'),
        ('9/1/2024 0:25', '2024-00063627', '1049 RANDOM AVE NE', 'Welfare Check', 'OK0140200')
    ]

    # Insert the random incidents into the database
    populatedb(db, random_incidents)

    # Test the status function and capture the output
    status(db)
    captured = capsys.readouterr()

    # Ensure the counts are correct
    expected_output = "Fire Alarm|1\nRunaway or Lost Child|1\nTraffic Stop|1\nWelfare Check|2\n"
    assert captured.out == expected_output

    # Close the database connection
    db.close()

