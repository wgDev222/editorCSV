import unittest
from logic import Editor, Validator, Parser
import pandas as pd
import os.path
from os import remove


class TestEditor(unittest.TestCase):
    def test_read_csv_file(self):
        source_file = 'Tests/Files/test_read.csv'
        output_df = Editor.read(source_file)
        check_df = pd.read_csv(source_file, sep=';', skiprows=0)

        self.assertTrue(check_df.equals(output_df))

    def test_read_csv_delimiter(self):
        source_file = 'Tests/Files/test_read_delimiter.csv'
        source_delimiter = ':'

        output_df = Editor.read(source_file, delimiter=source_delimiter)
        check_df = pd.read_csv(source_file, sep=source_delimiter)

        self.assertTrue(check_df.equals(output_df))

    def test_blank_lines(self):
        source_file = 'Tests/Files/test_blank_lines.csv'
        blank_lines = 2
        cols = 6
        output_df = Editor.read(source_file, blank_lines)
        self.assertEqual(len(output_df.columns), cols)

    def test_removing_headers(self):
        source_file = 'Tests/Files/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_remove = ['Symbol', 'Stan']

        check_df = pd.read_csv(source_file, sep=';')
        check_df.drop(columns=headers_to_remove, inplace=True)

        modified_df = Editor.rem_headers(output_df, headers_to_remove)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_adding_headers(self):
        source_file = 'Tests/Files/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_add = {'Family': 'test', 'Sale': True}

        check_df = pd.read_csv(source_file, sep=';')
        for header, value in headers_to_add.items():
            check_df[header] = value

        modified_df = Editor.add_headers(output_df, headers_to_add)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_duplicating_headers(self):
        source_file = 'Tests/Files/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_dupl = {'Nazwa': 'Name', 'Symbol': 'Znak'}

        check_df = pd.read_csv(source_file, sep=';')
        for header, duplicate_header in headers_to_dupl.items():
            col = check_df[header]
            dupl_col_index = check_df.columns.get_loc(header) + 1
            check_df.insert(dupl_col_index, duplicate_header, col, True)

        modified_df = Editor.duplicate_headers(output_df, headers_to_dupl)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_renaming_headers(self):
        source_file = 'Tests/Files/test.csv'
        output_df = Editor.read(source_file, 0)
        headers_to_rename = {'family': 'Family', 'Sale': 'SALE'}

        check_df = pd.read_csv(source_file, sep=';')
        check_df.rename(columns=headers_to_rename, inplace=True)

        modified_df = Editor.rename_headers(output_df, headers_to_rename)

        self.assertTrue(modified_df.columns.equals(check_df.columns))

    def test_saving_file_to_csv(self):
        source_file = 'Tests/Files/test.csv'
        output_filepath = 'Tests/Files/renamed.csv'

        df = Editor.read(source_file, 0)
        Editor.save(df, output_filepath)

        file_saved = os.path.exists(output_filepath)

        self.assertTrue(file_saved)

        remove(output_filepath)

    def test_saving_file_to_csv_delimiter(self):
        source_file = 'Tests/Files/test.csv'
        output_filepath = 'Tests/Files/new.csv'
        check_filepath = 'Tests/Files/check.csv'

        output_delimiter = ':'

        output_df = Editor.read(source_file)
        Editor.save(output_df, output_filepath, delimiter=output_delimiter)

        check_df = pd.read_csv(source_file, sep=';')
        check_df.to_csv(check_filepath, sep=output_delimiter, index=False)

        output_df = pd.read_csv(output_filepath, sep=output_delimiter)
        check_df = pd.read_csv(check_filepath, sep=output_delimiter)

        self.assertTrue(check_df.equals(output_df))

        remove(output_filepath)
        remove(check_filepath)

    def test_striping_values(self):
        source_file = 'Tests/Files/test.csv'
        output_df = Editor.read(source_file, 0)
        values_to_strip = {'Symbol': 1, 'Nazwa': -1}

        check_df = pd.read_csv(source_file, sep=';')

        for header, n in values_to_strip.items():
            if n >= 0:
                check_df[header] = check_df[header].apply(lambda x: x[n:])
            else:
                check_df[header] = check_df[header].apply(lambda x: x[:n])

        modified_df = Editor.strip_values(output_df, values_to_strip)

        self.assertTrue(modified_df.columns.equals(check_df.columns))


class TestValidate(unittest.TestCase):
    def test_path_existence(self):
        self.assertFalse(Validator.dir('Path'))
        self.assertTrue(Validator.dir('Tests/Files'))

    def test_file_existence(self):
        self.assertTrue(Validator.file('Tests/Files/h_add.csv'))
        self.assertFalse(Validator.file('h_add.csv'))
        self.assertFalse(Validator.file('Data/header'))


class TestParser(unittest.TestCase):
    def test_parsing_new_headers_file(self):
        arg = ['Tests/Files/h_add.csv']

        check_df = pd.read_csv(arg[0], sep=';')
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

    def test_parsing_dupl_headers_file(self):
        arg = ['Tests/Files/h_duplicate.csv']

        check_df = pd.read_csv(arg[0], sep=';')
        check_headers = check_df.set_index('Header').to_dict('dict')['Header_D']

        headers = Parser.duplicate_headers(arg)

        self.assertEqual(headers, check_headers)

    def test_parsing_dupl_headers_inline(self):
        arg = ['Nazwa:Name', 'Symbol:Znak']

        check_headers = {}
        for header in arg:
            items = header.split(':')
            if len(items) == 1:
                items.append('')
            check_headers[items[0]] = items[1]

        headers = Parser.new_headers(arg)
        self.assertEqual(headers, check_headers)

    def test_parsing_rem_headers_file(self):
        arg = ['Tests/Files/h_remove.csv']

        check_df = pd.read_csv(arg[0], sep=';')
        check_headers = check_df['Header'].tolist()

        headers = Parser.rem_headers(arg)
        self.assertEqual(headers, check_headers)

    def test_parsing_rem_headers_inline(self):
        arg = ['Lp', 'SKU']

        check_headers = arg

        headers = Parser.rem_headers(arg)

        self.assertEqual(headers, check_headers)

    def test_parsing_rename_headers_file(self):
        arg = ['Tests/Files/h_rename.csv']

        check_df = pd.read_csv(arg[0], sep=';')
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

    def test_parsing_striping_values_file(self):
        arg = 'Tests/Files/strip.csv'

        check_df = pd.read_csv(arg, sep=';')
        check_headers = check_df.set_index('Header').to_dict('dict')['Num']

        headers = Parser.strip_values(arg)
        self.assertEqual(headers, check_headers)


if __name__ == '__main__':
    unittest.main()
