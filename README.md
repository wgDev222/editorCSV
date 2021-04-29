# editorCSV
CLI .csv/.xlsx files editor

# Requirements
Pandas python module is required
```bash
pip3 install pandas 
pip3 install openpyxl
```

# Usage

```bash
python3 main.py file.csv -o test.csv -a [file.csv | Header:test...] -r [header1 header2...] -n [file.csv | Name:NewName...] -l [int]
```
 
## -o Specifies output pathname, if its not passed then changes are made to source file. When working with many sheets in Excel file, each one is saved in source file directory as sheet name

If you are using csv files as arguments first line must have headers, specified below.

Order of editing actions:
1. Adding
2. Removing
3. Renaming
4. Strping values
5. Deleting duplicate rows
6. Duplicating

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

## -s Striping character from values of given column only by file
Negative values strip characters from the end 

```csv
"Header";"Num";
"Model";"1"
"family";"-1"
```

## -c Duplicating headers by file or inline

```csv
"Header";"Header_D"
"Price";"Cena"
"Amount";"Ilosc"
```

```bash
Price:Cena Amount:Ilosc
```

## --dd Deleting duplicates considering specified columns 

```csv
"Header"
"Symbol"
"Nazwa"
```

```bash
Symbol Nazwa
```

## -l Number of lines to skip from start of source file, works only with .csv.

## -d Set Delimiter for input and output
