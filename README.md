# xml-transformations
Python scripts for working with XML.

## Multiple FITS XML to CSV
Takes a folder of File Information Tool Set (FITS) xml metadata files and saves the values from selected elements to a csv file with one row per xml file. Created for a file format analysis project.

## Multiple XML to CSV
Takes a folder of xml files and saves the values from selected elements to a csv file with one row per xml file. Made to use for quick data analysis using a spreadsheet. Can handle optional elements and repeating elements.

## Multiple XML to Multiple EAD
Takes a folder of xml files and transforms them to EAD files (a different XML standard). One EAD is made for each XML file.

## Multiple XML to One EAD
Takes a folder of xml files and combines them into one EAD file.

## PBCore to CSV
Takes a folder of PBCore xml files, extracts data from select fields and transforms if needed, and saves to a CSV file, one row per PBCore file.

## XML Replacement
Takes a folder of xml files. For each file, finds a particular element and updates the value of that element. Also creates a log of the changes.
