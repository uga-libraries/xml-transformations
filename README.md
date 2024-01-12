# XML Transformations

## Overview

Python scripts for working with XML, including transforming the data to CSVs, to EAD, and update values.
These were quickly developed for a one-time use, and are retained as a starting point for future scripts.

See also the FITS to preservation.xml transformation in [General AIP script](https://github.com/uga-libraries/general-aip)

## Getting Started

### Dependencies

Most of these scripts only use standard Python libraries.
The ElementTree library is used for working with the XML.

xmls-to-eads.py uses Saxon for XSLT transformations: [https://www.saxonica.com/](https://www.saxonica.com/)

### Installation

See the example input in each script's folder for guidance on how input should be formatted.

The values for variables in a few of the scripts must be edited prior to running them.

xmls-to-csv.py
   * Replace the path in os.chdir() with the folder containing the XML (line 16)

xmls-to-ead.py
   * Variable xml_directory (line 17): path to the folder containing the XML

xmls-to-eads.py
   * Variable xml_directory (line 17): path to the folder containing the XML
   * Variable saxon (line 18): path to Saxon jar file
   * Variable stylesheet (line 19): path to the xml-to-ead.xsl file in this repo


### Script Arguments

Some of these scripts require editing the variable within the script (see Installation), 
rather than getting the values from arguments.

fits-to-csv.py
   * target_directory (required): folder containing the FITS XML files

pbcore-to-csv.py
   * target_directory (required): folder containing the PBCore XML files

xml-element-value-replacement.py
   * xml_folder (required): folder containing the XML to be transformed

### Testing

Run the script on a small amount of your data, so you can easily predict the results, before running on a batch.

These scripts were written before we had procedures for creating testing procedures.
Additional testing guidance or unit tests will be written if they start getting used again.

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
