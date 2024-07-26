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
    
    def process_file(self, input_path, output_path, chunk_size=1000000):
        error_file_path = 'data/output_error.csv'

        # Delete the error file if it exists to ensure a clean slate
        if os.path.exists(error_file_path):
            os.remove(error_file_path)
        
        error_writer = None
        errorfile = None

        all_transformed_rows = []

        with open(input_path, 'r') as infile:
            reader = csv.DictReader(infile)

            # Process data in chunks
            chunk = []
            for row in reader:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    transformed_chunk = self.transformer.transform(chunk)
                    all_transformed_rows.extend(transformed_chunk)
                    chunk = []

            # Process any remaining rows
            if chunk:
                transformed_chunk = self.transformer.transform(chunk)
                all_transformed_rows.extend(transformed_chunk)

        # Apply sorting if defined in the transformations
        for transformation in self.config['transformations']:
            if transformation['action'] == 'sort_data':
                all_transformed_rows = self.transformer.sort_data(all_transformed_rows, transformation)
                break

        # Open the output file for writing the transformed rows
        with open(output_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=all_transformed_rows[0].keys())
            writer.writeheader()
            for row in all_transformed_rows:
                try:
                    writer.writerow(row)
                except Exception as e:
                    logging.error(f"Error writing row: {e}")
                    if not error_writer:
                        errorfile = open(error_file_path, 'w', newline='')
                        error_writer = csv.DictWriter(errorfile, fieldnames=row.keys())
                        error_writer.writeheader()
                    error_writer.writerow(row)

        if errorfile:
            errorfile.close()

# Configure logging to log errors
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
