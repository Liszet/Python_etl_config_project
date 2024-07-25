import csv
import json
import logging
from .transformers import Transformer

class ETL:
    def __init__ (self, config_path):
        with open(config_path, 'r') as file:
            self.config = json.load(file)
        self.transformer = Transformer(self.config['transformations'])
    
    def process_file(self, input_path, output_path):
        with open(input_path, 'r') as infile, open(output_path, 'w', newline='') as outfile:
            reader = csv.DictReader(infile)
            writer = None

            for row in reader:
                try:
                    transformed_row = self.transformer.transform(row)
                    if not writer:
                        writer = csv.DictWriter(outfile, fieldnames=transformed_row.keys())
                        writer.writeheader()
                    writer.writerow(transformed_row)
                except Exception as e:
                    logging.error(f"Error processing row: {e}")

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')