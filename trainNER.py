import os
import io
import re
import glob
import xml.etree.ElementTree as xmlparser

jdCombined = "jdcombined.txt"

## import tags, extract skill list
tags = []
root = xmlparser.parse("Tags/StackTags.xml").getroot()
for child in root.iter('row'):
    tags.append(child.attrib['TagName'])

## import JDs and perform data cleansing
lineStream = open(jdCombined, "w+")
regex = re.compile("[^0-9a-zA-Z#.+!@%&'/?,-]+")
filenames = glob.glob("JDs/*")
for filename in filenames:
    try: 
        with io.open(filename) as file:
            for line in file:
                if line.rstrip():
                    text = regex.sub(' ', line)   
                    ## Replace skill list words in JDs with skill tags for training   
                    for tag in tags:
                        text = text.replace(' {0} '.format(tag), ' <START:skill> {0} <END> '.format(tag))
                    lineStream.write(text)
        lineStream.write("\r\n\n")
    except:
        print ("The file %s threw an error" % filename)


## train the NER
os.system("opennlp TokenNameFinderTrainer -model en-ner-skill.bin -lang en -data jdcombined.txt -encoding UTF-8")


