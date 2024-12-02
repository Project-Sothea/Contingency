# Maps CSV cols to Data Sheet cols
from enum import Enum
from typing import List, Optional
from openpyxl.worksheet.datavalidation import DataValidation
import csv

class DataType(Enum):
    def __new__(cls, sql_type, validation: Optional[DataValidation] = None):
        obj = object.__new__(cls)
        obj._value_ = sql_type
        obj.validation = validation
        return obj

    # DataType definitions with associated DataValidation rules
    INTEGER = (
        "INTEGER",
        DataValidation(
            type="whole",
            operator="between",
            formula1="-9999",
            formula2="9999",
            showErrorMessage=True,
            error="Entry must be a whole number between -9999 and 9999",
            errorTitle="Invalid Entry",
        ),
    )
    TEXT = ("TEXT")
    VARCHAR_1 = (
        "VARCHAR(1)",
        DataValidation(
            type="textLength",  # Ensures the length of the text
            operator="equal",
            formula1="1",  # Text must be exactly 1 character
            showErrorMessage=True,
            error="Entry must be a single character",
            errorTitle="Invalid Entry",
        ),
    )
    BOOLEAN = (
        "BOOLEAN",
        DataValidation(
            type="list",
            formula1='"TRUE,FALSE"',
            showErrorMessage=True,
            error="Entry must be either 'TRUE' or 'FALSE'",
            errorTitle="Invalid Entry",
        ),
    )
    DATE = (
        "DATE",
        DataValidation(
            type="date",
            showErrorMessage=True,
            error="Entry must be a valid date",
            errorTitle="Invalid Entry",
        ),
    )
    NUMERIC_5_1 = (
        "NUMERIC(5, 1)",
        DataValidation(
            type="decimal",
            operator="between",
            formula1="-9999.9",
            formula2="9999.9",
            showErrorMessage=True,
            error="Entry must be a number between -9999.9 and 9999.9",
            errorTitle="Invalid Entry",
        ),
    )
    BYTEA = ("BYTEA")


class FieldDescriptor:
    """
    Describes a field
    """

    def __init__(self, sql_name: str, go_name: str, json_name: str, datasheet_name: str, csv_name: str,
                 datatype: DataType, colour: str, required: bool = False, datasheet_range: str = None):
        self.sql_name: str = sql_name                   # SQL column name
        self.go_name: str = go_name                     # Go struct field name
        self.json_name: str = json_name                 # JSON field name
        self.datasheet_name: str = datasheet_name       # DataSheet column name
        self.csv_name: str = csv_name                   # CSV column name in patientdata.csv
        self.datatype: DataType = datatype              # Data type of the field (Loosely follows SQL type)
        self.colour: str = colour                       # Column colour
        self.required: bool = required                  # Whether the field is required
        self.datasheet_range: str = datasheet_range     # Range of the column in the datasheet

    def __repr__(self):
        return self.sql_name


class CategoryDescriptor:
    """
    Describes a Category
    """

    def __init__(self, name: str, fields: list):
        self.name: str = name
        self.fields: List[FieldDescriptor] = fields  # fields is expected to be a list of Field objects

    def __repr__(self):
        return self.name


class Types:
    def __init__(self, csv_path: str):
        self.categories: List[CategoryDescriptor] = []  # An array of CategoryDescriptor objects
        self._load_from_csv(csv_path)

    def _load_from_csv(self, csv_path: str):
        # Dictionary to store category-to-fields mapping
        category_map = {}

        with open(csv_path, mode="r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Extract data for the field
                category = row["Category Dropdown"]
                sql_name = row["SQL Name"]
                go_name = row["Go Name"]
                json_name = row["JSON Name"]
                datasheet_name = row["Datasheet Name"]
                csv_name = row["CSV Name"]
                datatype = row["Data Type"]
                required = row["Required"].strip().upper() == "TRUE"
                datasheet_range = row["Datasheet Range"]
                colour = row["Colour"]

                # Create a FieldDescriptor
                field = FieldDescriptor(
                    sql_name=sql_name,
                    go_name=go_name,
                    json_name=json_name,
                    datasheet_name=datasheet_name,
                    csv_name=csv_name,
                    datatype=DataType[datatype],
                    required=required,
                    datasheet_range=datasheet_range,
                    colour=colour
                )

                # Add the field to the appropriate category
                # Create new category if it doesn't exist
                if category not in category_map:
                    category_map[category] = []
                category_map[category].append(field)

        # Convert category_map to CategoryDescriptors
        for category, fields in category_map.items():
            self.categories.append(CategoryDescriptor(name=category, fields=fields))

    def __repr__(self):
        return f"Types(categories={self.categories})"


if __name__ == "__main__":
    types = Types("types.csv")

    # Print header with increased padding
    print(f"{'Category':<25} {'Field':<30} {'DataType':<25} {'Required':<10}")
    print("=" * 90)

    for category in types.categories:
        for field in category.fields:
            print(f"{category.name:<25} {field.sql_name:<30} {field.datatype:<25} {str(field.required):<10}")
