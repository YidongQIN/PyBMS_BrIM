import xml.etree.ElementTree as ET

# ParamML XML file
## read XML
def read_xml(in_path):
	tree = ET.parse(in_path)
	return tree
## write XML
def write_xml(tree, out_path):
	tree.write(out_path, encoding="utf-8",xml_declaration=True)
# search
## search by attrib
def if_match(node, kv_map):
    for key in kv_map:
        if node.get(key) != kv_map.get(key):
            return False
    return True

def get_node_by_keyvalue(nodelist, kv_map):
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes
## search by path
def find_nodes(tree, path):
    return tree.findall(path)
# ----main----
tree = read_xml('0 MARC.xml')
root = tree.getroot()

