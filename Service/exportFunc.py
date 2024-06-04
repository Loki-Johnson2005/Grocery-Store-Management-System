import csv
from pathlib import Path


def export_data_to_spreadsheet(s_name, s_location, s_type, s_capacity, s_status, s_water_level):
    # Define the headings for the spreadsheet
    headings = ["Name", "Location", "Type", "Capacity", "Status", "Water Level"]

    # Create a list of data values
    data = {s_name, s_location, s_type, s_capacity, s_status, s_water_level}

    # Get the path to the user's Documents folder
    documents_path = Path.home() / "Documents"

    # Create the export directory if it doesn't exist
    export_directory = documents_path / "export_directory"
    export_directory.mkdir(parents=True, exist_ok=True)

    # Create a filename for the export file
    filename = export_directory / "exported.csv"

    # Write the data to a CSV file
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headings)
        writer.writerow(data)

    # Print a success message
    print("Data exported to spreadsheet successfully.")
