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

Watch the demo [here](https://drive.google.com/file/d/1KlixiBupG-qc0pLOrtsK8WzuEwomaoKb/view?usp=sharing).

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
# extractincidents(pdf_data)
- **Parameters**: 
  - `pdf_data`: A byte stream representing the downloaded PDF content.
- **Process**: 
  - This function processes the PDF data:
    - Reads the PDF using `PdfReader`.
    - Extracts text from each page.
    - Parses the text using `parse_incident_data()` to extract relevant incident fields (date/time, incident number, location, nature, and ORI).
  - Returns a list of incidents.
- **Returns**: 
  - A list of tuples, where each tuple represents an incident with its fields: `(incident_time, incident_number, location, nature, incident_ori)`.
    
**Example**:  
```python
incidents = extractincidents(pdf_data)

```
# parse_incident_data(text)
- **Parameters**: 
  - `text`: A string representing the extracted text from a PDF page.
- **Process**: 
  - Uses a regular expression to identify and extract incident data from the text.
  - It captures fields like incident time, number, location, nature, and ORI.
  - Handles edge cases like "911 Call Nature" and unknown data.
- **Returns**: 
  - A list of tuples representing the parsed incidents.
- **Process**:  
  -  The regular expression used in the project is:
    ```regex
    (\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) (\d{4}-\d{8}) ((?:[A-Z0-9 /]+(?:DR|AVE|NE|RR|P|PL|ST|SW|BLVD|CIR|PKWY|RD|HWY|CT|SE|NW|RAMP|LN|BOARDWALK|WAY|GRN|OK-9|TER|SB I|AV|LN|UNIT 1201|Interstate|SQ|CT|CITY|Robinson|STREET|NB I|- GOLDSBY)|[0-9.-]+;[0-9.-]+)) (.+?) (OK\d{6}|EMSSTAT|14005|14009)
  
Uses a regular expression to identify and extract incident data from the text.
- Date/Time: (\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}) – a standard date/time format.
- Incident Number: (\d{4}-\d{8}) – an incident number in the format of 4 digits followed by 8 digits.
- Location: ((?:[A-Z0-9 /]+...)) – a location that may include street names and ends with suffixes like DR, AVE, ST, etc., or lat/long coordinates.
- Nature: (.+?) – captures the nature of the incident, which can be multiple words.
- ORI: (OK\d{6}|EMSSTAT|14005|14009) – captures the ORI code.


**Example**:  
```python
 parsed_incidents = parse_incident_data(text)

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
# populatedb(db, incidents)
- **Parameters**: 
  - `db`: An SQLite database connection object.
  - `incidents`: A list of incident tuples `(incident_time, incident_number, location, nature, incident_ori)`.
- **Process**: 
  - Inserts the list of incidents into the SQLite database's `incidents` table.
  - Commits the transaction to save the data.
- **Returns**: 
  - None.

**Example**:  
```python
populatedb(db, incidents)

```
# status(db)
- **Parameters**: 
  - `db`: An SQLite database connection object.
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

## Known Bugs:
1. **Empty PDFs**:
   - If the program encounters an empty or malformed PDF file, it will crash due to a lack of error handling for such cases. The `pypdf` library throws exceptions when it cannot read valid PDF data, which is not currently caught in the script. Adding exception handling for empty PDFs and displaying a user-friendly message would be a proper fix for this issue.

2. **Incomplete Incidents**:
   - If an incident is split across lines or incomplete in the PDF, the regular expression parser might fail to capture all the necessary fields, leading to missing or incorrect data. This is due to inconsistent formatting of data in the PDF.
2. **Incidents Split Across Pages:**:
   - Another related issue is when incident data is split across pages in the PDF. The current extraction logic assumes each page is self-contained, which can cause issues if an incident begins on one page and finishes on another. To handle this correctly, the code would need to combine data from multiple pages.

## Assumptions:
1. **Location Field Suffixes**:
   - The assumption in the current implementation is that the location field will end with certain well-known suffixes like `DR`, `AVE`, `ST`, etc., or `latitude/longitude coordinates (e.g., 35.2050366666667;-97.421115)`. These patterns have been identified from the provided PDFs. If new PDFs introduce new suffixes or formats, the regular expression may fail, and further adjustments would be necessary to ensure accurate extraction.

2. **Checked PDFs**:
   - The project has been tested on a handful of incident PDFs from the Norman, Oklahoma police department, and the location suffixes generally match the ones listed in the regular expression. However, this may not be comprehensive. If future PDFs introduce new or previously unseen formats, the regular expression may need to be updated.

3. **Consistent Formatting**:
   - This project assumes that the incidents in the PDF files follow a consistent format, including the structure of the date/time, incident number, location, nature, and ORI. If the police department changes its PDF formatting or alters the structure of its reports, the current regular expression extraction logic might not work as expected and would require modification.

4. **Incident Nature Edge Cases**:
   - The code includes special handling for natures like "911 Call Nature Unknown". The assumption here is that other edge cases might occur, but for now, the script explicitly handles some of the more common ones. Additional edge cases will need to be addressed as they are encountered.

