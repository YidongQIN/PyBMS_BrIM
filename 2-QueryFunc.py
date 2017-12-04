# import the ET API
import xml.etree.ElementTree as ET
tree = ET.parse('0 MARC.xml')
root = tree.getroot()
