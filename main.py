from BMS_BrIM.BrIM_ELMT import *


# test Material
mma = Material(2, 'ureal')
mma.set_property(d=100, Fy=55555, E=5000, a=0.005, b=23)
mma.set_dbconfig('fours', 'Material')
mma.describe('this is  just a mt')
mma.set_property(d=666)
mma.set_dbconfig('fours','Material')
a= mma.get_mongo_doc()
print("haha yes",a)

#test ProjGroups
new_proj=ProjGroups('NewProj')
new_proj.set_dbconfig()
new_proj.set_mongo_doc()


'''



test = PyOpenBrIMElmt('O', 'test name', a=666, b='madan')
newproj = PyOpenBrIMElmt("O", 'new proj')
new_node = PyOpenBrIMElmt('O', 'new node1', D='~ TEST ~ ', UC='test')
new_node2 = PyOpenBrIMElmt('O', 'new_node2', D='~ ~ TEST ~ ~')
new_par = PyOpenBrIMElmt('P', '666', par_type='p_tag')
pp = OBPrmElmt('  v ', 100)
pp2 = OBPrmElmt(' a ', '10.0')
pp.show_info()
pp2.show_info()

mat1 = OBMaterial('C4000Psi', 'Deck Concrete', 'Concrete')
mat1.mat_property(d='0.000002248', E=3604, a=0.000055, Fc28=4)
mat1.show_mat_table()

beam1.set_points(1,1,1,20,20,20)
print(beam1.__dict__)
print(point1.__dict__)



database='bridge_test',

ds201 = PyElmt('Sensor Test',201)
ds201.mysql_conn(**config)
info = ds201.mysql_read('sensorId', 'sensor', 'manufacturerName', 'modelNumber',fetch_type='one')

pp.attach_to(new_node)
new_node.attach_to(newproj)
new_node2.attach_to(newproj)
newproj.attach_to(test)
new_par.attach_to(test)
ShowTree(test)
test.findall_by_xpath('./P')
test.find_by_xpath('./O')

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
unit = NetworkUnit(114, config)
print(unit.get_unit_info())
print(unit.get_channel_install())

newline = StraightBeamGeo(100,0,1,math.sqrt(3),'section')
ShowTree(newline.model)
ppp=PlateFEM(10,20,30,'mat','PLPLP')
newline.geom()

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

line1=Line(point1, point2,sec1)
feline = FELine(node1,n2,sec1)

feline.show_sub()
feline.as_line(line1)
feline.show_sub()

newproj.save_project()
ShowTree(newproj)
print('---delete test---')
newproj.save_project('before del.xml')
newproj.del_all_sub()
newproj.check_del_sub(T='Line')
newproj.show_sub()
newproj.save_project('after del.xml')
newproj.check_del_sub('P',D='Density')
newproj.save_project()
newproj.show_info('','Y')
print('--- change attribute test ---')
newproj.show_sub()
new_node2.update(D='this has been changed!')
point1 = Point(1,2,0.2,'point1 has no name')
print(point1.elmt.attrib)
newproj.sub(point1)
point1.show_self()
newproj.check_del_sub('P',N='Fc28')
newproj.show_sub()
newproj.save_project()
print('---search test---')
newproj.findall_by_xpath('.//','Y')
print('---find all sub by key&value test----')
results=newproj.findall_by_attribute(N='test new_parameter')
print(results)
print(newproj.verify_attributes(T='Project'))
ResultsTable(results)

xx = PrmElmt("x_spacing", '108.3')
print(type(xx.value))
print(xx.value)

'''''
