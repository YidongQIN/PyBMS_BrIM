import xml.etree.ElementTree as ET
import PyOpenBrIM

# ----main----

# find the node
search_method = input('Search by 1.Path or 2.Attributes?\n')
if search_method is '1':
    path='./O/P'
    # path = input('input the path in Xpath format\n')
    results = find_nodes(root, path)
else:
    # op = input('Object or Parameter? Type "O" or "P"\n')
    # kv = input('Input attributes in format of dict {"key":"value",}')
    op = "*"
    kv = {"T": "Material"}
    # kv = {"D": "modulus of elasticity"}
    results = get_node_by_keyvalue(root.iter(op), kv)

if select_OBJECT(results):
    table_OBJECT(select_OBJECT(results))
if select_PARAMETER(results):
    table_PARAMETER(select_PARAMETER(results))
