import csv
from os import remove

class Validation:
    @staticmethod
    def check_key(key, _dict, msg, exists=True):
        if exists:
            if key in _dict:
                raise Exception(msg)
        else:
            if key not in _dict:
                raise Exception(msg)
        return True

class Decoding:
    @staticmethod
    def to_utf8(file):
        with open(file, 'rb') as f:
            text = f.read()

        with open(file, 'w') as f:
            f.write(text.decode('iso-8859-2'))

class CSVEditor:

    def __init__(self, delimiter=','):
        self.__delimiter = delimiter

    def get_delimiter(self):
        return self.__delimiter

    def set_delimiter(self, delimiter):
        self.__delimiter = delimiter

    def proc_1(self, file, new_headers, rem_headers, modifiers, line_d=0, encoding='utf-8', o_file=False):

        with open(file, encoding=encoding) as csv_file:

            # Lines skipping
            for i in range(line_d):
                next(csv_file)

            csv_reader = csv.DictReader(csv_file, delimiter=self.__delimiter)

            fieldnames = csv_reader.fieldnames.copy()
            for header in new_headers.keys():
                Validation.check_key(header, fieldnames, f"Warning: New Header - {header} - already exists.")
                fieldnames.append(header)

            for header in rem_headers:
                Validation.check_key(header, fieldnames, f"Warning: Header - {header} - can't be removed, because it doesn't exist", exists=False)
                fieldnames.remove(header)

            with open('temp.csv', 'w') as result_file:
                csv_writer = csv.DictWriter(result_file, fieldnames=fieldnames, delimiter=self.__delimiter, quotechar='"', quoting=csv.QUOTE_ALL)

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

            with open('temp.csv', 'r') as r:
                f = o_file or file
                with open(f, 'w') as o:
                    for line in r:
                        o.write(line)

            remove('temp.csv')


def stan_mod(value):
    return 0 if value == 'brak' else 1


# editor = CSVEditor(';')
#
# editor.proc_1('part.csv', line_d=1, new_headers={'Family': 'test'},
#               rem_headers=['Lp'], modifiers={'Stan': stan_mod})
