import pandas as pd
import os.path

class Editor:
    @staticmethod
    def read(filename, lines_skipped=0):
        df = pd.read_csv(filename, sep=';', skiprows=lines_skipped)
        return df

    @staticmethod
    def save(df, filepath):
        df.to_csv(filepath)

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

class Parser:
    @staticmethod
    def new_headers(arg):
        headers_to_add = {}
        if Validator.file(str(arg)):
            df = Editor.read(arg)
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
        headers_to_remove = []
        if Validator.file(str(arg)):
            df = Editor.read(arg)
            headers_to_remove = df['Header'].tolist()
        else:
            return arg

        return headers_to_remove

    @staticmethod
    def rename_headers(arg):
        headers_to_rename = {}
        if Validator.file(str(arg)):
            df = Editor.read(arg)
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





