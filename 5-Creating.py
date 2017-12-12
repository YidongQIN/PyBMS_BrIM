import PyOpenBrIM

# ----main----
tree = read_xml('0 MARC.xml')
root = tree.getroot()

# find the node
# op = "*"
# kv = {"T": "Material"}
# results = get_node_by_keyvalue(root.iter(op), kv)
# if select_OBJECT(results):
#     table_OBJECT(select_OBJECT(results))

