import PyOpenBrIM as ob


root = tree.getroot()


# find the node
search_method = input('Search by 1.Path or 2.Attributes?\n')
if search_method is '1':
    path = './O/P'
    # path = input('input the path in Xpath format\n')
    results = ob.find_nodes(root, path)
else:
    # op = input('Object or Parameter? Type "O" or "P"\n')
    # kv = input('Input attributes in format of dict {"key":"value",}')
    op = "*"
    kv = {"T": "Material"}
    # kv = {"D": "modulus of elasticity"}
    results = ob.get_node_by_keyvalue(root.iter(op), kv)

if ob.select_OBJECT(results):
    ob.table_OBJECT(ob.select_OBJECT(results))
if ob.select_PARAMETER(results):
    ob.table_PARAMETER(ob.select_PARAMETER(results))


# modify the XML file
# modify_kv=input('Input new attribute')
modify_kv = {"D": "This is concrete"}
ob.change_node_attributes(results, modify_kv)

# creat new node
# new_node_tag = input('Input the tag of new node')
# new_node_kv = input('Input the attributes of new node')
new_node_tag = 'P'
new_node_kv = {"N": "Nu", "V": "0.2", "D": "Poisson's Ratio"}
a = ob.create_node(new_node_tag, new_node_kv)
ob.add_subNode(results, a)

print(results)
print(a)

# delete node
# del_tag=input('Input the tag of the node to delete')
# del_attribute=input('Input the attributes of the node to delete')
del_tag = "P"
del_attribute = {"N": "Fy"}
ob.del_node_by_tagkeyvalue(results, del_tag, del_attribute)

# output results in new XML
ob.write_xml(tree, "xx.xml")
print('tree is ')
print(tree)
