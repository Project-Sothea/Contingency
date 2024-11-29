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

    def readCSV(self):
        """
        Read the CSV file into a Pandas DataFrame
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
        # DV Rule - NUMERIC(5, 1)
        numeric_dv = DataValidation(type="decimal", operator="between", formula1="-9999.9", formula2="9999.9",
                                    showErrorMessage=True)
        numeric_dv.error = "Entry must be a number between -9999.9 and 9999.9"
        numeric_dv.errorTitle = "Invalid Entry"

        # DV Rule - INTEGER
        integer_dv = DataValidation(type="whole", operator="between", formula1="-9999", formula2="9999",
                                    showErrorMessage=True)
        integer_dv.error = "Entry must be a whole number between -9999 and 9999"
        integer_dv.errorTitle = "Invalid Entry"

        # DV Rule - DATE
        date_dv = DataValidation(type="date", showErrorMessage=True)
        date_dv.error = "Entry must be a valid date"
        date_dv.errorTitle = "Invalid Entry"

        # DV Rule - BOOLEAN
        boolean_dv = DataValidation(type="list", formula1='"TRUE,FALSE"', showErrorMessage=True)
        boolean_dv.error = "Entry must be either 'TRUE' or 'FALSE'"
        boolean_dv.errorTitle = "Invalid Entry"

        # DV Rule - VARCHAR(1) M/F
        gender_dv = DataValidation(type="list", formula1='"M,F"', showErrorMessage=True)
        gender_dv.error = "Entry must be a either M/F"
        gender_dv.errorTitle = "Invalid Entry"
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
