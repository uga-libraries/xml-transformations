"""Copy data from multiple Dublin Core XML files into a single CSV spreadsheet.

This script was created to get a quick overview f the contents of XML before doing batch transformations,
to identify any complications that need to be addressed.
Look for things like empty fields, abbreviations to spell out, and different ways that dates are formatted.

The xml this script is designed for had all elements as direct children of the root.
All elements could be optional and could be repeated.
    
Before running the script, put all xml files to be included in the csv into a folder.
Enter the path for that folder in line 10.
"""
import os
import xml.etree.ElementTree as ET
import csv

# change to directory containing xml input files
os.chdir('INSERT PATH TO FOLDER WITH XML HERE')

# make csv file to save data to
csv_file = open('../combined-xml.csv', 'w', newline='', encoding='UTF-8')
csvwriter = csv.writer(csv_file)

# add header row to the csv file
csvwriter.writerow(['title', 'identifier', 'source', 'coverage', 'date', 'publisher', 'description',
                    'subject', 'altid'])

# iterate over each xml file and create a row in the csv file
for file in os.listdir('.'):
    
    # read the xml file
    tree = ET.parse(file)
    root = tree.getroot()

    # store the values of each element of interest as variables to be written to a csv row later.
    for dc in root.findall('.'):

        # get the value(s) from the title element(s), which may appear 0, 1, or multiple times.
        # this block of code (line 39-54) is then repeated for every element to be included in the csv.
        title = dc.findtext('title')
        # if there is no title element, put a value of "N/A" in the csv.
        if title is None:
            title = "N/A"
        else:
            # find all instances of title, temporarily save to a list, and then combine all titles from the list
            # into a single string with a | between each title.
            title_list = []
            for title in dc.findall('title'):
                title_list.append(title.text)
                # if a title element is empty, it will return None which will give an error when try to join.
                # remove None from the list and display a message in the terminal so we know there are blanks.
                if None in title_list:
                    title_list.remove(None)
                    print("title has empty tags")
                # this is the value that is going to be in the csv.
                title = ' | '.join(title_list)

        id = dc.findtext('identifier')
        if id is None:
            id = "N/A"
        else:
            id_list = []      
            for id in dc.findall('identifier'):
                id_list.append(id.text)
                if None in id_list:
                    id_list.remove(None)
                    print("identifier has empty tags")
                id = ' | '.join(id_list)

        source = dc.findtext('source')
        if source is None:
            source = "N/A"
        else:
            source_list = []
            for source in dc.findall('source'):
                source_list.append(source.text)
                if None in source_list:
                    source_list.remove(None)
                    print("source has empty tags")
                source = ' | '.join(source_list)

        cov = dc.findtext('coverage')
        if cov is None:
            cov = "N/A"
        else:
            cov_list = []
            for cov in dc.findall('coverage'):
                cov_list.append(cov.text)
                if None in cov_list:
                    cov_list.remove(None)
                    print("coverage has empty tags")
                cov = ' | '.join(cov_list)

        date = dc.findtext('date')
        if date is None:
            date = "N/A"
        else:
            date_list = []
            for date in dc.findall('date'):
                date_list.append(date.text)
                if None in date_list:
                    date_list.remove(None)
                    print("date has empty tags")
                date = ' | '.join(date_list)

        pub = dc.findtext('publisher')
        if pub is None:
            pub = "N/A"
        else:
            pub_list = []
            for pub in dc.findall('publisher'):
                pub_list.append(pub.text)
                if None in pub_list:
                    pub_list.remove(None)
                    print("publisher has empty tags")
                pub = ' | '.join(pub_list)

        desc = dc.findtext('description')
        if desc is None:
            desc = "N/A"
        else:
            desc_list = []
            for desc in dc.findall('description'):
                desc_list.append(desc.text)
                if None in desc_list:
                    desc_list.remove(None)
                    print("description has empty tags")
                desc = ' | '.join(desc_list)
       
        sub = dc.findtext('subject')
        if sub is None:
            sub = "N/A"
        else:
            sub_list = []
            for sub in dc.findall('subject'):
                sub_list.append(sub.text)
                if None in sub_list:
                    sub_list.remove(None)
                    print("subject has empty tags")
                sub = ' | '.join(sub_list)

        altid = dc.findtext('identifier.alternate')
        if altid is None:
            altid = "N/A"
        else:
            altid_list = []
            for altid in dc.findall('identifier.alternate'):
                altid_list.append(altid.text)
                if None in altid_list:
                    altid_list.remove(None)
                    print("identifier.alternate has empty tags")
                altid = ' | '.join(altid_list)                

    # Write all the values for the xml file to a row in the csv file
    csvwriter.writerow([title, id, source, cov, date, pub, desc, sub, altid])

# close csv file
csv_file.close()

print("Done!")
