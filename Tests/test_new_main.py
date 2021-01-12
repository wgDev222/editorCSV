import unittest
import main
import pandas as pd
from logic import execute_logic
from os import remove
from logic import Editor

class TestCLI(unittest.TestCase):
    def test_saving_to_new_csv_file(self):
        params = 'Tests/Files/test.csv -o Data/new.csv'
        args = main.parser.parse_args(params.split())

        execute_logic(args)

        check_df = pd.read_csv(args.file, sep=';')
        output_df = pd.read_csv(args.output, sep=';')

        self.assertTrue(check_df.equals(output_df))

        params = 'Tests/Files/missing.csv -o Data/new.csv'
        args = main.parser.parse_args(params.split())

        with self.assertRaises(Exception): execute_logic(args)

        remove('Data/new.csv')

    def test_adding_headers_file(self):
        params = 'Tests/Files/test.csv -a h_add.csv -o Data/new.csv'
        args = main.parser.parse_args(params.split())

        # execute_logic(args)
        #
        # check_df = pd.read_csv(args.file, sep=';')
        # # Editor.add_headers()
        #
        # output_df = pd.read_csv(args.output, sep=';')


if __name__ == '__main__':
    unittest.main()
