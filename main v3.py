# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *
import PyOpenBrIM as pob

newproj=PyOpenBrIMElmt('new proj')
newproj.read_xmlfile('test.xml')
new_node=ObjElmt('Line','wo cao name',D='TMD',UC='buzhid')
# newproj.add_sub(new_node)
add_child_node(newproj.elmt,new_node.elmt)
newproj.save_project('new path.xml')
findall=newproj.findall_by_xpath('.//')
ResultsTable(findall)