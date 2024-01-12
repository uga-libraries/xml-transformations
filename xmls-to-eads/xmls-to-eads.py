"""Transform each Dublin Core XML in a folder into an EAD finding aid.

This script was used to create batch create an EAD finding aid for each map described in a database.
The database exported one xml file per copy of each map.

The xml this script is designed for had all elements as direct children of the root.
Some elements were optional and some could be repeated.
    
Before running the script, put all xml files to be included in the csv into a folder.
Enter the path for that folder in line 18.
Also enter the path for the xslt processor and xslt stylesheet (lines 20-21).
"""

import os
import pathlib
import re
import subprocess

# locations of xml, xslt program (Saxon), and stylesheet
xml_directory = 'INSERT PATH TO FOLDER WITH XML HERE'
saxon = 'INSERT PATH TO SAXON HERE'
stylesheet = 'INSERT PATH TO xml-to-ead.xsl STYLESHEET HERE'

os.chdir(xml_directory)

# count the number of copies of each map, where filenames are formatted idcopy#.xml.
# base is the filename without the 'copy#' part. Ex: base of hmapab12copy2.xml is hmapab12.xml
base_list=[]

for file in os.listdir(xml_directory):
    # find the string 'copy' followed by a single digit and replace it with nothing to remove it. 
    file_base = re.sub(r'copy\d', r'', file)
    base_list.append(file_base)

# the number of times each base appears is saved to a dictionary for later reference.
base_count = {i:base_list.count(i) for i in base_list}

# iterate over each xml file and use xslt stylesheet to make the EAD.
for file in os.listdir(xml_directory):
    # skip if copy is part of filename so get one EAD per unique title.
    if 'copy' in file:
        continue
    
    # look up the number of copies from the base_count dictionary to use in an extent note.
    count = base_count[file]
    
    # run stylesheet on XML file to produce an EAD file.
    # the EAD file is named mapid-ead.xml, for example hmapab12-ead.xml.
    # count is a parameter that passes the number of copies to the stylesheet so it can be included in the EAD.
    subprocess.run(f'java -cp {saxon} net.sf.saxon.Transform -s:{file} -xsl:{stylesheet} -o:../{pathlib.Path(file).stem}-ead.xml count="{count}"', shell=True)
