import os

import pandas as pd
from sqlalchemy.orm import sessionmaker

from columns import Types
from sqlalchemy import create_engine
from columns import DATABASE


class Importer:
    def __init__(self, types_file_path: str, csv_file_path: str, database_name: str, host_name: str, user_name: str, password: str, port_number: int):
        self.types_file_path: str = types_file_path
        self.csv_file_path: str = csv_file_path

        self.database_name = database_name
        self.host_name = host_name
        self.user_name = user_name
        self.password = password
        self.port_number = port_number
        self.engine = None
        self.session = None

        self.types: Types = None
        self.df: pd.DataFrame = None

    def initialise(self):
        try:
            self.types = Types(self.types_file_path)
            print(f"Types file '{self.types_file_path}' read successfully!")
        except Exception as e:
            print(f"Error reading types file: {e}")

        try:
            connection_string = f'postgresql+psycopg2://{self.user_name}:{self.password}@{self.host_name}:{self.port_number}/{self.database_name}'
            self.engine = create_engine(connection_string)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print(connection_string)
            print("Database connection established.")
            print("Database session established.")
        except Exception as e:
            print("Database connection failed.")
            print(f"Error details: {e}")

    def readCSV(self):
        """
        Read a CSV file and return the dataframe.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            df (pd.DataFrame): Dataframe containing the CSV data.
        """
        try:
            self.df = pd.read_csv(self.csv_file_path)
        except Exception as e:
            print(f"Error reading CSV file '{self.csv_file_path}': {e}")
            return None

    def removeNullRows(self, df: pd.DataFrame, columns_to_keep: list) -> pd.DataFrame:
        non_keep_columns = [col for col in df.columns if col not in columns_to_keep]
        return df[~df[non_keep_columns].isna().all(axis=1)]

    def processTable(self, df: pd.DataFrame, schema: dict, table_name: str) -> pd.DataFrame:
        # Select the relevant columns and rename them
        subset_df = df[list(schema.keys())].rename(columns=schema, inplace=False)
        # Remove rows that are entirely null except for the id and vid columns
        subset_df = self.removeNullRows(subset_df, ['id', 'vid'])
        return subset_df

    def writeToDatabase(self, df: pd.DataFrame, table_name: str) -> None:
        """
        Write DataFrame to database using SQLAlchemy session.

        :param df: DataFrame to write
        :param table_name: Name of the table
        :param session: SQLAlchemy session
        """
        try:
            # Use pandas to_sql method with if_exists='append'
            df.to_sql(table_name, self.session.bind, if_exists='append', index=False)
            print(f"Data for table '{table_name}' has been written to the database.")
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(f"Error writing to table '{table_name}': {e}")

    def importToDatabase(self):
        """
        Import the CSV data to the database.
        """
        # Reorder categories to ensure 'admin' comes first
        self.types.categories.sort(key=lambda c: c.name != "admin")

        for category in self.types.categories:
            category_csv_sql_map = self.types.csv_sql_map[category.name]
            try:
                subset_df = self.processTable(self.df, category_csv_sql_map, category.name)

                # Write to the database
                # CATEGORY NAME IS CASE SENSITIVE (MUST BE ALL LOWERCASE)
                self.writeToDatabase(subset_df, category.name)
            except Exception as e:
                print(f"Error writing to the database: {e}")

if __name__ == "__main__":
    types_file_path = "../types.csv"
    csv_file_path = "../merger/merged_output.csv"
    database_name = DATABASE["database_name"]
    host_name = DATABASE["host_name"]
    user_name = DATABASE["user_name"]
    password = DATABASE["password"]
    port_number = DATABASE["port_number"]
    importer = Importer(types_file_path, csv_file_path, database_name, host_name, user_name, password, port_number)
    importer.initialise()
    importer.readCSV()
    importer.importToDatabase()


