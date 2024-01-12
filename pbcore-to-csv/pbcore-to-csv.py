"""Extracts portions of data from PBCore XML files and saves to a single CSV spreadsheet.

This script was created for the Brown Media Archives NHPRC project.

Parameters:
    * target_directory: the path to the folder containing the PBCore XML files

Returns:
    The output is one CSV file (combined-pbcore-records.csv) with data from every XML in the folder,
    saved to a folder (csv_output) in the same folder as the folder with the PBCore XML.
"""
import csv
import os
import re
import xml.etree.ElementTree as ET
from sys import argv

# Check if the required argument target directory is a directory and is a valid path.
# If not, prints an error and exits the script.
errors = []
if len(argv) == 2:
    if os.path.exists(argv[1]):
        if os.path.isdir(argv[1]):
            target_directory = argv[1]
        else:
            errors.append(f'Target directory "{argv[1]}" is not a directory.')
    else:
        errors.append(f'Target directory "{argv[1]}" is not a valid path.')
else:
    errors.append('Script usage is not correct.')
if len(errors) > 0:     
    for error in errors:
        print(error)
    print("\nScript usage: python3 '/path/pbcore_to_csv.py' 'path/target_directory'")
    exit()

print("\nData conversion in progress...")

# change current directory to directory containing pbcore files
os.chdir(target_directory)

# make new directory for csv output file in same parent folder as target directory, if it doesn't already exist
if not os.path.exists('../csv_output'):
    os.mkdir('../csv_output')

# make csv file to save output to named "combined-pbcore-records.csv"
csv_file = open('../csv_output/combined-pbcore-records.csv', 'w', newline='', encoding='UTF8')

# create csv writer object
csvwriter = csv.writer(csv_file)

# write header row to csv file
csvwriter.writerow(['id', 'formatDuration', 'formatMediaType', 'formatGenerations', 'dateCreated',
                    'formatDigital', 'formatStandard', 'formatFileSize', 'formatTracks'])

# create dictionary of namespace prefixes so that 'pbcore' prefix can be used in xpath below
ns = {'pbcore': 'http://www.pbcore.org/PBCore/PBCoreNamespace.html'}

# for each file in the directory, get values from select elements, reformat if needed, and save the results to variables
# if reformatting requires regular expressions, will save error message to variable if the pattern cannot be matched
# so script can continue running for other files and to alert staff
# then write all of the values from the variables to a row in the csv file
for file in os.listdir(target_directory):

    # skip if not an xml file
    if not file.endswith('.xml'):
        continue
    
    # parse xml file and get the root element
    ET.register_namespace('', "http://www.pbcore.org/PBCore/PBCoreNamespace.html")
    tree = ET.parse(file)
    root = tree.getroot()
    
    # id: get value of instantiationIdentifier with attribute source="File Name"
    # expected format of instantiationIdentifier is bmac_id.extension where extension is one or more lowercase letters
    # reformatting: remove "bmac_" and file extension, add suffix -digmaster
    for identifier in root.findall('./pbcore:instantiationIdentifier[@source="File Name"]', ns):
        try:
            regex = re.match('^bmac_(.+)\.[a-z]+', identifier.text)
            id = f'{regex.group(1)}-digmaster'
        except:
            id = 'error: could not reformat'
    
    # formatDuration: get value of instantiationDuration
    # reformatting: make HH:MM:SS by removing the semicolon and everything after it
    inst_duration = root.find('./pbcore:instantiationDuration', ns).text
    try:
        regex = re.match('^(\d{2}:\d{2}:\d{2});', inst_duration)
        formatDuration = regex.group(1)
    except:
        formatDuration = 'error: could not reformat'
    
    # formatMediaType: get value of instantiationMediaType 
    # reformatting: none
    formatMediaType = root.find('./pbcore:instantiationMediaType', ns).text
    
    # formatGenerations: always the same text
    formatGenerations = 'Digital Preservation Master'
        
    # dateCreated: get value of instantiationDate 
    # reformatting: make YYYY-MM-DD by removing the "T" and everything after it
    inst_date = root.find('./pbcore:instantiationDate', ns).text
    try:
        regex = re.match('^(\d{4}-\d{2}-\d{2})T', inst_date)
        dateCreated = regex.group(1)
    except:
        dateCreated = 'error: could not reformat'
    
    # formatDigital: get value of instantiationDigital
    # reformatting: none
    formatDigital = root.find('./pbcore:instantiationDigital', ns).text
    
    # formatStandard: get value of instantiationStandard
    # reformatting: none
    formatStandard = root.find('./pbcore:instantiationStandard', ns).text

    # formatFileSize: get value of instantiationFileSize
    # reformatting: Callie is checking if always in bytes or if need to do conversions based on unitOfMeasure attribute
    # in the meantime, this will put text in csv if it wasn't bytes to alert staff
    inst_size = root.find('./pbcore:instantiationFileSize', ns)
    if inst_size.attrib['unitsOfMeasure'] == 'byte':
        formatFileSize = f'{inst_size.text} bytes'
    else:
        formatFileSize = 'not in bytes'

    # formatTracks: get value of instantiationTracks 
    # reformatting: none
    formatTracks = root.find('./pbcore:instantiationTracks', ns).text
    
    # write selected values from the variables to a row in the csv file
    csvwriter.writerow([id, formatDuration, formatMediaType, formatGenerations, dateCreated,
                        formatDigital, formatStandard, formatFileSize, formatTracks])

# close csv file
csv_file.close()

print("Script complete")
