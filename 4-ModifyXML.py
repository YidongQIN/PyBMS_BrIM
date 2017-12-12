import xml.etree.ElementTree as ET
import prettytable as pt

# read XML
def read_xml(in_path):
    tree = ET.parse(in_path)
    return tree
# write XML
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
# search by path
def find_nodes(tree, path):
    return tree.findall(path)
## search by key and value of attributes
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
# output format
def O_or_P(op):
    if op is 'O':
        return 'Object'
    elif op is 'P':
        return 'Parameter'
    else:
        return 'Not correct tag'
def other_attribute(dict):
    dict.pop('N')
    dict.pop('T')
    atts = ''
    for key, value in dict.items():
        atts = atts + key + '=' + value + ', '
    return atts

# ----change----
def change_node_properties(nodelist, kv_map, is_delete=False):
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))

def create_node(tag, property_map):
    element = ET.Element(tag, property_map)
    return element

def add_child_node(nodelist, element):
    for node in nodelist:
        node.append(element)

def del_node_by_tagkeyvalue(nodelist, tag, kv_map):
    '''同过属性及属性值定位一个节点，并删除之
       nodelist: 父节点列表
       tag:子节点标签
       kv_map: 属性及属性值列表'''
    for parent_node in nodelist:
        children = parent_node.getchildren()
        for child in children:
            if child.tag == tag and if_match(child, kv_map):
                parent_node.remove(child)

# ----main----

tree = read_xml('0 MARC.xml')
root = tree.getroot()

# input and search path
# path = input('input the path\n')
# result = find_nodes(root, path)

# input and search by attrib
# op = input('Object or Parameter? Type "O" or "P" in.\n')
# kv = input('Input attributes in format of dict {"key":"value",}')

# test
op = "O"
kv = {"T":"Material"}

# find the node
nodes = root.iter(op)
results = get_node_by_keyvalue(nodes, kv)

# modify the XML file
# modify_kv=input('Input new attribute')
modify_kv={"D":"This is concrete"}
change_node_properties(results,modify_kv)

# new node
new_node_kv = {"N":"Nu", "V":"0.2", "D":"Poisson's Ratio"}
a = create_node("P", new_node_kv)
add_child_node(results, a)

# output results
# new XML
write_xml(tree,"./new.xml")
