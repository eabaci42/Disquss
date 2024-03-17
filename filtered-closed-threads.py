import csv
import sys

def filter_closed_threads(input_csv_path, output_csv_path='closed-threads.csv'):
    """
    This function reads a CSV file, filters out the entries with status 'Closed', 
    and writes them to a new CSV file.
    
    :param input_csv_path: Path to the input CSV file.
    :param output_csv_path: Path to the output CSV file for 'Closed' entries.
    """
    # Initialize a list to hold the filtered 'Closed' entries.
    closed_entries = []

    # Read the CSV file and filter the data.
    with open(input_csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # Go through each row and check the status.
        for row in reader:
            if row['Status'].strip().lower() == 'closed':
                closed_entries.append(row)

    # Write the 'Closed' entries to the output CSV file.
    if closed_entries:  # Check if there's any closed entry
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=closed_entries[0].keys())
            writer.writeheader()
            writer.writerows(closed_entries)
    
    return output_csv_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python filter_closed_threads.py <input_csv_path>")
        sys.exit(1)
    
    input_csv_path = sys.argv[1]
    output_csv_path = 'closed-threads.csv'
    
    print(f"Filtering 'Closed' entries from {input_csv_path} and writing them to {output_csv_path}...")
    filter_closed_threads(input_csv_path, output_csv_path)
    print("Done.")

if __name__ == "__main__":
    main()
    