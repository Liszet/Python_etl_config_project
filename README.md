# Configurable ETL system

## Overview

This project implements a configurable ETL (Extract, Transform, Load) system for transforming CSV files using Python's built-in libraries. The transformations are specified in a configuration file (`config/transformations.json`), allowing for flexible and customizable data processing. The output is a CSV file.

## Features

- Rename columns
- Concatenate columns to form dates
- Apply proper case to text fields
- Add constant values to columns
- Order the data based on a specific column
- Select specific columns for the output

## Installation

1. Clone the repository
2. Ensure you have Python 3 installed
3. No additional dependencies are required

## How to Run

1. Run the main script by using following command in the terminal:

```bash
python main.py
```

2. If you need to generate new sample data, run the following script

```bash
python .\data\generate_sample.py
```


## Transformations
The transformations are specified in a configuration file `config/transformations.json` . The available transformations and the parameters they take are further described below.

### Rename Column
Renames a column , optionally changes its type and optionally converts the text in the column to proper case

```json
{
    "action": "rename_column",
    "source_column": "Order Number",
    "target_column": "OrderID",
    "type": "Integer",
    "proper_case" : false
}
```
- **source_column**: The original column name
- **target_column**: The new column name
- **type**: (Optional) The data type to cast the column to. Supported types: `Integer`, `BigDecimal` , `String` . If ommited then it defaults to `String`. 
- **proper_case** (Optional): set to `true` if you want to convert the text in the column to proper case (title case)

### Concatenate Date
Concatenates multiple columns that represent year, month and day into a single column where the format can be specified

```json
{
    "action": "concatenate_date",
    "source_columns": ["Year", "Month", "Day"],
    "target_column": "OrderDate",
    "format": "%Y%m%d"
}
```
- **source_columns**: List of columns to concatenate
- **target_column**: The new column name
- **format**: The format of the output, use `strftime`and `strptime` compatible formats, like `%Y%m%d` or `%Y-%m-%d`

### Add Constant Column
Adds a new column with a constant value

```json
{
    "action": "add_constant",
    "target_column": "Unit",
    "value": "kg",
    "type": "String"
}
```
- **target_column**: The new column name.
- **value**: The constant value to add
- **type** (Optional): The data type of the constant value. If ommited then it defaults to `String` .

### Sort Data
Sorts the data based on a column. Default is ascending, unless otherwise specified.

```json
{
    "action": "sort_data",
    "sort_column": "OrderDate",
    "sort_order": "desc"
}
```
- **sort_column**: the column used for sorting
- **sort_order** (Optional): Default is ascending. Valid values `asc` (ascending) and `desc` (descending)

### Select Output Columns
Selects specific columns for the final output
```json
{
    "action": "select_output_columns",
    "columns": ["OrderID", "OrderDate", "ProductId", "ProductName", "Quantity", "Unit"]
}
```
- **columns**: List of columns to include in the final output


## Unit Tests
To run the tests, run the following line in the terminal. This runs all the unit tests found in the `tests` directory using the unittest Python built-in module.

```bash
python -m unittest discover tests
```

## Performance Tests

To evaluate the performance of the ETL system, I conducted tests by varying the size of the sample.csv file. 

Here is a summary of the performance test results:

| Sample.csv Number of Rows | Execution Time (sec) |
|---------------------------|---------------------|
| 1,000                     | 0.3                 |
| 100,000                   | 2                   |
| 1,000,000                 | 20                  |
| 10,000,000                | 300                 |
| 10,000,000                | 250  (etl_chunk)    |

And here are the specs of the computer running the tests:

- Processor: 11th Gen Intel(R) Core(TM) i7-11850H @ 2.50GHz
- RAM: 32 GB
- Storage: 474 GB SSD
- Operating System: Windows 11 23H2
- Python Version: 3.12.4

The last test is run by modifying the main.py to use etl_chunk.py file instead. There are some performance improvements, but the handling of the column transformations do mean that all data needs to be loaded into memory for part of the transformation. 

Further tests would need to be conducted. 
