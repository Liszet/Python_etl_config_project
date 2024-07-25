from etl.etl import ETL
import time

if __name__ == "__main__":
    start_time = time.time()

    etl = ETL('config/transformations.json')
    etl.process_file('data/sample.csv', 'data/output.csv')

    end_time = time.time()
    duration = end_time - start_time

    print("\n The sample.csv file has been transformed successfully. Check output.csv for the results.")
    print(f"Process completed in {duration:.2f} seconds.")

    # Open the output file and print the first 5 rows
    print("\n First 5 rows of the output file:\n")
    with open('data/output.csv', 'r') as file:
        for _ in range(5):
            print(file.readline().strip())