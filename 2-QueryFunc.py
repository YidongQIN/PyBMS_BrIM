# import the ET API

import xml.etree.ElementTree as ET
tree = ET.parse('0 MARC.xml')
root = tree.getroot()

print('---root.get---')
print(root.get('N'))
print('---root.items---')
a = root.items()
print(a[1])
print('---root.attrib---')
b = root.attrib
print(b['T'])

