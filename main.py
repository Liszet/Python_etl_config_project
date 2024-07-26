from etl.etl import ETL # modify this to use etl.etl_chunk to handle bigger csv files
import time
import os

if __name__ == "__main__":
    start_time = time.time()

    etl = ETL('config/transformations.json')
    etl.process_file('data/sample.csv', 'data/output.csv')

    end_time = time.time()
    duration = end_time - start_time

    print("\n The sample.csv file has been transformed. Check output.csv for the results.")
    print(f"Process completed in {duration:.2f} seconds.")

    # Check if the error file exists and if it has any rows
    error_file_path = 'data/output_error.csv'
    if os.path.exists(error_file_path):
        with open(error_file_path, 'r') as error_file:
            error_rows = sum(1 for _ in error_file) - 1  # Subtract 1 for the header
        if error_rows > 0:
            print(f"\nThere were {error_rows} error rows during processing. Check output_error.csv for the error rows. Below is a sample.\n")
            with open('data/output_error.csv', 'r') as file:
                for _ in range(3):
                    print(file.readline().strip())
        else:
            print("\nNo errors encountered during processing.")
    else:
        print("\nNo errors encountered during processing.")

    # Open the output file and print the first 5 rows
    print("\n First 5 rows of the output file:\n")
    with open('data/output.csv', 'r') as file:
        for _ in range(5):
            print(file.readline().strip())