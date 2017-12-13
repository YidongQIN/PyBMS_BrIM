import PyOpenBrIM as ob

# ----main----
tree = ob.read_xml('0 MARC.xml')
root = tree.getroot()

# find the node
op = "*"
kv = {"T": "Material"}
results = ob.get_node_by_keyvalue(root.iter(op), kv)
if ob.select_OBJECT(results):
    ob.table_OBJECT(ob.select_OBJECT(results))

