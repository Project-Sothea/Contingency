import os

import pandas as pd
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill, Side, Border, Alignment

import columns
from columns import required_columns, Types
from columns import DataType

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
        """
        Apply formatting rules to an Excel workbook.
        - Applies a border to all cells
        - Colours cells according to their category
        - Resizes column width to fit the content.
        - First Row: Triples height, centres text
        - Pins the first 3 columns
        - Adds dropdowns if necessary
        """

        # Apply border to all cells
        border_style = Border(
            left=Side(border_style="thin", color="000000"),
            right=Side(border_style="thin", color="000000"),
            top=Side(border_style="thin", color="000000"),
            bottom=Side(border_style="thin", color="000000")
        )

        for row in self.ws.iter_rows(min_row=1, max_row=self.ws.max_row, min_col=1, max_col=self.ws.max_column):
            for cell in row:
                cell.border = border_style
        print("Borders applied successfully!")

        # Colours cells according to their category
        for category in self.types.categories:
            for field in category.fields:
                custom_fill = PatternFill(start_color=field.colour, end_color=field.colour, fill_type="solid")
                start_cell, end_cell = field.datasheet_range.split(":")
                start_column = ''.join(filter(str.isalpha, start_cell))
                range_cells = self.ws[f"{start_cell}:{start_column}{self.ws.max_row}"]
                for row in range_cells:
                    for cell in row:
                        cell.fill = custom_fill
        print("Cell colours applied successfully!")

        # Resizes column width and height to fit the content
        for col in self.ws.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
            adjusted_width = (max_length + 2)
            self.ws.column_dimensions[column].width = adjusted_width

            # Apply text wrapping to all cells in the first row
            for cell in self.ws[1]:  # Loop through each cell in the first row
                cell.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")


        self.wb.save(self.wb_name)
        print("Formatting applied and saved successfully!")


if __name__ == "__main__":
    # Path to patient data csv file
    patientdata_file_path = "patientdata.csv"  # Replace with your directory path
    types_file_path = "types.csv"

    # delete the existing DataSheet.xlsx file
    try:
        os.remove("DataSheet.xlsx")
    except:
        pass

    initialiser = Initialiser(patientdata_file_path, types_file_path)
    initialiser.readCSV()
    initialiser.applyValidationRules()
    initialiser.applyFormatting()
