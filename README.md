# Configurable ETL system

## Overview

This project implements a configurable ETL (Extract, Transform, Load) system for transforming CSV files using Python's built-in libraries. The transformations are specified in a configuration file (`config/transformations.json`), allowing for flexible and customizable data processing. The output is a CSV file.

## Features

- Rename columns
- Concatenate columns to form dates
- Apply proper case to text fields
- Add constant values to columns
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

### Select Output Columns
Selects specific columns for the final output
```json
{
    "action": "select_output_columns",
    "columns": ["OrderID", "OrderDate", "ProductId", "ProductName", "Quantity", "Unit"]
}
```
- **columns**: List of columns to include in the final output


## Unit tests
To run the tests, run the following line in the terminal. This runs all the unit tests found in the `tests` directory using the unittest Python built-in module.

```bash
python -m unittest discover tests
```