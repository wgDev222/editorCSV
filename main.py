import argparse
from logic import Editor, execute_logic

parser = argparse.ArgumentParser(description='Editor for CSV files', prog='editorCSV',  usage='%(prog)s [options]',
                                 epilog="Created by Wiktor Grochowski", allow_abbrev=False)

parser.add_argument('file', action='store', help='Path to input file')
parser.add_argument('-o', '--output', action='store', default=False, help='Path to output file')
parser.add_argument('-l', '--lines', action='store', type=int, default=0, help='Number of lines to delete')
parser.add_argument('-a', '--add_headers', action='store', type=str, nargs='*', default=[],
                    help='Headers with values to add.If value is not specified empty string is passed.'
                         ' Example: header:value header2:value2')
parser.add_argument('-r', '--rem_headers', action='store', type=str, nargs='*', default=[],
                    help='Headers to remove')
parser.add_argument('-n', '--rename_headers', action='store', type=str, nargs='*', default=[],
                    help='Headers to Rename')
parser.add_argument('-d', '--delimiter', action='store', default=';', type=str, help='Delimiter for csv')
parser.add_argument('-c', '--duplicate_headers', action='store', type=str, nargs='*', default=[],
                    help='Headers to Duplicate')
parser.add_argument('-s', '--strip_values', action='store', type=str, default=False, help='Strips values from specified column')
parser.add_argument('--dd', action='store_true', help='Deletes duplicate rows')
# parser.add_argument('-q', '--quotes', action='store', default=';', type=str, help='String quotes for result file')

if __name__ == '__main__':
    args = parser.parse_args()
    execute_logic(args)
