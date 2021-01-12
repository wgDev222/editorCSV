# editorCSV
CLI .csv/.xlsx files editor

# Usage

```bash
python3 main.py file.csv -o test.csv -a [file.csv | Header:test...] -r [header1 header2...] -n [file.csv | Name:NewName...] -l [int]
```
 
## -o Specifies output pathname, if its not passed then changes are made to source file. When working with many sheets in Excel file, 
each one is saved in source file directory as sheet name

## -a Adding new headers by file or inline

```csv
"Name";"Value"
"family";"Test"
"Price";"0"
```

```bash
family:Test Price:0
```

## -r Removing header by file or inline

```csv
"Header"
"Family"
"Cena"
```

```bash
Family Cena
```
## -n Renaming headers by file or inline

```csv
"Name";"NewName"
"Price";"Cena"
"family";"Family"
```

```bash
Price:Cena family:Family
```

## -l Number of lines to skip from start of source file, works only with .csv.

## -d Set Delimiter for input and output
