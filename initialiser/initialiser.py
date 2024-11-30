import os
import pandas as pd
from openpyxl.reader.excel import load_workbook

from columns import required_columns
from columns import range_columns
from openpyxl.worksheet.datavalidation import DataValidation

class Initialiser:
    def __init__(self, csv_file_path):
        """
        Initialize the Validator object with a CSV file path.

        Args:
            csv_file_path (str): The path to the CSV file to be validated.
        """
        self.csv_file_path: str = csv_file_path
        self.df: pd.DataFrame = None
        self.wb = None
        self.ws = None
        self.wb_name = "DataSheet.xlsx"
        self.ws_name = "Sheet1"

       # Initialise Types


    def readCSV(self):
        """
        Read the CSV file into a Pandas DataFrame, and initialise the Excel workbook and worksheet.
        """
        try:
            # Read the CSV file into a DataFrame
            self.df = pd.read_csv(self.csv_file_path)
            print(f"CSV file '{self.csv_file_path}' read successfully!")

            # try to rename the columns of the DataFrame according to the 'required_columns' mapping
            self.df.rename(columns=required_columns, inplace=True)

            # Save DataFrame to an Excel file
            self.df.to_excel(self.wb_name, sheet_name=self.ws_name, index=False)

            # Load and store the workbook
            self.wb = load_workbook(self.wb_name)

            if self.ws_name not in self.wb.sheetnames:
                raise ValueError(f"Sheet '{self.ws_name}' does not exist in the workbook.")

            self.ws = self.wb[self.ws_name]

        except Exception as e:
            print(f"Error reading CSV file: {e}")

    def applyValidationRules(self):
        """
        Apply data validation rules to an Excel workbook.
        """
        # Custom DV Rule - Range [0, 7]
        # Custom DV Rule - Range [0, 6]

        try:
            # Add the dv rules to the worksheet
            self.ws.add_data_validation(numeric_dv)
            self.ws.add_data_validation(integer_dv)
            self.ws.add_data_validation(date_dv)
            self.ws.add_data_validation(boolean_dv)
            self.ws.add_data_validation(gender_dv)

            # Apply Numeric DV Rule to columns
            numeric_dv.add(range_columns["vs_temperature"])

            # Apply Integer DV Rule to columns
            integer_dv.add(range_columns["id"])
            integer_dv.add(range_columns["vid"])
            integer_dv.add(range_columns["a_age"])

            # Apply Date DV Rule to columns
            date_dv.add(range_columns["a_reg_date"])
            date_dv.add(range_columns["a_dob"])
            date_dv.add(range_columns["a_last_menstrual_period"])

            # Apply Boolean DV Rule to columns
            boolean_dv.add(range_columns["a_pregnant"])
            boolean_dv.add(range_columns["a_sent_to_id"])

            # Apply Gender DV Rule to columns
            gender_dv.add(range_columns["a_gender"])

            self.wb.save(self.wb_name)
            print("Validation rules applied and saved successfully!")

        except Exception as e:
            print(f"Error applying validation rules: {e}")


# Path to patient data csv file
path = "patientdata.csv"  # Replace with your directory path

validator = Initialiser(path)
validator.readCSV()
validator.applyValidationRules()
