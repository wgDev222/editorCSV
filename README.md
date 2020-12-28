# editorCSV
CLI .csv/.xlsx files editor

# Usage

## .csv

```bash
python3 main.py ../cennik\(pln\)_2020-12-08_12-29\ 2.csv -o ../test.csv -a Family:test -r Lp -l 1 
```
-o - output file

-a - new headers Name:Value

-r - headers to remove

-l - line skipping

## .xlsx
The same way as with csv files. Editor finds out that it is excel file, on its own.

New files names are based on sheets names.
