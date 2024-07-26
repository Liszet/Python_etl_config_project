from datetime import datetime
import decimal

class Transformer:
    def __init__(self, transformations):
        self.transformations = transformations

    def transform(self, row):
        for transformation in self.transformations:
            action = transformation['action']
            if action == 'rename_column':
                self.rename_column(row, transformation)
            elif action == 'concatenate_date':
                self.concatenate_date_columns(row, transformation)
            elif action == 'add_column_constant':
                self.add_column_constant(row, transformation)
            elif action == 'select_output_columns':
                row = self.select_output_columns(row, transformation)
        return row
    
    # Rename a column based on config file
    def rename_column(self, row, transformation):
        # Check if proper_case is required
        if transformation.get('proper_case', False): # If proper_case is True, convert the value to title case and rename the column
            row[transformation['target_column']] = row.pop(transformation['source_column']).title()
        else: # Otherwise just rename the column
            row[transformation['target_column']] = row.pop(transformation['source_column'])
        row[transformation['target_column']] = self.cast_type(row[transformation['target_column']], transformation['type']) # Cast the value to the required type based on config file
    
    # Concatenate date columns and save to target column
    def concatenate_date_columns(self, row, transformation):
        concatenated_value = ''.join(row[col] for col in transformation['source_columns']) # Concatenate all source columns with no space
        datetime_value = datetime.strptime(concatenated_value, "%Y%m%d").date() # Convert concatenated value to date
        row[transformation['target_column']] = datetime_value.strftime(transformation['format']) # Output format based on config file and save to target column as string

    # Add a constant value to a new column
    def add_column_constant(self, row, transformation):
        row[transformation['target_column']] = self.cast_type(transformation['value'], transformation['type'])

    # Select output columns based on config file
    def select_output_columns(self, row, transformation):
        return {col: row[col] for col in transformation['columns']}
    
    # Cast the value to the required type based on config file
    def cast_type(self, value, type_str):
        if type_str == 'Integer':
            return int(value)
        elif type_str == 'BigDecimal':
            return decimal.Decimal(value)
        elif type_str == 'String':
            return str(value)
        return value