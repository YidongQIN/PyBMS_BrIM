# import the ET API
import xml.etree.ElementTree as ET
tree = ET.parse('3 MARC CADD.xml')
root = tree.getroot()

marc_object=root.findall('O')
for a in marc_object:
	print(a.attrib)
