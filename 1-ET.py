# import the ET API
import xml.etree.ElementTree as ET
tree = ET.parse('0 MARC.xml')
root = tree.getroot()

# result: find all the child object element
print('find all the child object element')
marc_object=root.findall('O')
for a in marc_object:
	print(a.attrib)
print('-------------------')

# example: find all the child element
# marc_object=root.findall('O')
# for a in marc_object:
# 	print(a.attrib)
