# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *

newproj = PyOpenBrIMElmt('new proj')
# newproj.read_xmlfile('xml file/test.xml')
newproj.read_xmlfile('new path')
# new_node = ObjElmt('Line', 'object name', D='description of object', UC='test')
# newproj.add_sub(new_node)
# new_node2 = ObjElmt('Not Line', 'object2', D='des')
# new_par = PrmElmt('test param','666','de',par_type='p_tag')
# # new_par.show_it()
# add_child_node(new_node2,new_par)
# add_child_node(newproj, new_node2)
# newproj.show_sub()
#
# newproj.save_project('new path.xml')
# findall = newproj.findall_by_xpath('.//')
# ResultsTable(findall)

# projec= PyOpenBrIMElmt('test for format')
# projec.new_project()
# projec.save_project()