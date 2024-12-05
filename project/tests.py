import sqlite3
import pandas as pd
import os
import unittest
from pipeline import(transformByYear, transformSelectColumns, transformMerge, transformFillMissingValuesWithMean, loadDataSet, main)


class pipeline_tests(unittest.TestCase):

    def setUp(self):
         current_file = os.path.dirname(__file__)
         parent_directory = os.path.dirname(current_file)
         self.data_dir = os.path.join(parent_directory, "data")
         self.output_file = os.path.join(self.data_dir, 'productivity_compensation_and_poverty_level.db')

         if os.path.exists(self.output_file):
             os.remove(self.output_file)

    #Unit Test1
    def test_transformByYear(self):
        #Test data
        data = pd.DataFrame({
            'year':[1950, 1960, 1965,1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 
                    1991, 1995, 1995, 1995, 2000, 2005, 2006, 2009, 2010, 2011, 2012, 2013, 2014, 
                    2015, 2016, 2017, 2018, 2019, 2020, 2025, 2030, 2070],
            'wage': [1] * 36
        })

        transformed_data = transformByYear(data)
        valid_years_condition = ((transformed_data['year'] >= 1980) & (transformed_data['year'] <= 1990)) | \
                                 ((transformed_data['year'] >= 2010) & (transformed_data['year'] <= 2020))
        invalid_years = transformed_data[~valid_years_condition]
        self.assertTrue(invalid_years.empty, f"Test Failed: Invalid years found: {invalid_years['year'].tolist()}")
        print("Unit Test1 Passed: for transformByYear()")

    #Unit Test2
    def test_transformSelectColumns(self):
        #Test data
        data = pd.DataFrame({
            'year': [1980, 1981, 1982],
            'wage': [1, 2, 3],
            'hours': [60, 70, 80]
        })

        #Test2(a) valid columns
        valid_columns = ['year', 'wage']
        transformed_data = transformSelectColumns(data, valid_columns)
        self.assertEqual(transformed_data.shape, (3, 2), f"Test Failed: Expected shape (3, 2), but got {transformed_data.shape}")
        print("Unit Test2 Passed: for transformSelectColumns() with valid columns")

        #Test2(b) invalid columns
        invalid_columns = ['year','wage', 'wrong','wrong2']
      
        # Calling transformSelectColumns with invalid columns
        transformed_data = transformSelectColumns(data, invalid_columns)

        # Check that the resulting DataFrame has the shape (3, 2) — only the valid columns are included
        self.assertEqual(transformed_data.shape, (3, 2), f"Test Failed: Expected shape (3, 2), but got {transformed_data.shape}")
        print("Unit Test2 Passed: for transformSelectColumns() with invalid columns")

    #System-level test: tests if the pipeline executes successfully and the DB is created & populated successfully
    def test_pipeline_execution(self):
        main()

        #Test1: tests if the DB is created
        self.assertTrue(os.path.exists(self.output_file), "DB is not created.")

        #Test2: tests that the DB is not empty
        conn = sqlite3.connect(self.output_file)
        cursor = conn.cursor()

        #Test3: tests if the table exists in the DB
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='productivity_compensation_and_poverty_level';")
        self.assertIsNotNone(cursor.fetchone(), "Expected table does not exist.")

        #Test4: tests that the table is not empty
        query_to_show_table_data = "SELECT COUNT(*) FROM productivity_compensation_and_poverty_level;"
        cursor.execute(query_to_show_table_data)
        count = cursor.fetchone()[0]
        self.assertGreater(count, 0, "The output table is empty.")

        conn.close()

    def tearDown(self):
        """Environment cleanup after each test"""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)


if __name__ == "__main__":
    unittest.main()