"""Replaces the value of a single element with a different value for every XML file in a folder.

This script currently replaces dates of 2012 with 1912,
but has patterns for finding different kinds of elements to use for new scripts.

Parameters:
    xml_folder: path to the folder with the XML to be updated

Returns:

    The script will overwrite the existing XML file with the updated value and create a log of the changes.
"""
import csv
import os
import sys
import xml.etree.ElementTree as et

# Gets the XMLs folder from script argument and makes it the current directory.
# If it is missing or not a valid directory, prints an error and quits the script.
try:
    xml_folder = sys.argv[1]
    os.chdir(xml_folder)
except (IndexError, FileNotFoundError, NotADirectoryError):
    print("Path to the XML folder was not provided or is not a valid directory.")
    exit()

# Calculates how many XML are updated to verify it changed everything.
total_xml = 0
errors_xml = 0

# Makes a CSV to save the status of each of the files.
# Will need to update the status messages once know what we're looking for and what can go wrong.
log_file = open("log.csv", "w", newline="")
log = csv.writer(log_file)
log.writerow(["File Name", "Status"])

for file in os.listdir("."):

    # Skip if not xml
    if not file.endswith(".xml"):
        continue

    total_xml += 1

    # Read the data from the xml file.
    tree = et.parse(file)
    root = tree.getroot()

    # Find an element where no element is never repeated.
    title = root.find("header/title")

    # Find an element that is repeated but has different attributes.
    date = root.find("header/date[@type='created']")

    # Find an element that is repeated based on its position.
    first_subject = root.find("body[2]/paragraph[1]/subject")

    # Verify the text of the element is expected. If it is, change the value in the file.
    # If element was missing, find returns None rather than an error. But None.text will give an error.
    try:
        if date.text == "2012":
            date.text = "1912"
            tree.write(file)
            log.writerow([file, "Text Updated"])
        else:
            log.writerow([file, "Text Not Updated"])
    except AttributeError:
        errors_xml += 1
        log.writerow([file, "Element is missing"])

print(f"Script completed. {total_xml} XML processed. {errors_xml} had errors.")
