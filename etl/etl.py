import csv
import json
import logging
import os
from .transformers import Transformer

class ETL:
    def __init__(self, config_path):
        # Load the configuration file
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        # Initialize the transformer with the loaded transformations
        self.transformer = Transformer(self.config['transformations'])
    
    def process_file(self, input_path, output_path):
        error_file_path = 'data/output_error.csv'

        # Delete the error file if it exists to ensure a clean slate
        if os.path.exists(error_file_path):
            os.remove(error_file_path)
        
        error_writer = None
        errorfile = None

        # Read the input CSV file
        with open(input_path, 'r') as infile:
            reader = csv.DictReader(infile)
            rows = [row for row in reader]

        # Transform the rows using the transformer
        transformed_rows = self.transformer.transform(rows)

        # Open the output file for writing the transformed rows
        with open(output_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=transformed_rows[0].keys())
            writer.writeheader()
            for row in transformed_rows:
                try:
                    # Write each transformed row to the output file
                    writer.writerow(row)
                except Exception as e:
                    logging.error(f"Error writing row: {e}")
                    # Open the error file if an error occurs and it hasn't been opened yet
                    if not error_writer:
                        errorfile = open(error_file_path, 'w', newline='')
                        error_writer = csv.DictWriter(errorfile, fieldnames=row.keys())
                        error_writer.writeheader()
                    # Write the erroneous row to the error file
                    error_writer.writerow(row)


# Configure logging to log errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
