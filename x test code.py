# 以下代码成功的创建了xml并输入信息，可用于对比
root = ET.Element('ParamML')
node1 = ET.Element('Node1',{'name':'China'})
root.append(node1)
tree = ET.ElementTree(root)
tree.write('xx.xml')

# iter和findall对比，返回的结果都是element
for node in root.iter():
    print(node,node.attrib)

for node in root.findall('*'):
    print(node, node.attrib)

