import os
import unittest
from goodtables import validate
import datapackage

# Constants
REPORT_LIMIT = 1000
ROW_LIMIT = 100000


class TestData(unittest.TestCase):

    def setUp(self):
        """Set up datapackage for testing."""
        try:
            self.dp = datapackage.DataPackage('datapackage.json')
        except datapackage.exceptions.ValidationError as e:
            self.fail(f"Datapackage validation failed: {e}")

    def test_structure(self):
        """Test the structure of the data."""
        data_format = 'csv'

        # Validate the structure
        data_path = self.dp.descriptor['resources'][0]['path']
        report = validate(data_path, structure=True, row_limit=ROW_LIMIT, report_limit=REPORT_LIMIT)

        # Extract validation result
        valid = report['valid']

        # Exclude unnecessary fields
        exclude_fields = ['result_context', 'processor', 'row_name', 'result_category', 'column_index', 'column_name', 'result_level']

        # Generate output and assert
        self.assertTrue(valid, msg="Structure validation failed.")

    def test_schema(self):
        """Test the schema of the data."""
        data_format = 'csv'
        data_path = self.dp.descriptor['resources'][0]['path']
        schema = self.dp.descriptor['resources'][0]['schema']

        # Validate the schema
        report = validate(data_path, schema=schema, row_limit=ROW_LIMIT, report_limit=REPORT_LIMIT)

        # Extract validation result
        valid = report['valid']

        # Exclude unnecessary fields
        exclude_fields = ['result_context', 'processor', 'row_name', 'result_category', 'column_name', 'result_id', 'result_level']

        # Generate output and assert
        self.assertTrue(valid, msg="Schema validation failed.")


if __name__ == '__main__':
    former_path = os.getcwd()
    try:
        dp = datapackage.DataPackage('datapackage.json')
        unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(TestData))
    except Exception as e:
        os.chdir(former_path)
        raise e
