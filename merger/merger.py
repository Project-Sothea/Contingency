import os

import sys

# Add the parent directory of 'columns' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import pandas as pd
import columns
from columns import Types

"""
Merge DataSheet.xlsx files in the specified directory on a set of columns (id, vid)
Have a log to indicate files that 
"""


class Merger:
    def __init__(self, uploads_directory_file_path: str, types_file_path: str, merge_cols=None):
        """
        Initialize the Merger object with the directory containing XLSX / CSV files.

        Args:
            directory (str): Path to the directory containing the XLSX / CSV files.
        """
        self.types: columns.Types = None
        self.directory = uploads_directory_file_path
        self.types_file_path: str = types_file_path
        self.dataframes: list[pd.DataFrame] = []
        self.df: pd.DataFrame = None
        self.merge_cols: list[str] = merge_cols if merge_cols is not None else [] # String value of columns to merge on

    def initialise(self):
        """
        Do necessary initialisations for the Merger class
        Initialise the 'Types' object with the types CSV file.
        """
        try:
            self.types = Types(self.types_file_path)
            print(f"Types '{self.types_file_path}' read successfully!")
        except Exception as e:
            print(f"Error reading types file '{self.types_file_path}': {e}")

    def readDataSheets(self):
        """
        Read all XLSX / CSV files in the specified directory and check for issues.

        Returns:
            dataframes (list): List of dataframes read from XLSX / CSV files.
        """
        # List to store dataframes
        dataframes = []

        # Initialize a list to keep track of files/columns with issues
        problems = []

        # Generate a list of valid datasheet column names from self.categories
        valid_columns = set()
        for category in self.types.categories:
            for field in category.fields:
                valid_columns.add(field.datasheet_name)

        for file in os.listdir(self.directory):
            if file.endswith(".csv") or file.endswith(".xlsx"):
                file_path = os.path.join(self.directory, file)
                print(f"Reading file: {file_path}")

                try:
                    if file.endswith(".csv"):
                        df = pd.read_csv(file_path)
                    elif file.endswith("DataSheet.xlsx"):
                        df = pd.read_excel(file_path)

                    # Check for columns that don't match the expected datasheet names
                    columns_in_file = set(df.columns)
                    invalid_columns = columns_in_file - valid_columns
                    missing_columns = valid_columns - columns_in_file

                    # If there are any mismatches, log them but skip adding the dataframe
                    if invalid_columns or missing_columns:
                        problems.append({
                            "file": file,
                            "invalid_columns": list(invalid_columns),
                            "missing_columns": list(missing_columns)
                        })
                        print(f"Skipping file {file} due to column mismatches.")
                        continue  # Skip adding this dataframe to the list

                    # Check for duplicate Registration ID and Visit ID
                    if {'Registration ID*', 'Visit ID*'}.issubset(df.columns):
                        duplicates = df[df.duplicated(subset=['Registration ID*', 'Visit ID*'], keep=False)]
                        if not duplicates.empty:
                            problems.append({
                                "file": file,
                                "duplicates": duplicates[['Registration ID*', 'Visit ID*']].to_dict(orient='records')
                            })
                            print(f"File {file} has duplicate Registration ID and Visit ID entries.")
                            # Log the duplicates but still add the dataframe

                    # Add the dataframe to the list
                    dataframes.append(df)

                except Exception as e:
                    print(f"Error reading file {file}: {e}")

        # Print problems if there are any
        if problems:
            print("Validation issues found:")
            for problem in problems:
                print(f"File: {problem.get('file')}")
                if "invalid_columns" in problem:
                    print(f"  Invalid columns: {', '.join(problem['invalid_columns'])}")
                if "missing_columns" in problem:
                    print(f"  Missing columns: {', '.join(problem['missing_columns'])}")
                if "duplicates" in problem:
                    print("  Duplicate Registration ID and Visit ID entries:")
                    for duplicate in problem['duplicates']:
                        print(f"    {duplicate}")
        else:
            print("All files have valid columns and no duplicate IDs.")

        # Store the dataframes in the class
        self.dataframes = dataframes

    def mergeDataSheets(self, output_file="merged_output.csv"):
        """
        Merge read dataframes on 'id' and 'vid' columns.

        Args:
            output_file (str): Name of the output file to save the merged dataframe.
        """
        # Merge all dataframes on 'id' and 'vid'
        if self.dataframes:
            # For every dataframe, rename its columns
            self.renameColumns()

            # Set column types before pd concat
            self.setColumntypes()

            # Concatenate dataframes
            self.df = pd.concat(self.dataframes, ignore_index=True)

            # Rename columns based on the types
            self.renameColumns()

            # Group by 'id' and 'vid' and aggregate to merge rows
            self.df = self.df.groupby(self.merge_cols, as_index=False).first()

            # Save the merged dataframe to a new CSV file
            self.df.to_csv(output_file, index=False)
            print(f"Merged file saved as: {output_file}")
        else:
            print("No valid files to merge.")

    def renameColumns(self):
        """
        Renames the columns of the existing DataFrame based on a datasheet_name to csv_name mapping.

        Raises:
            ValueError: If self.types or self.df is not initialized.
        """
        # Check if self.types and self.df are initialized
        if self.types is None:
            raise ValueError(
                "The 'types' object is not initialized. Please initialize 'self.types' before renaming columns.")
        if self.dataframes is None:
            raise ValueError(
                "The DataFrame 'self.df' is not initialized. Please load data into 'self.df' before renaming columns.")

        # Generate a mapping from datasheet_name to csv_name
        datasheet_to_csv_map = {}
        for category in self.types.categories:
            for field in category.fields:
                datasheet_to_csv_map[field.datasheet_name] = field.csv_name

        # Rename the columns for each dataframe in self.dataframes
        for dataframe in self.dataframes:
            dataframe.rename(columns=datasheet_to_csv_map, inplace=True)

    def setColumntypes(self):
        """
        Set the appropriate data type for each csv-named column based on non-NaN values for each dataframe in self.dataframes.
        """
        if not self.dataframes:
            raise ValueError(
                "The 'dataframes' list is empty or not initialized. Please load data into 'self.dataframes' before "
                "setting column types.")

        for df in self.dataframes:
            for category in self.types.categories:
                for field in category.fields:
                    # Check if the field's CSV name is present in the dataframe columns
                    if field.csv_name in df.columns:
                        # Assign the correct dtype based on the field's DataType
                        if field.datatype == columns.DataType.INTEGER:
                            df[field.csv_name] = df[field.csv_name].astype('Int64')  # Integer type (nullable)
                        elif field.datatype == columns.DataType.TEXT:
                            df[field.csv_name] = df[field.csv_name].astype('string')
                        elif field.datatype == columns.DataType.NUMERIC_5_1:
                            df[field.csv_name] = pd.to_numeric(df[field.csv_name], errors='coerce')


if __name__ == "__main__":
    # Directory containing the CSV files
    uploads_directory_file_path = "../server/uploads/"  # Replace with your directory path
    types_file_path = "../types.csv"                    # Replace with path to types.csv

    merger = Merger(uploads_directory_file_path, types_file_path, ["id", "vid"])
    merger.initialise()
    merger.readDataSheets()
    merger.mergeDataSheets()
