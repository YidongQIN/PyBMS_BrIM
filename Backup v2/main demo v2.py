# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *

newproj = PyOpenBrIMElmt('new proj')
newproj.read_xmlfile('test.xml')
new_node = ObjElmt('Line', 'object name', D='description of object', UC='test')
newproj.add_sub(new_node)
new_node2 = ObjElmt('Not Line', 'object2', D='des')
add_child_node(newproj, new_node2)
newproj.save_project('new path.xml')
findall = newproj.findall_by_xpath('.//')
ResultsTable(findall)
