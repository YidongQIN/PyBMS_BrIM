import PyOpenBrIM as ob
import xml.etree.ElementTree as ET

# ----main----


root_attrib = {"Alignment":"None" , "N":"new" , "T":"Project" , "TransAlignRule":"Right"}
root = ob.create_node('O',root_attrib)
node1_attrib = {"N":"Units","T":"Group"}
node1 = ob.create_node('O', node1_attrib)

root = ob.find_nodes(root,'.')

tree = ET.ElementTree(root)
tree.write('xx.xml')
