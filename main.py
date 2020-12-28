import argparse
from logic import *

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
parser.add_argument('--stan_mod', action='store_true', default=False, help='Modify Stan header')
parser.add_argument('-e', '--encoding', action='store', default='utf-8', type=str,
                    help='Input file encoding')
parser.add_argument('-d', '--delimiter', action='store', default=';', type=str, help='Delimiter for csv')

args = parser.parse_args()

editor = CSVEditor(args.delimiter)

new_headers = {}
for h in args.add_headers:
    items = h.split(':')
    if len(items) == 1:
        items.append('')
    new_headers[items[0]] = items[1]

mod = {}
if args.stan_mod:
    mod = {'Stan': stan_mod}

editor.modify(args.file, line_d=args.lines, new_headers=new_headers,
              rem_headers=args.rem_headers, modifiers=mod, encoding=args.encoding, o_file=args.output)




