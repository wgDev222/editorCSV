import argparse
from logic import *

parser = argparse.ArgumentParser(description='Editor for CSV files', prog='editorCSV',  usage='%(prog)s [options]',
                                 epilog="Created by Wiktor Grochowski", allow_abbrev=False)


parser.add_argument('file', action='store', help='Input file')
parser.add_argument('-o', '--output', action='store', default=False, help='Output file')
parser.add_argument('-l', '--lines', action='store', type=int, default=0, help='Number of lines to delete')
parser.add_argument('-a', '--add_headers', action='store', type=str, nargs='*', default=[], help='Headers to add, with default value. example: header:value')
parser.add_argument('-r', '--rem_headers', action='store', type=str, nargs='*', default=[], help='Headers to remove')
parser.add_argument('--stan_mod', action='store_true', help='Modify Stan header')
parser.add_argument('-e', '--encoding', action='store', type=str, help='Input file encoding')
parser.add_argument('-d', '--delimiter', action='store', default=';', type=str, help='Delimiter fro csv')


args = parser.parse_args()

print(args)

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

editor.proc_1(args.file, line_d=args.lines, new_headers=new_headers,
              rem_headers=args.rem_headers, modifiers=mod, encoding=args.encoding, o_file=args.output)

'''
- filename [string] •
- lines to remove [int] •
- headers to add [?] •
- headers to remove [list] •
- modifying function -> flag •
- encoding [string] •
- delimiter [string] •
- output file •
'''

# editor.proc_1('../cennik(pln)_2020-12-08_18-46 copy.csv', line_d=1, new_headers={'Family': 'test'},
#               rem_headers=['Lp'], modifiers={'Stan': stan_mod}, encoding='iso-8859-2')

