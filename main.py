# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *

newproj = PyOpenBrIMElmt('new proj')
print(newproj.elmt.attrib['N'])
newproj.read_xmlfile('xml file/test.xml')
new_node = ObjElmt('Line', 'object name', D='description of object', UC='test')
newproj.add_sub(new_node)
new_node2 = ObjElmt('Not Line', 'object2', D='des')
new_par = PrmElmt('test param', '666', 'de', par_type='p_tag')
new_node2.add_sub(new_par)
newproj.add_sub(new_node2)
newproj.show_sub()
print('--- change ---')
new_node2.update(D='this has been changed!')
point1 = Point(1,2,0,'point has no name')
newproj.add_sub(point1)
point1.show_self()
# new_node2_p.if_is_Parameter()
# <P> {'D': 'Concrete Compressive Strength', 'N': 'Fc28', 'Role': 'Input', 'V': '4'}
# newproj.del_sub('P',N='Fc28')
newproj.show_sub()
# newproj.save_project()