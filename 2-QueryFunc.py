import xml.etree.ElementTree as ET
# XML file
## read XML
def read_xml(in_path):
	tree = ET.parse(in_path)
	return tree
## write XML
def write_xml(tree, out_path):
	tree.write(out_path, encoding="utf-8",xml_declaration=True)
# search
##



# ----main----
tree = read_xml('0 MARC.xml')
root = tree.getroot()

a = root.iter('O')
for b in a:
	if 'Type' in b.keys():
		print(b.get('Type'))

