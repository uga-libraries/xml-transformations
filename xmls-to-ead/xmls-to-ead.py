# Purpose: take data from multiple xml files and combine them into a single dsc section of an EAD finding aid.

"""Combine data from multiple Dublin Core XML files into a single dsc section for an EAD finding aid.

This script was used to create a single finding aid for a group of items that were described individually in a database.
The database exported one xml file per item.

The xml this script is designed for had all elements as direct children of the root.
Some elements were optional and some could be repeated.
    
Before running the script, put all xml files to be included in the EAD into a folder.
Enter the path for that folder in line 17.

After running the script, paste everything into an xml file (template-ead.xml in this repo)
that has the collection-level elements needed to be able to import it into Archivists' Toolkit for further editing.
"""
import xml.etree.ElementTree as ET
import os
import re

xml_directory = 'INSERT PATH TO FOLDER WITH XML HERE'

# make a new xml document, with a root element named dsc.
combo = ET.ElementTree(ET.Element('dsc'))
combo_root = combo.getroot()

# iterate over each xml file and make the c01 element and all its children.
for xml in os.listdir(xml_directory):

    # read the xml file.
    ET.register_namespace('xtf', "http://cdlib.org/xtf")
    tree = ET.parse(f'{xml_directory}/{xml}')
    root = tree.getroot()
    
    # get values from xml and store in variables, transforming if needed (lines 31-90).
    # each variable has the value for one EAD element.
    title = ''
    for title in root.findall('title'):
        title = title.text
        
    identifier = ''
    for id in root.findall('identifier'):
        identifier = id.text
        
    publisher = ''
    for pub in root.findall('publisher'):
        publisher = pub.text
        
    description = ''
    for desc in root.findall('description'):
        description = desc.text
    
    # combine publisher and description to use for the scope and content note.
    # an xml file may have both, only one, or neither of these two elements.
    scope = ''
    if publisher == '':
        # if there isn't publisher or description.
        if description == '':
            scope = 'empty'
        # if there is only description.
        else:
            scope = description
    else:
        # if there is only publisher.
        if description == '':
            scope = f'Publisher: {publisher}'
        # if there is publisher and description.
        else:
            scope = f'Publisher: {publisher}; {description}'
    
    # format the date information.
    # get start and end year to use for the normal attribute in EAD.
    # get coverage (a separate date element in the xml) which gives information on if the date is approximate or not.
    coverage = ''
    for coverage in root.findall('coverage'):
        coverage = coverage.text
    
    date = ''
    start_year = ''
    end_year = ''
    for date in root.findall('date'):
        # the date is a year range, which is formatted YYYY-YYYY
        if '-' in date.text:
            regex = re.match(r'(\d{4})-(\d{4})', date.text)
            start_year = regex.group(1)
            end_year = regex.group(2)
        # the date is a single year, which is formatted YYYY
        else:
            start_year = date.text
            end_year = date.text

        # if any of these three characters are in coverage, the date is approximate.
        if 's' in coverage or '[' in coverage or 'ca.' in coverage:
            date = f'circa {date.text}'
        else:
            date = date.text

    # make the EAD, which is a c01 element and all its children.
    
    root = ET.Element('c01', level="item")
    did = ET.SubElement(root, 'did')
    ET.SubElement(did, 'unittitle').text = title
    ET.SubElement(did, 'container', type="Item").text = identifier
    
    if date == 'n.d.' or date == 'n.d,':
        ET.SubElement(did, 'unitdate').text = 'undated'
    else:
        ET.SubElement(did, 'unitdate', normal=f'{start_year}/{end_year}').text = date
    
    if scope != 'empty':
        sc = ET.SubElement(root, 'scopecontent')
        ET.SubElement(sc, 'head').text = 'Scope and Contents note'
        ET.SubElement(sc, 'p').text = scope
    
    # add the c01 for this xml file to the dsc element.
    combo_root.append(root)

# save all the c01s to the xml file.    
combo.write('H:/python/hargrett/broadsides/dsc.xml')
