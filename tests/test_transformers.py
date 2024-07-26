import unittest
from etl.transformers import Transformer
from datetime import datetime
import decimal

class TestTransformer(unittest.TestCase):

    def setUp(self):
        self.transformations = [
            {
                "action": "rename_column",
                "source_column": "Order Number",
                "target_column": "OrderID",
                "type": "Integer"
            },
            {
                "action": "concatenate_date",
                "source_columns": ["Year", "Month", "Day"],
                "target_column": "OrderDate",
                "format": "%Y-%m-%d"
            },
            {
                "action": "rename_column",
                "source_column": "Product Number",
                "target_column": "ProductId",
                "type": "String"
            },
            {
                "action": "rename_column",
                "source_column": "Product Name",
                "target_column": "ProductName",
                "type": "String",
                "proper_case": True
            },
            {
                "action": "rename_column",
                "source_column": "Count",
                "target_column": "Quantity",
                "type": "BigDecimal"
            },
            {
                "action": "add_column_constant",
                "target_column": "Unit",
                "value": "kg",
                "type": "String"
            },
            {
                "action": "select_output_columns",
                "columns": ["OrderID", "OrderDate", "ProductId", "ProductName", "Quantity", "Unit"]
            }
        ]
        self.transformer = Transformer(self.transformations)

    # Test renaming a column and converting to integer
    def test_rename_column(self):
        row = {'Order Number': '12345'}
        expected = {'OrderID': 12345}
        self.transformer.rename_column(row, self.transformations[0])
        self.assertEqual(row, expected)

    # Test renaming a column and converting to proper case
    def test_rename_column_proper_case(self):
        row = {'Product Name': 'test product'}
        expected = {'ProductName': 'Test Product'}
        self.transformer.rename_column(row, self.transformations[3])
        self.assertEqual(row, expected)

    # Test renaming a column without proper case conversion
    def test_rename_column_no_proper_case(self):
        row = {'Product Number': 'P123'}
        expected = {'ProductId': 'P123'}
        self.transformer.rename_column(row, self.transformations[2])
        self.assertEqual(row, expected)

    # Test renaming a column when the source column does not exist
    def test_rename_column_non_existent_source(self):
        row = {'Non Existent': 'value'}
        with self.assertRaises(KeyError):
            self.transformer.rename_column(row, self.transformations[0])

    # Test concatenating date columns with the default format
    def test_concatenate_date_columns(self):
        row = {'Year': '2020', 'Month': '07', 'Day': '15'}
        expected = {'OrderDate': '2020-07-15'}
        self.transformer.concatenate_date_columns(row, self.transformations[1])
        self.assertEqual(row['OrderDate'], expected['OrderDate'])

    # Test concatenating date columns with a different format
    def test_concatenate_date_columns_different_format(self):
        row = {'Year': '2020', 'Month': '07', 'Day': '15'}
        transformation = {
            "action": "concatenate_date",
            "source_columns": ["Year", "Month", "Day"],
            "target_column": "OrderDate",
            "format": "%d-%m-%Y"
        }
        self.transformer.concatenate_date_columns(row, transformation)
        expected = {'OrderDate': '15-07-2020'}
        self.assertEqual(row['OrderDate'], expected['OrderDate'])

    # Test concatenating date columns with invalid date components
    def test_concatenate_date_columns_invalid_date(self):
        row = {'Year': '2020', 'Month': '02', 'Day': '30'}
        with self.assertRaises(ValueError):
            self.transformer.concatenate_date_columns(row, self.transformations[1])

    # Test adding a constant column with string type
    def test_add_column_constant(self):
        row = {}
        expected = {'Unit': 'kg'}
        self.transformer.add_column_constant(row, self.transformations[5])
        self.assertEqual(row, expected)

    # Test adding a constant column with integer type
    def test_add_column_constant_integer(self):
        row = {}
        transformation = {
            "action": "add_column_constant",
            "target_column": "ConstantColumn",
            "value": "42",
            "type": "Integer"
        }
        self.transformer.add_column_constant(row, transformation)
        expected = {'ConstantColumn': 42}
        self.assertEqual(row, expected)

    # Test adding a constant column with decimal type
    def test_add_column_constant_decimal(self):
        row = {}
        transformation = {
            "action": "add_column_constant",
            "target_column": "ConstantColumn",
            "value": "10.55",
            "type": "BigDecimal"
        }
        self.transformer.add_column_constant(row, transformation)
        expected = {'ConstantColumn': decimal.Decimal('10.55')}
        self.assertEqual(row, expected)

    # Test selecting output columns when all columns are present
    def test_select_output_columns(self):
        row = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Product Name',
            'Quantity': decimal.Decimal('10.5'),
            'Unit': 'kg',
            'ExtraColumn': 'Should be removed'
        }
        expected = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Product Name',
            'Quantity': decimal.Decimal('10.5'),
            'Unit': 'kg'
        }
        result = self.transformer.select_output_columns(row, self.transformations[6])
        self.assertEqual(result, expected)

    # Test selecting output columns when some columns are missing
    def test_select_output_columns_missing_column(self):
        row = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Product Name',
            'Unit': 'kg'
        }
        with self.assertRaises(KeyError):
            self.transformer.select_output_columns(row, self.transformations[6])

    # Test selecting output columns when extra columns are present
    def test_select_output_columns_extra_columns(self):
        row = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Product Name',
            'Quantity': decimal.Decimal('10.5'),
            'Unit': 'kg',
            'ExtraColumn': 'Should be removed'
        }
        expected = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Product Name',
            'Quantity': decimal.Decimal('10.5'),
            'Unit': 'kg'
        }
        result = self.transformer.select_output_columns(row, self.transformations[6])
        self.assertEqual(result, expected)

    # Test the full transformation process
    def test_full_transformation(self):
        row = {
            'Order Number': '12345',
            'Year': '2020',
            'Month': '07',
            'Day': '15',
            'Product Number': 'P123',
            'Product Name': 'test product',
            'Count': '10.5',
            'ExtraColumn': 'Should be removed'
        }
        expected = {
            'OrderID': 12345,
            'OrderDate': '2020-07-15',
            'ProductId': 'P123',
            'ProductName': 'Test Product',
            'Quantity': decimal.Decimal('10.5'),
            'Unit': 'kg'
        }
        result = self.transformer.transform(row)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
