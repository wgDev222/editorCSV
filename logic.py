import pandas as pd
import os.path

STRING_QUOTING = True
MAX_SPLIT_COLUMN_COUNT = 4
COLS_SPLIT_BY = '|'

class Editor:
    @staticmethod
    def read(filename, lines_skipped=0, delimiter=';'):
        file_extenstion = os.path.splitext(filename)[1]

        if file_extenstion == '.xlsx':
            df_sheets = pd.read_excel(filename, sheet_name=None)
            return df_sheets
        elif file_extenstion == '.csv':
            df = pd.read_csv(filename, sep=delimiter, skiprows=lines_skipped)
            return df

    @staticmethod
    def save(df, filepath, delimiter=';'):
        quoting = 1
        if not STRING_QUOTING:
            quoting = 0
        df.to_csv(filepath, sep=delimiter, index=False, quoting=quoting)

    @staticmethod
    def rem_headers(df, headers_to_remove):
        result_df = df
        result_df.drop(columns=headers_to_remove, inplace=True)
        return result_df

    @staticmethod
    def add_headers(df, headers_to_add):
        result_df = df

        for header, value in headers_to_add.items():
            result_df[header] = value

        return result_df

    @staticmethod
    def rename_headers(df, headers_to_rename):
        result_df = df
        result_df.rename(columns=headers_to_rename, inplace=True)

        return result_df

    @staticmethod
    def duplicate_headers(df, headers_to_dupl):
        result_df = df

        for header, duplicate_header in headers_to_dupl.items():
            col = df[header]
            dupl_col_index = df.columns.get_loc(header)+1

            df.insert(dupl_col_index, duplicate_header, col, True)

        return result_df

    @staticmethod
    def strip_values(df, values_to_strip):
        result_df = df

        for header, n in values_to_strip.items():
            if n >= 0:
                df[header] = df[header].apply(lambda x: x[n:])
            else:
                df[header] = df[header].apply(lambda x: x[:n])

        return result_df

    @staticmethod
    def delete_duplicates(df, headers_to_dd):
        result_df = df
        for header in headers_to_dd:
            result_df.drop_duplicates([header], inplace=True)
        return result_df

    @staticmethod
    def bleach_values(df, headers_to_bleach):
        import bleach

        def clean(val, if_empty='None'):
            cleaned = bleach.clean(str(val)) or if_empty
            return cleaned

        for header in headers_to_bleach:
            df[header] = df[header].apply(lambda val: clean(val))

        return df

    @staticmethod
    def replace_values(df, headers_to_replace):
        for column, rep in headers_to_replace.items():
            a = rep.split('-')[0]
            try:
                b = rep.split('-')[1]
            except IndexError:
                b = ''
            df[column] = df[column].apply(lambda val: val.replace(a, b))
        return df

    @staticmethod
    def split_columns(df, columns_to_split):
        for column in columns_to_split:
            values_series = df[column]
            new_cols = [column]
            for i in range(1, MAX_SPLIT_COLUMN_COUNT):
                new_col_name = column + str(i)
                new_col_index = df.columns.get_loc(column) + i
                new_cols.append(new_col_name)

                df.insert(new_col_index, new_col_name, '', False)

            for i, value in enumerate(values_series):
                new_values = value.strip().split(COLS_SPLIT_BY)
                for j, new_col in enumerate(new_cols):
                    try:
                        df[new_col][i] = new_values[j]
                    except IndexError:
                        continue

        return df

    @staticmethod
    def trim_columns(df, columns_to_split):
        for column in columns_to_split:
            df[column] = df[column].apply(lambda val: str(val).strip())
        return df


class Parser:

    @staticmethod
    def parse(arg, header=['Header'], args_as_list=True):
        try:
            file = arg[0]
        except IndexError:
            return {}
        result_headers = {}
        if Validator.file(file):
            df = Editor.read(file)
            if args_as_list:
                result_headers = df[header[0]].tolist()
            else:
                result_headers = df.set_index(header[0]).to_dict('dict')[header[1]]
        else:
            if args_as_list:
                return arg
            else:
                for header in arg:
                    items = header.split(':')
                    if len(items) == 1:
                        items.append('')
                    result_headers[items[0]] = ''.join(items[1:])

        return result_headers

    @staticmethod
    def new_headers(arg):
        try:
            test_arg = arg[0]
        except IndexError:
            return {}
        headers_to_add = {}
        if Validator.file(test_arg):
            df = Editor.read(test_arg)
            headers_to_add = df.set_index('Name').to_dict('dict')['Value']
        else:
            for header in arg:
                items = header.split(':')
                if len(items) == 1:
                    items.append('')
                headers_to_add[items[0]] = items[1]

        return headers_to_add

    @staticmethod
    def duplicate_headers(arg):
        try:
            test_arg = arg[0]
        except IndexError:

            return {}
        headers_to_dupli = {}
        if Validator.file(test_arg):
            df = Editor.read(test_arg)
            headers_to_dupli = df.set_index('Header').to_dict('dict')['Header_D']
        else:
            for header in arg:
                items = header.split(':')
                if len(items) == 1:
                    items.append('')
                headers_to_dupli[items[0]] = items[1]

        return headers_to_dupli

    @staticmethod
    def rem_headers(arg):
        try:
            test_arg = arg[0]
        except IndexError:
            return []
        headers_to_remove = []
        if Validator.file(test_arg):
            df = Editor.read(test_arg)
            headers_to_remove = df['Header'].tolist()
        else:
            return arg

        return headers_to_remove

    @staticmethod
    def rename_headers(arg):
        try:
            test_arg = arg[0]
        except IndexError:
            return {}
        headers_to_rename = {}
        if Validator.file(test_arg):
            df = Editor.read(test_arg)
            headers_to_rename = df.set_index('Name').to_dict('dict')['NewName']
        else:
            for header in arg:
                items = header.split(':')
                if len(items) == 1:
                    items.append('')
                headers_to_rename[items[0]] = items[1]

        return headers_to_rename

    @staticmethod
    def strip_values(arg):
        if Validator.file(arg):
            df = Editor.read(arg)
            strip_values = df.set_index('Header').to_dict('dict')['Num']
            return strip_values
        else:
            return {}

    @staticmethod
    def delete_duplicates(arg):
        try:
            test_arg = arg[0]
        except IndexError:
            return []
        headers_to_dd = []
        if Validator.file(test_arg):
            df = Editor.read(test_arg)
            headers_to_dd = df['Header'].tolist()
        else:
            return arg

        return headers_to_dd

    @staticmethod
    def bleach_values(arg):
        return Parser.parse(arg)

    @staticmethod
    def replace_values(arg):
        return Parser.parse(arg, args_as_list=False, header=['Column', 'Replace'])

    @staticmethod
    def split_columns(arg):
        return Parser.parse(arg)

    @staticmethod
    def trim_columns(arg):
        return Parser.parse(arg)

class Validator:
    @staticmethod
    def dir(path):
        if os.path.exists(path) and os.path.isdir(path):
            return True
        else:
            return False

    @staticmethod
    def file(filepath):
        return os.path.isfile(filepath)


class Change:
    def __init__(self, header, new_name='', value=''):
        self.header = header
        self.new_name = new_name
        self.value = value


def execute_logic(args):
    if Validator.file(args.file):
        dfs = Editor.read(args.file, lines_skipped=args.lines, delimiter=args.delimiter)
        if isinstance(dfs, pd.DataFrame):
            modify_df(args, dfs)
        elif isinstance(dfs, dict):
            prefix = args.output
            for filename, df in dfs.items():
                filename = prefix + filename + '.csv'
                path = os.path.split(args.file)[0]
                args.output = os.path.join(path, filename)
                modify_df(args, df)
    else:
        raise Exception('Error: Source file does not exist')

def modify_df(args, df):
    if not args.output:
        args.output = args.file

    headers_add = Parser.new_headers(args.add_headers)
    headers_remove = Parser.rem_headers(args.rem_headers)
    headers_rename = Parser.rename_headers(args.rename_headers)
    headers_dupli = Parser.duplicate_headers(args.duplicate_headers)
    header_to_strip = Parser.strip_values(args.strip_values)
    headers_to_dd = Parser.delete_duplicates(args.dd)

    df = Editor.add_headers(df, headers_add)
    df = Editor.rem_headers(df, headers_remove)
    if args.split_cols is not None:
        columns_to_split = Parser.split_columns(args.split_cols)
        df = Editor.split_columns(df, columns_to_split)
    df = Editor.rename_headers(df, headers_rename)
    df = Editor.strip_values(df, header_to_strip)
    if args.trim_cols is not None:
        columns_to_trim = Parser.trim_columns(args.trim_cols)
        df = Editor.trim_columns(df, columns_to_trim)
    df = Editor.delete_duplicates(df, headers_to_dd)
    df = Editor.duplicate_headers(df, headers_dupli)
    if args.bleach is not None:
        header_to_bleach = Parser.bleach_values(args.bleach)
        df = Editor.bleach_values(df, header_to_bleach)
    if args.replace is not None:
        headers_to_replace = Parser.replace_values(args.replace)
        df = Editor.replace_values(df, headers_to_replace)

    Editor.save(df, args.output, delimiter=args.delimiter)
