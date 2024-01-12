"""Extracts portions of data from FITS XML files and saves to a CSV spreadsheet.

This script was created for a format analysis project.
It gets format information for each file in the FITS XML and saves it as a row in a CSV.

Parameters:
    * target_directory: the path to the folder containing the FITS XML files

Returns:
    The output is one CSV file (combined-file-formats.csv) with data from every XML in the folder,
    saved to a folder (csv_output) in the parent folder of the folder with the FITS XML.
"""
import os
import os.path
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from sys import argv

errors = []     # create a variable to hold error messages
if len(argv) == 2:        # if we are passed two arguments
    if os.path.exists(argv[1]):     # check if target directory exists
        if os.path.isdir(argv[1]):  # check if target directory is a directory
            target_directory = argv[1]
        else:
            errors.append(f'Target directory "{argv[1]}" is not a directory.')  # if not a directory, add to error messages
    else:
        errors.append(f'Target directory "{argv[1]}" does not exist.')  # if it does not exist, add to error messages
else:
    print("Please specify a target directory")
    exit()

if len(errors) > 0:     # if there are errors, print each error message
  for error in errors:
    print(error)
    exit()

print("Converting xml data to csv...")

# change to directory containing xml input files
os.chdir(target_directory)

# make new directory for csv output file
os.mkdir('../csv_output')

# open csv file for writing
csv_file = open('../csv_output/combined-file-formats.csv', 'w', newline = '', encoding = 'UTF8')

# create csv writer object
csvwriter = csv.writer(csv_file)

# write header row to csv file
csvwriter.writerow(['file_path', 'puid', 'format_name', 'format_version', 'mime_type', 'date_last_modified'])

# iterate over files in target directory
for file in os.listdir(target_directory):
    # parse XML file and get root of tree
    ET.register_namespace('',"http://hul.harvard.edu/ois/xml/ns/fits/fits_output")
    tree = ET.parse(file)
    root = tree.getroot()

    # for each fits element, find specified children and store as variables to be written to csv row later
    for fits in root.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fits'):

        for filepath in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}filepath'):
            file_path = filepath.text

        # check if externalIdentifier element is present in fits record; if not, returned value will be "puid_unknown"
        puid = fits.findtext('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}externalIdentifier')
        if puid is None:
            puid = "puid_unknown"
        else:
            puid_list = []
            for externalIdentifier in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}externalIdentifier'):
                puid_list.append(externalIdentifier.text)
                # check if there are empty externalIdentifier elements, which will return value of 'None', and remove them from the list ('None' values cannot be converted to strings in next step)
                if None in puid_list: puid_list.remove(None)
                puid = ' | '.join(puid_list)

        # find all identified format names and mime types and combine into a list
        format_name_list = []
        mime_type_list = []
        for identity in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}identity'):
                format_name_list.append(identity.attrib['format'])
                format_name = ' | '.join(format_name_list)
                mime_type_list.append(identity.attrib['mimetype'])
                mime_type = ' | '.join(mime_type_list)

        # check if version element is present in fits record; if not, returned value will be "version_unknown"
        format_version = fits.findtext('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}version')
        if format_version is None:
            format_version = "version_unknown"
        else:
            format_version_list = []
            for version in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}version'):
                format_version_list.append(version.text)
                # check if there are empty version elements, which will return value of 'None', and remove them from the list ('None' values cannot be converted to strings in next step)
                if None in format_version_list: format_version_list.remove(None)
                format_version = ' | '.join(format_version_list)

        # use date last modified as identified by the file system unix time stamp
        for fslastmodified in fits.findall('.//{http://hul.harvard.edu/ois/xml/ns/fits/fits_output}fslastmodified'):
            # convert unix time stamp to an integer and then reformat to YYYY
            date_last_modified = datetime.fromtimestamp(int(fslastmodified.text) / 1e3).strftime('%Y')

        # write selected xml text nodes to csv file, one row for each fits entry
        csvwriter.writerow([file_path, puid, format_name, format_version, mime_type, date_last_modified])

# close csv file
csv_file.close
print("Script complete")
