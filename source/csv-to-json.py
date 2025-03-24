"""
CSV to JSON Converter for ACS Table Rendering Tester
----------------------------------------------------

INSTRUCTIONS FOR USE:
1. Place your CSV input file (e.g., "test_cases.csv") in the same directory as this script.
2. Update the `csv_filename` and `json_filename` variables below with your file names.
3. Run this script using Python: `python csv-to-json.py`
4. The script will create a JSON file with the same data structure as the CSV.

EXPECTED CSV FORMAT:
Each row in the CSV should contain the following columns:
- dataYear: The ACS data year (e.g., 2023)
- dataset: Either "acs1" or "acs5"
- tableGroup: The table group ID (e.g., B01001)
- geographyID: The formatted geography identifier (e.g., 050XX00US18039)

OUTPUT:
The generated JSON file will contain an array of objects, where each object corresponds to a row in the CSV.

EXAMPLE CSV:
dataYear,dataset,tableGroup,geographyID
2023,acs1,B01001,050XX00US18039
2023,acs1,DP02,160XX00US0410670
2023,acs5,S0101,010XX00US

EXAMPLE OUTPUT JSON:
[
    {"dataYear": "2023", "dataset": "acs1", "tableGroup": "B01001", "geographyID": "050XX00US18039"},
    {"dataYear": "2023", "dataset": "acs1", "tableGroup": "DP02", "geographyID": "160XX00US0410670"},
    {"dataYear": "2023", "dataset": "acs5", "tableGroup": "S0101", "geographyID": "010XX00US"}
]
"""

import csv
import json

# Set input CSV file and output JSON file names
csv_filename = "test-cases.csv"  # Change this if your CSV has a different name
json_filename = "test-cases.json"  # Change this to rename the output JSON file

def csv_to_json(csv_filename, json_filename):
    """
    Reads a CSV file and converts it into a JSON file.

    - Opens the CSV file for reading.
    - Reads each row and stores it as a dictionary.
    - Converts the list of dictionaries into a JSON array.
    - Writes the JSON output to a file.
    """

    # Open the CSV file for reading
    try:
        with open(csv_filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Reads CSV into a list of dictionaries
            data = [row for row in reader]  # Convert the reader object to a list

            if not data:
                print("❌ Error: The CSV file is empty. Please provide valid data.")
                return

    except FileNotFoundError:
        print(f"❌ Error: The file '{csv_filename}' was not found. Make sure it exists in the same directory.")
        return
    except Exception as e:
        print(f"❌ Error reading the CSV file: {e}")
        return

    # Open the JSON file for writing
    try:
        with open(json_filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)  # Convert list of dicts to JSON format
            print(f"✅ JSON file '{json_filename}' created successfully!")

    except Exception as e:
        print(f"❌ Error writing the JSON file: {e}")

# Run the conversion function
if __name__ == "__main__":
    csv_to_json(csv_filename, json_filename)
