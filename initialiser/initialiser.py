import os
import pandas as pd
from openpyxl.reader.excel import load_workbook

import columns
from columns import required_columns, Types
from columns import DataType
from openpyxl.worksheet.datavalidation import DataValidation

class Initialiser:
    def __init__(self, patientdata_file_path, types_file_path):
        """
        Initialize the Validator object with a CSV file path.

        Args:
            csv_file_path (str): The path to the CSV file to be validated.
        """
        self.csv_file_path: str = patientdata_file_path
        self.types_file_path: str = types_file_path
        self.df: pd.DataFrame = None
        self.wb = None
        self.ws = None
        self.wb_name = "DataSheet.xlsx"
        self.ws_name = "Sheet1"
        self.types: columns.Types

    def readCSV(self):
        """
        Read the CSV file into a Pandas DataFrame, and initialise the Excel workbook and worksheet.
        """
        try:
            # Initialise Types
            self.types = Types(self.types_file_path)
            print(f"Types '{self.types_file_path}' read successfully!")

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
            print(f"Error reading CSV file / Initialising Types: {e}")

    def applyValidationRules(self):
        """
        Apply data validation rules to an Excel workbook.
        """
        # Custom DV Rule - Range [0, 7]
        # Custom DV Rule - Range [0, 6]

        try:
            # Add the dv rules listed in DataType enums to the worksheet
            for dt in DataType:
                if dt.validation != None:
                    self.ws.add_data_validation(dt.validation)

            # for each category in types, for each field in the category, apply the validation rule to its datasheet range
            for category in self.types.categories:
                for field in category.fields:
                    if field.datatype.validation != None:
                        field.datatype.validation.add(field.datasheet_range)

            self.wb.save(self.wb_name)
            print("Validation rules applied and saved successfully!")

        except Exception as e:
            print(f"Error applying validation rules: {e}")

    def applyFormatting(self):
        pass


if __name__ == "__main__":
    # Path to patient data csv file
    patientdata_file_path = "patientdata.csv"  # Replace with your directory path
    types_file_path = "types.csv"

    validator = Initialiser(patientdata_file_path, types_file_path)
    validator.readCSV()
    validator.applyValidationRules()
