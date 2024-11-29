# MERGE DATA SHEETS
import os
import pandas as pd
from columns import required_columns

"""
Merge XLSX files in the specified directory on 'id' and 'vid' columns.
"""

class Merger:
    def __init__(self, directory):
        """
        Initialize the Merger object with the directory containing XLSX / CSV files.

        Args:
            directory (str): Path to the directory containing the XLSX / CSV files.
        """
        self.directory = directory
        self.dataframes = self.readDataSheets()

    def readDataSheets(self) -> list:
        """
        Read all XLSX / CSV files in the specified directory.

        Returns:
            dataframes (list): List of dataframes read from XLSX / CSV files.
        """
        # List to store dataframes
        dataframes = []

        for file in os.listdir(self.directory):
            if file.endswith(".csv") or file.endswith(".xlsx"):
                file_path = os.path.join(self.directory, file)
                print(f"Reading file: {file_path}")

                try:
                    if file.endswith(".csv"):
                        df = pd.read_csv(file_path)
                    elif file.endswith(".xlsx"):
                        df = pd.read_excel(file_path)

                    # Validate columns
                    if len(df.columns) == len(required_columns) and 'id' in df.columns and 'vid' in df.columns:
                        dataframes.append(df)
                    else:
                        print(f"Skipping file {file}: Missing 'id' or 'vid' columns / Unequal number of columns")
                except Exception as e:
                    print(f"Error reading file {file}: {e}")

        return dataframes

    def mergeDataSheets(self, output_file="merged_output.csv"):
        """
        Merge CSV files in the specified directory on 'id' and 'vid' columns.

        Args:
            output_file (str): Name of the output file to save the merged dataframe.
        """
        # List to store dataframes
        dataframes = []

        # Loop through all files in the directory
        for file in os.listdir(self.directory):
            if file.endswith(".csv"):
                file_path = os.path.join(self.directory, file)
                print(f"Reading file: {file_path}")
                df = pd.read_csv(file_path)

                # Ensure required columns exist
                if 'id' in df.columns and 'vid' in df.columns:
                    dataframes.append(df)
                else:
                    print(f"Skipping file {file}: Missing 'id' or 'vid' columns")

        # Merge all dataframes on 'id' and 'vid'
        if dataframes:
            # Concatenate dataframes
            merged_df = pd.concat(dataframes, ignore_index=True)
            # Group by 'id' and 'vid' and aggregate to merge rows
            merged_df = merged_df.groupby(['id', 'vid'], as_index=False).first()

            # Save the merged dataframe to a new CSV file
            merged_df.to_csv(output_file, index=False)
            print(f"Merged file saved as: {output_file}")
        else:
            print("No valid files to merge.")


# Directory containing the CSV files
directory = "simple/"  # Replace with your directory path

merger = Merger(directory)
merger.mergeDataSheets()