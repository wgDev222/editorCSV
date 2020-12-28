import csv
from os import remove, path, listdir
import pandas as pd
from pathlib import Path

# import xlrd


class Validation:
    @staticmethod
    def check_key(key, _dict, msg, exists=True):
        if exists:
            if key in _dict:
                print(msg)
                return False
                # raise Exception(msg)
        else:
            if key not in _dict:
                print(msg)
                return False
                # raise Exception(msg)
        return True

class Decoding:
    @staticmethod
    def to_utf8(file):
        with open(file, 'rb') as f:
            text = f.read()

        with open(file, 'w') as f:
            f.write(text.decode('iso-8859-2'))

class Convert:
    @staticmethod
    def to_csv(file, _path=''):
        output_path = Path(_path)

        sheets = pd.read_excel(file, sheet_name=None)
        files = []
        for key, s in sheets.items():
            filename = output_path / f"{key}.csv"
            files.append(filename)
            s.to_csv(filename, index=None, header=True, sep=';')
        return files

class CSVEditor:

    def __init__(self, delimiter=','):
        self.__delimiter = delimiter

    def get_delimiter(self):
        return self.__delimiter

    def set_delimiter(self, delimiter):
        self.__delimiter = delimiter

    def modify(self, file, new_headers, rem_headers, modifiers, line_d=0, encoding='utf-8', o_file=False):
        filename, file_extension = path.splitext(file)
        csv_files = []
        if file_extension == '.xlsx':
            csv_files = Convert.to_csv(file)
        elif file_extension == '':
            for entry in listdir(file):
                if path.isfile(path.join(file, entry)):
                    print(entry)
        else:
            csv_files.append(Path(file))
        for csv_file in csv_files:
            self.__process(csv_file, encoding, line_d, new_headers, rem_headers, modifiers, o_file)

    def __process(self, file, encoding, line_d, new_headers, rem_headers, modifiers, o_file):
        with open(file, encoding=encoding) as csv_file:
            # Lines skipping
            for i in range(line_d):
                next(csv_file)

            csv_reader = csv.DictReader(csv_file, delimiter=self.__delimiter)
            fieldnames = csv_reader.fieldnames.copy()

            for header in new_headers.keys():
                if Validation.check_key(header, fieldnames, f"Warning: New Header - {header} - already exists."):
                    fieldnames.append(header)
                else:
                    new_headers = {}

            for header in rem_headers:
                if Validation.check_key(header, fieldnames, f"Warning: Header - {header} - can't be removed, because it doesn't exist", exists=False):
                    fieldnames.remove(header)
                else:
                    rem_headers = []
            print(fieldnames)
            self.__save(fieldnames, csv_reader, new_headers, modifiers, rem_headers)
            self.__write(o_file, file)

            remove('temp.csv')

    def __save(self, fieldnames, csv_reader, new_headers, modifiers, rem_headers):
        with open('temp.csv', 'w') as result_file:
            csv_writer = csv.DictWriter(result_file, fieldnames=fieldnames, delimiter=self.__delimiter, quotechar='"',
                                        quoting=csv.QUOTE_ALL)

            csv_writer.writeheader()

            for line in csv_reader:
                # Adding new headers with default values
                for header, value in new_headers.items():
                    line[header] = value

                # Removing headers
                for header in rem_headers:
                    del line[header]

                # modifying values
                for header, func in modifiers.items():
                    Validation.check_key(header, line,
                                         f"Warning: Header - {header} - can't be modified, because it doesn't exist",
                                         exists=False)
                    line[header] = func(line[header])
                csv_writer.writerow(line)

    def __write(self, o_file, s_file):
        with open('temp.csv', 'r') as r:
            f = o_file or s_file
            with open(f, 'w') as o:
                for line in r:
                    o.write(line)

    def main(self, file, o_path):
        filename, file_extension = path.splitext(file)
        csv_files = []

        if file_extension == '.xlsx':
            csv_files = Convert.to_csv(file, o_path)
            print(csv_files)
        else:
            csv_files.append(Path(file))

        for csv_file in csv_files:
            self.modify(csv_file, new_headers={'Family': 'test'}, rem_headers=[], modifiers={})


def stan_mod(value):
    return 0 if value == 'brak' else 1


# editor = CSVEditor(';')
#
# editor.proc_1('part.csv', line_d=1, new_headers={'Family': 'test'},
#               rem_headers=['Lp'], modifiers={'Stan': stan_mod})

# c = CSVEditor(',')
# c.main('Test.csv', '')
