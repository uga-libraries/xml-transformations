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
   * Update the element being search for using the root.find() lines as an example.

### Testing

Run the script on a small amount of your data, so you can easily predict the results, before running on a batch.

These scripts were written before we had procedures for creating testing procedures.
Additional testing guidance or unit tests will be written if they start getting used again.

## Workflow

The majority of the scripts get the contents from every XML file in a folder, edit the data, 
and export it to either a CSV file or EAD file(s).
The exception is xml-element-value-replacement.py, which updates the value of an element in an XML file.

See the comments at the top of each script for further details.

## Author

The primary author was Adriane Hanson, Head of Digital Stewardship at the University of Georgia Libraries,
with contributions from Brandon Pieczko, Digital Archivist at the Russell Library.
