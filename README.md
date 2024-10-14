# Project-0---CIS-6930-Fall-2024
## Name:
Rama Satyanarayana Murthy Reddy Velagala

## Project Description
This project is designed to extract data from an online source, specifically the Norman, Oklahoma Police Department's incident summary PDF. The goal is to parse the PDF, extract incident data, and store it in a SQLite database. The program extracts fields such as Date/Time, Incident Number, Location, Nature, and Incident ORI from the PDF, populates the data into a database, and provides a summary of the nature of incidents and the number of times each occurred.

The project demonstrates proficiency in Python3, SQL, regular expressions, and Linux command-line tools.

## How to Install

1. Clone the project repository from GitHub:
   ```bash
   git clone https://github.com/vrsmreddy/Project-0---CIS-6930-Fall-2024.git
   cd Project-0---CIS-6930-Fall-2024
2.Install pipenv, if not already installed:
```
pip install pipenv
```
3.Install the required dependencies using pipenv:
``` 
pipenv install
```
4. Activate the virtual environment:
``` 
pipenv shell
```
## How to Run
To run the program, use the following command inside the project directory:
``` bash
pipenv run python project0/main.py --incidents [incident_summary_url]
```
Example usage:
```bash
pipenv run python project0/main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-01_daily_incident_summary.pdf

```
Example Output:
```bash
Alarm|17
Assist Fire|1
Contact a Subject|35
Drunk Driver|3
Traffic Stop|49
Welfare Check|29
...
```
## Demo

Watch the demo [here](https://drive.google.com/file/d/1Iw-HH8e-6EXdSqBZD91zhyuqDosBOuft/view?usp=sharing).

## Functions
# fetchincidents(url)
- **Parameters**: 
  - `url`: A string representing the URL of the incident PDF file.
- **Process**: 
  - This function sends an HTTP request to the given URL, retrieves the PDF file, and returns its content as bytes.
- **Returns**: 
  - A byte stream representing the downloaded PDF.
    
**Example**:  
```python
pdf_data = fetchincidents("https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-01_daily_incident_summary.pdf")
```
### extractincidents(pdf_data)

**Parameters:**
- `pdf_data`: A byte stream representing the downloaded PDF content.

**Process:**
1. Writes the PDF data to a temporary file.
2. Reads the PDF using `PyPDF2.PdfFileReader`.
3. Extracts text from each page of the PDF.
4. Replaces specific unwanted text strings (e.g., headers and footers) and adjusts formatting using regular expressions to identify incident entries.
5. Parses each entry into a list containing the incident fields: `date/time`, `incident number`, `location`, `nature`, and `ORI`.
6. Filters out any entries that don't contain the expected number of fields.

**Returns:**
- A list of lists (each representing an incident) with five fields: `(date/time, incident number, location, nature, ORI)`.

**Example:**

```python
incidents = extractincidents(pdf_data)
```

 # createdb()
- **Parameters**: 
  - None.
- **Process**: 
  - This function creates a new SQLite database (or connects to an existing one).
  - Drops any existing `incidents` table to ensure the database is fresh.
  - Creates a new `incidents` table with columns for time, number, location, nature, and ORI.
- **Returns**: 
  - A connection object to the SQLite database.
    
**Example**:  
```python
 db = createdb()

```
# populatedb(database_name, incident_records)
- **Parameters**: 
  - `database_name`: An SQLite database connection object.
  - `incident_records`: A list of incident tuples `(incident_time, incident_number, location, nature, incident_ori)`.
- **Process**: 
  - Inserts the list of incidents into the SQLite database's `incidents` table.
  - Commits the transaction to save the data.
- **Returns**: 
  - None.

**Example**:  
```python
populatedb(db, incidents)

```
# status(database_name)
- **Parameters**: 
  - `database_name`: The path to the SQLite database file.
- **Process**: 
  - Queries the database to count the occurrences of each incident nature.
  - Prints the results to the console in a pipe-separated format (`nature|count`), sorted alphabetically by nature.
- **Returns**: 
  - None.

**Example**:  
```python
status(db)

```
# main(url)
- **Parameters**: 
  - `url`: A string representing the URL of the incident PDF file.
- **Process**: 
  This function orchestrates the overall process:
  -  Downloads the PDF using `fetchincidents()`.
  -  Extracts incident data using `extractincidents()`.
  -  Creates a database using `createdb()`.
  -  Populates the database with the extracted incidents using `populatedb()`.
  -   Prints a summary of incidents by nature using `status()`.
  
- **Returns**: 
  - None.
  
**Example**:  
```python
main("https://www.normanok.gov/sites/default/files/documents/2024-09/2024-09-01_daily_incident_summary.pdf")

```

# Database Development

The project uses SQLite as the database to store the extracted incident data. The database file is created from scratch every time the script runs, ensuring a clean state for every execution.

## Table: `incidents`
- **Columns**:
  - `incident_time` (TEXT): The date and time the incident occurred.
  - `incident_number` (TEXT): A unique identifier for each incident.
  - `incident_location` (TEXT): The location where the incident took place.
  - `nature` (TEXT): The nature or type of the incident (e.g., "Welfare Check", "Traffic Stop").
  - `incident_ori` (TEXT): The originating identifier for the incident (e.g., OK0140200).
  
The database is created with the `createdb()` function, which ensures that the `incidents` table is reinitialized each time the program is executed. This guarantees that each run of the program is independent, allowing fresh data to be inserted and preventing conflicts with previously stored records.

Data is inserted into the `incidents` table using the `populatedb()` function, which accepts a list of incident tuples and commits them to the database.

# Bugs and Assumptions

1. **Empty or Malformed PDFs**:
   - If the program encounters an empty or malformed PDF, it will raise an error during the parsing process. The current implementation of `PyPDF2.PdfFileReader()` does not handle empty or corrupted PDFs, and this would result in a crash.

2. **PDF Format Changes**:
   - The script assumes that the structure of the PDF will always be consistent in terms of how the data (Date/Time, Incident Number, Location, Nature, Incident ORI) is presented. If the structure of the PDF changes (e.g., if fields are rearranged, new fields are introduced, or line breaks change), the extraction logic based on `split()` operations may fail to capture the data correctly.
3. **Incidents Split Across Pages:**:
   - The script assumes that each page contains complete incidents. If an incident is split across two pages (e.g., the first part of the incident is on one page and the second part on the next), the current implementation may fail to capture the entire incident, leading to incomplete records.
4. **Handling Splitting**:
   - The code uses the || marker to identify new incidents based on the date format. If an incident spans multiple lines or pages, this approach may not correctly capture all incidents. Additionally, it assumes that incidents always start with a date, which may not always be the case in a different format.

