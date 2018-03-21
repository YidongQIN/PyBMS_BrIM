# import ClassPyOpenBrIM
from ClassPyOpenBrIM import *

print('demo for ClassPyOpenBrIM')
newproj = PyOpenBrIMElmt('new proj')
newproj.parse_xmlfile('xml file/test.xml')
unit1=Unit('first unit')
ShowTable(unit1)

mat1=Material('C4000Psi','Deck Concrete','Concrete')
mat1.set_pars(d='0.000002248',E=3604,a=0.000055,Fc28=4)
mat1.show_mat()

point=[]
for i in range(4):
    point.append(Point(i,0,0))

shape1=Shape('s1',*point)
shape2=Shape('s2',*point)
shape2.is_cutout()
shape2.show_sub()

sec1=Section('sect',mat1,shape1,shape2)
ShowTree(sec1)

point1=Point(0,0,0,'P1')
point2=Point(10,0,0,'P2')
point3=Point(20,0,0,'P2')
point4=Point(30,0,0,'P2')

line1=Line(point1)
line1.attach_to(newproj)

sur1=Surface(point1,point2,point3,point4,50,'mat1','name of surface')
sur1.attach_to(newproj)
par1=PrmElmt('par', 'value')
par1.attach_to(newproj)
# --- Test on basic methods of OpenBrIM class---
print('---add sub nodes test---')
new_node = ObjElmt('Line', 'new node1', D='~ TEST ~ ', UC='test')
new_node2 = ObjElmt('Not Line', 'new_node2', D='~ ~ TEST ~ ~')
new_par = PrmElmt('test parameter', '666', '$$$$$$$$$$$', par_type='p_tag')
new_node2.add_sub(new_par)
newproj.add_sub(new_node2, new_node)
newproj.node_struc('Y','Y')
print('---delete test---')
newproj.save_project('before del.xml')
newproj.del_sub(T='Line')
newproj.del_sub('P',D='Density')
newproj.save_project('after del.xml')
newproj.del_all_sub()
newproj.save_project('after all del.xml')
print('--- change attribute test ---')
newproj.show_sub()
new_node2.update(D='this has been changed!')
newproj.save_project()
print('---search test---')
newproj.findall_by_xpath('.//','Y')
print('---find all sub by key&value test----')
results=newproj.findall_by_attribute(N='test param')
print(newproj.verify_attributes(T='Project'))
ResultsTable(results)
