import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import sys


URL = 'http://localhost:9000'

r = requests.post(URL)

# this is the response xml text
xml = BeautifulSoup(r.text, "xml").textarea.contents[0]
print "xml text: ", xml

# search for all id attributes
#print ET.dump(ET.fromstring(str(xml))) # dump xml with namespace

nodes = ET.fromstring(str(xml)).findall(".//item")

print "items: " 
for n in nodes:	
	print "\t" + n.text

ids = []
for n in nodes: 
	ids.append(n.attrib['id'])

print "list of ids: "	
print ids
