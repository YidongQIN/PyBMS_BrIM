from BMS_BrIM import *
import math



test=PyOpenBrIMElmt('O','test name', a=666, b='madan')
newproj = PyOpenBrIMElmt("O",'new proj')
new_node = PyOpenBrIMElmt('O', 'new node1', D='~ TEST ~ ', UC='test')
new_node2 = PyOpenBrIMElmt('O', 'new_node2', D='~ ~ TEST ~ ~')
new_par = PyOpenBrIMElmt('P', '666', par_type='p_tag')
pp = OBPrmElmt('  v ',100)
pp2 = OBPrmElmt(' a ','10.0')
pp.show_info()
pp2.show_info()

mat1=OBMaterial('C4000Psi','Deck Concrete','Concrete')
mat1.mat_property(d='0.000002248', E=3604, a=0.000055, Fc28=4)
mat1.show_mat_table()



# pp.attach_to(new_node)
# new_node.attach_to(newproj)
# new_node2.attach_to(newproj)
# newproj.attach_to(test)
# new_par.attach_to(test)
# ShowTree(test)
# test.findall_by_xpath('./P')
# test.find_by_xpath('./O')



'''

beam1.set_points(1,1,1,20,20,20)
print(beam1.__dict__)
print(point1.__dict__)

with ConnMongoDB('fours') as mgdb:
    mgdb.col_find_one('Parameter',{'value':{'$gt':200}})
    mgdb.findall_by_kv('Parameter','value', {'$gt':300})
    mgdb.find_by_kv('Parameter', 'name', 'ncol')
    mgdb.insert_elmt('Member', beam1)
    mgdb.find_by_kv('Member','_id', beamId)
    mgdb.update_elmt('Member',point1)
    mgdb.findall_by_kv('Member','name','PPP')
    mgdb.delete_elmt('Member',point1)
    mgdb.have_a_look('Member')


database='bridge_test',

config = dict(user='root', password='qyd123', host='127.0.0.1',
               port=3306,database='bridge_test',
              path='c:\\Users\\yqin78\\Proj.Python\\PyOpenBrIM\\server backup\\20180302_141015_19')
ds201 = PyElmt('Sensor Test',201)
ds201.mysql_conn(**config)
info = ds201.mysql_read('sensorId', 'sensor', 'manufacturerName', 'modelNumber',fetch_type='one')



with ConnMySQL(**config) as testconn:
    testconn.query('select * from bridge_test.sensor')
    print(testconn.fetch_row())
    print(testconn.backup_path)

ShowTree(proj)
proj.save_project()
config = dict(user='root', password='qyd123', host='127.0.0.1', database='bridge_test', port = 3306)
ex =Experiment(20,1, config)
print(ex.get_expt_info())
print(ex.get_bridge_info())
# unit = NetworkUnit(114, config)
# print(unit.get_unit_info())
# print(unit.get_channel_install())

# newline = StraightBeamGeo(100,0,1,math.sqrt(3),'section')
# ShowTree(newline.model)
ppp=PlateFEM(10,20,30,'mat','PLPLP')
# newline.geom()


text = Text3D('Text3D Object',0,0,0)
text.attach_to(proj)

di = Displacement(202,'Test dat path',config)
di.geom().attach_to(proj)
print(di.get_install())



config = dict(user='root', password='qyd123', host='127.0.0.1', database='bridge_test', port = 3306, path = 'c:\\Users\\yqin78\\Proj.Python\\PyOpenBrIM\\server backup\\20180327_161910_20\\U116_ADC_B2.dat')
di = Sensor(202,'Test dat path','test',config)
di.plot_dat()
print('file path'+di.datpath)
print('config: '+str(di.db))


test = BoltedPlate('Plate 0', 5, 50, 50, 6, 8, 8, 4, 4).as_prmodel()
test.attach_to(proj)
proj.save_project()

th = PrmElmt('thick',123,par_type='Thick')

point=[]
for i in range(4):
    point.append(Point(i,0,0))
shape1=Shape('s1',*point)
shape2=Shape('s2',*point)
shape2.is_cutout()
sec1=Section('sect',mat1,shape1,shape2)

point1=Point(0,0,0,'P1')
point2=Point(10,0,0,'P2')
point3=Point(20,0,0,'P2')
point4=Point(30,0,0,'P2')
n3 = FENode(0,100,0)
n3.as_point(point3)
n3.show_info()

node1 = FENode(1,2,2,'nananan')
n2 =FENode(0,0,0,'adf')

line1=Line(point1, point2,sec1)
feline = FELine(node1,n2,sec1)

feline.show_sub()
feline.as_line(line1)
feline.show_sub()




newproj.save_project()
ShowTree(newproj)
# print('---delete test---')
# newproj.save_project('before del.xml')
# newproj.del_all_sub()
# newproj.check_del_sub(T='Line')
# newproj.show_sub()
# newproj.save_project('after del.xml')
# newproj.check_del_sub('P',D='Density')
# newproj.save_project()
# newproj.show_info('','Y')
# print('--- change attribute test ---')
# newproj.show_sub()
# new_node2.update(D='this has been changed!')
# point1 = Point(1,2,0.2,'point1 has no name')
# print(point1.elmt.attrib)
# newproj.sub(point1)
# point1.show_self()
# newproj.check_del_sub('P',N='Fc28')
# newproj.show_sub()
# newproj.save_project()
# print('---search test---')
# newproj.findall_by_xpath('.//','Y')
# print('---find all sub by key&value test----')
# results=newproj.findall_by_attribute(N='test new_parameter')
# print(results)
# print(newproj.verify_attributes(T='Project'))
# ResultsTable(results)

xx = PrmElmt("x_spacing", '108.3')
print(type(xx.value))
print(xx.value)

'''''
