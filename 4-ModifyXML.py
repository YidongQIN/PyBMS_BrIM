import xml.etree.ElementTree as ET
import prettytable as pt

# read XML
def read_xml(in_path):
    tree = ET.parse(in_path)
    return tree
# write XML
def write_xml(tree, out_path):
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
# search
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
# search by node path
def find_nodes(tree, path):
    return tree.findall(path)
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
        print(key, value)
        atts = atts + key + '=' + value + ', '
    return atts

# ----change----
def change_node_properties(nodelist, kv_map, is_delete=False):
    '''修改/增加 /删除 节点的属性及属性值
       nodelist: 节点列表
       kv_map:属性及属性值map'''
    for node in nodelist:
        for key in kv_map:
            if is_delete:
                if key in node.attrib:
                    del node.attrib[key]
            else:
                node.set(key, kv_map.get(key))

def change_node_text(nodelist, text, is_add=False, is_delete=False):
    '''改变/增加/删除一个节点的文本
       nodelist:节点列表
       text : 更新后的文本'''
    for node in nodelist:
        if is_add:
            node.text += text
        elif is_delete:
            node.text = ""
        else:
            node.text = text

def create_node(tag, property_map, content):
    '''新造一个节点
       tag:节点标签
       property_map:属性及属性值map
       content: 节点闭合标签里的文本内容
       return 新节点'''
    element = Element(tag, property_map)
    element.text = content
    return element

def add_child_node(nodelist, element):
    '''给一个节点添加子节点
       nodelist: 节点列表
       element: 子节点'''
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
# op = input('Object or Parameter? Type "O" or "P" please.\n')
# kv = input('Input attributes in format of dict \{ \}')
op = "O"
kv = {"T":"Node", "Y":"0"}
nodes = root.iter(op)
results = get_node_by_keyvalue(nodes, kv)

# output results
# PrettyTable
tb = pt.PrettyTable(["Tag","Name","Type","Other Attributes"])
tb.align["Other Attributes"]="l"
for anode in results:
    row = [anode.tag, anode.attrib.get("N"),anode.attrib.get("T"),other_attribute(anode.attrib)]
    tb.add_row(row)
print(tb)
