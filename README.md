### Overview
Contains utilities used for converting application database data to usable Data Sheets, and for merging Data Sheets to be imported
into the application database.

### Installation

We recommend configuring a virtual environment for this project.
1. `cd` to the project root
2. `python3 -m venv venv` / `python3 -m venv venv` 
3. `source venv/bin/activate` / `.\venv\Scripts\activate.bat`
4. In your IDE, configure the Python interpreter to use the virtual environment
5. For initial setup, do `pip install -r requirements.txt`

You can configure the database connection parameters in `columns.py`

### `Initialiser.py`
Initialiser script that takes a CSV file of the application database and converts it to a usable Data Sheet by drs.
Can assume formatting and values of the CSV file to be correct.
Some things it does include:
- Renames columns
- Applies xlsx data validation rules
- Formats cells to have dropdowns to select from
 
### `Merger.py`
Merger script that takes a directory of Data Sheets and merges them into a single Data Sheet.

If a DataSheet has duplicate rows, the script will arbitrarily choose one of the rows, and discard the other one.
It will log the DataSheets with duplicates for further checking later on.

If multiple DataSheets have overlapping rows filled out for a patient, the script will arbitrarily keep one.

### `Importer.py`
Takes a successfully merged Data Sheet and imports it into the application database.

### How to use:
Ensure that types.csv is in the project, and up-to-date.

### Configuring columns.py
Fill out the columns.py file with the correct parameters for the database.

Initially when the system is working:
Cron Job:
1. While the biometrics system is up, run /cron/backup.py, to grab csv backups of the database every minute.
2. Periodically check the run logs to ensure that the backups are working
3. You can also make sure the webserver is running in advance.

Converting DB to Data Sheet: (System is down)
1. Run the Initialiser.py script, which pulls the latest backup csv from /cron/backups, and converts it to DataSheet.xlsx. 
2. Place the DataSheet.xlsx in the /server/uploads folder for the stations to use.
3. Navigate to /server/, and start up the webserver with `python app.py`, so that users can download the DataSheet.xlsx file to use. 
   - If the server is down, share the DataSheet.xlsx file using thumbdrives

Converting Data Sheet to DB: (System is back up)
1. Ensure the system is back up.
2. Navigate to /server/, and start up the webserver with `python app.py`, so that users can upload their DataSheet.xlsx files.
   - If the server is down, collect the DataSheet.xlsx files using thumbdrives, then place them in the /server/uploads folder. Naming shouldn't matter.
3. Run Merger.py, merge the DataSheets into a single merged_output.csv file.
4. Go to PgAdmin, and run the following SQL command to clear the database:
```sql
TRUNCATE TABLE admin CASCADE;
```
4. Run Importer.py to import the merged_output.csv file into the database.

### To Do:
- Test backup_script.bat works on another machine
- Make script work from another machine over a network
- Merger: Gets uploaded DataSheet.xlsx files from /server/uploads, merges them and saves to /merger/merged folder
- Importer: Gets merged DataSheet.xlsx files from /merger/merged, imports them into the database

- BUG: Type coercion for columns after concatenation in merger.py causes numeric values to become floats. doesn't seem to affect ability to import yett
 
### CAUTION
- In order to prevent accidentally running the script and resetting the database, the script will only work if the existing tables are cleared.
- To clear the database, enter the Query Editor in pgAdmin and run the following SQL command manually:
```sql
TRUNCATE TABLE admin CASCADE;
```