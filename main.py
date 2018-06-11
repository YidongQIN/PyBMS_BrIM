from BMS_BrIM import *
import json
#
# story_num = OBPrmElmt('Storey_Number', 4, role='Input')  # 4 storey means 5 plates
# height = OBPrmElmt('Height', 300.0, des='Vertical space between two storeys', role='Input')
# height_top = OBPrmElmt('Height_top', 270.0, 'Height of the top story', role='Input')
# t_plate = OBPrmElmt('t', 13, 'Thickness of each plate', role='Input')
# l_plate = OBPrmElmt('l', 405.0, 'Length of each plate', role='Input')
# w_plate = OBPrmElmt('w', 303.0, 'Width of each plate', role='Input')
# d_hole = OBPrmElmt('d', 6.0, 'Diameter of hols in the plate', role='Input')
# x_clear = OBPrmElmt('x_clear', 50.0, 'x clearance from the edge to the hole', role='Input')
# y_clear = OBPrmElmt('y_clear', 24.0, 'y clearance from the edge to the hole', role='Input')
# x_num = OBPrmElmt('ncol', 7, 'Column Number of holes', role='Input')
# y_num = OBPrmElmt('nrow', 11, 'Column Number of holes', role='Input')
# t_colm = OBPrmElmt('Thick_column', 1.0, 'Thickness of each column', role='Input')
# w_colm = OBPrmElmt('Width_column', 25.0, 'Width of each column', role='Input')
# in_1 = OBPrmElmt('Interval_1', 36.2, 'interval from edge to the first column', role='Input')
# in_2 = OBPrmElmt('Interval_2', 26.8, 'interval from the first column to the second column', role='Input')
# in_3 = OBPrmElmt('Interval_3', 77.0, 'interval from the first column to the second column', role='Input')
# # the track? maybe not
# d_track = OBPrmElmt('TrackDiameter', 18.0)
# h1_track = OBPrmElmt('h1_track', 23.0)
# h2_track = OBPrmElmt('h2_track', 6.0)
# b_track = OBPrmElmt('Width_track', 49.0)
#
#
# col_rect = OBShape('rectangle',
#                    OBPoint(-w_colm.value / 2, -t_colm.value / 2),
#                    OBPoint(w_colm.value / 2, -t_colm.value / 2),
#                    OBPoint(w_colm.value / 2, t_colm.value / 2),
#                    OBPoint(-w_colm.value / 2, t_colm.value / 2))

testmg=PyElmt('Beam','Beam_1_1','Column_0,48.7')
testmg.set_database(database='fours')
result= testmg.mongo_read('Member')
print(result)
print(result['Section'])

'''
class combine(StrainGauge, Beam):

    def __init__(self, id, des, db, name):
        super(combine, self).__init__(id,des,db)
        print(self.name)
        self.name=name
        print('init find dir()')
        print(dir())
        print('==========')

    def attr_json(self):
        super(combine, self).attr_json()
        _d={}
        for k,v in self.__dict__.items():
            print("  - {}: {}".format(k,v))
            _d[k]=str(v)
        js = json.dumps(_d,sort_keys=True, indent=4)
        return js



if __name__ == '__main__':
    config = dict(user='root', password='qyd123', host='127.0.0.1', database='bridge_test', port=3306,path='c:\\Users\\yqin78\\Proj.Python\\PyOpenBrIM\\server backup\\20180302_141015_19')
    point1 = OBPoint(0, 0, 0, 'P1')
    point2 = OBPoint(10, 0, 0, 'P2')
    point3 = OBPoint(20, 0, 0, 'P2')
    point4 = OBPoint(30, 0, 0, 'P2')
    tc = combine(202,'Test dat path',config, 'CombineClass')
    # print(tc.x)
    tc.coordinates(0,0,0,10,20,0)
    # print(tc.x1)
    atja = tc.attr_json()
    print(atja)
    decoded = json.loads(atja)
    dbc = decoded['dbconfig']
    print(type(dbc))


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
