
root = ET.Element('ParamML')
node1 = ET.Element('Node1',{'name':'China'})
root.append(node1)
tree = ET.ElementTree(root)
tree.write('append_proj.xml')
