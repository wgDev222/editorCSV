import pandas as pd
import os.path

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
        df.to_csv(filepath, sep=delimiter, index=False)

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


class Parser:
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
            for filename, df in dfs.items():
                filename = args.output + filename +'.csv'
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

    df = Editor.add_headers(df, headers_add)
    df = Editor.rem_headers(df, headers_remove)
    df = Editor.rename_headers(df, headers_rename)

    Editor.save(df, args.output, delimiter=args.delimiter)
