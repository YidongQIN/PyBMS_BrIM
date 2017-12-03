# import the ET API
import xml.etree.ElementTree as ET
tree = ET.parse('0 MARC.xml')
root = tree.getroot()

# find all the child element
marc_object=root.findall('O')
for a in marc_object:
	print(a.attrib)

