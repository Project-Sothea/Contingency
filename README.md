### Overview
Contains utilities used for converting application database data to usable Data Sheets, and for merging Data Sheets to be imported
into the application database.

### `Merger.py`
Merger script that takes a directory of Data Sheets and merges them into a single Data Sheet.
Cannot assume formatting and values of the Data Sheet columns to be correct.

### `Initialiser.py`
Initialiser script that takes a CSV file of the application database and converts it to a usable Data Sheet by drs.
Can assume formatting and values of the CSV file to be correct.
Some things it does include: 
- Renames columns
- Applies xlsx data validation rules
- Formats cells to have dropdowns to select from

### `Importer.py`
Takes a successfully merged Data Sheet and imports it into the application database.

### How to use:
- Converting DB to Data Sheet: (System is down)
    1. Run the Initialiser script with the CSV file of the application database as input, generating a formatted, ready-to-use Data Sheet.
    2. Disseminate the Data Sheet for the various stations to start using (Manually / Network File Sharing system)

- Converting Data Sheet to DB: (System is back up)
    1. Collate all the Data Sheets from the various stations. (Manually / Network File Sharing System)
    2. Merge the Data Sheets into a single Data Sheet using the Merger script.
    3. Import the merged Data Sheet into the application database using the Importer script.

### Files
- patientdata.csv

- DataSheet.xlsx

- types.csv