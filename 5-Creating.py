import PyOpenBrIM as ob
from xml.etree.ElementTree import *

# ----main----
tree = ob.read_xml('new_proj.xml')
root = tree.getroot()

ob.write_xml(tree, "./new_proj.xml")
