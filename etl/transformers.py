from datetime import datetime
import decimal

class Transformer:
    def __init__(self, transformations):
        self.transformations = transformations

    def transform(self, rows):
        single_row = False
        # Check if rows is a single dictionary and convert to list
        if isinstance(rows, dict):
            rows = [rows]
            single_row = True

        transformed_rows = []
        for row in rows:
            transformed_row = row.copy()
            for transformation in self.transformations:
                action = transformation['action']
                if action == 'rename_column':
                    self.rename_column(transformed_row, transformation)
                elif action == 'concatenate_date':
                    self.concatenate_date_columns(transformed_row, transformation)
                elif action == 'add_column_constant':
                    self.add_column_constant(transformed_row, transformation)
            transformed_rows.append(transformed_row)
        
        # Apply sorting if defined in the transformations
        for transformation in self.transformations:
            if transformation['action'] == 'sort_data':
                transformed_rows = self.sort_data(transformed_rows, transformation)
                break

        # Apply selecting output columns if defined in the transformations
        for transformation in self.transformations:
            if transformation['action'] == 'select_output_columns':
                transformed_rows = [self.select_output_columns(row, transformation) for row in transformed_rows]
                break

        return transformed_rows[0] if single_row else transformed_rows # Return a single dictionary if only one row is passed
    
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

    # Sort the data based on config file
    def sort_data(self, rows, transformation):
        sort_column = transformation['sort_column']
        sort_order = transformation.get('sort_order', 'asc').lower()
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'
        return sorted(rows, key=lambda x: x[sort_column], reverse=(sort_order == 'desc'))

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