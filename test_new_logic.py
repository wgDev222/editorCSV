import unittest
from new_logic import Editor, Validator, Parser
import pandas as pd
import os.path
from os import remove


class TestEditor(unittest.TestCase):
    def test_read_csv_file(self):
        source_file = 'Data/test_read.csv'
        output_df = Editor.read(source_file, 0)
        check_df = pd.read_csv(source_file, sep=';', skiprows=0)

        self.assertTrue(check_df.equals(output_df))

    def test_blank_lines(self):
        source_file = 'Data/test_blank_lines.csv'
        blank_lines = 2
        cols = 6
        output_df = Editor.read(source_file, blank_lines)

        self.assertEqual(len(output_df.columns), cols)

    def test_removing_headers(self):
        source_file = 'Data/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_remove = ['Symbol', 'Stan']

        check_df = pd.read_csv(source_file, sep=';')
        check_df.drop(columns=headers_to_remove, inplace=True)

        modified_df = Editor.rem_headers(output_df, headers_to_remove)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_adding_headers(self):
        source_file = 'Data/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_add = {'Family': 'test', 'Sale': True}

        check_df = pd.read_csv(source_file, sep=';')
        for header, value in headers_to_add.items():
            check_df[header] = value

        modified_df = Editor.add_headers(output_df, headers_to_add)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_saving_file_to_csv(self):
        source_file = 'Data/test.csv'
        output_filepath = 'Data/renamed.csv'

        df = Editor.read(source_file, 0)
        Editor.save(df, output_filepath)

        file_saved = os.path.exists(output_filepath)

        self.assertTrue(file_saved)

        remove(output_filepath)

class TestValidate(unittest.TestCase):
    def test_path_existence(self):
        self.assertFalse(Validator.dir('Path'))
        self.assertTrue(Validator.dir('Data'))

    def test_file_existence(self):
        self.assertTrue(Validator.file('Data/h_add.csv'))
        self.assertFalse(Validator.file('h_add.csv'))
        self.assertFalse(Validator.file('Data/header'))


class TestParser(unittest.TestCase):
    def test_parsing_new_headers_file(self):
        arg = 'Data/h_add.csv'

        check_df = pd.read_csv(arg, sep=';')
        check_headers = check_df.set_index('Name').to_dict('dict')['Value']

        headers = Parser.new_headers(arg)
        self.assertEqual(headers, check_headers)

    def test_parsing_new_headers_inline(self):
        arg = ['Family:test', 'Price:Much']

        check_headers = {}
        for header in arg:
            items = header.split(':')
            if len(items) == 1:
                items.append('')
            check_headers[items[0]] = items[1]

        headers = Parser.new_headers(arg)
        self.assertEqual(headers, check_headers)


    def test_parsing_rem_headers_file(self):
        arg = 'Data/h_remove.csv'

        check_df = pd.read_csv(arg, sep=';')
        check_headers = check_df['Header'].tolist()

        headers = Parser.rem_headers(arg)

        self.assertEqual(headers, check_headers)

    def test_parsing_rem_headers_inline(self):
        arg = ['Lp', 'SKU']

        check_headers = arg

        headers = Parser.rem_headers(arg)

        self.assertEqual(headers, check_headers)

    def test_parsing_rename_headers_file(self):
        arg = 'Data/h_rename.csv'

        check_df = pd.read_csv(arg, sep=';')
        check_headers = check_df.set_index('Name').to_dict('dict')['NewName']

        headers = Parser.rename_headers(arg)
        self.assertEqual(headers, check_headers)

    def test_parsing_rename_headers_inline(self):
        arg = ['family:Family', 'Price:Cena']

        check_headers = {}
        for header in arg:
            items = header.split(':')
            if len(items) == 1:
                items.append('')
            check_headers[items[0]] = items[1]

        headers = Parser.rename_headers(arg)
        self.assertEqual(headers, check_headers)


if __name__ == '__main__':
    unittest.main()
