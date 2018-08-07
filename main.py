from BMS_BrIM import *

testproj = ProjGroups('Testproj')
# ttt = Parameter(66, 'ThickNess', 20)
steel = Material(1, 'Steel', d="0.0000007345", E="29000")
testproj.mat_group.append(steel)
rec1=Shape(1, 'Rect 6*6', RectangleOBShape, 6, 6)
rec2=Shape(2, 'Rect 6*6', RectangleOBShape, 6, 6, is_cut=True)
sect = Section(11, 'BottomChord', rec1, rec2, material=steel)
ttt=Parameter(13, 'DeckThickness', 4, 'Thickness')
testproj.sec_group.append(rec1,rec2, sect)
node1 = Node(1, 0, 3, node_id=100)
node2 = Node(10, 22, 33, node_id=200)
deck = Surface(node1, node2, node1, node2, ttt, steel, 20, 'TestDeck')
ShowTree(ttt.openBrIM)
print(ttt.ob_type)
'''
print("=== test AbstractELMT ===")

# test Material
print("==== test Material ====")
mma = Material(2, 'Test Mat')
mma.set_property(d=100, Fy=55555, E=5000, a=0.005, b=23)
mma.set_dbconfig('fours', 'Material')
mma.describe('this is  just a mt')
mma.set_property(d=666)
mma.set_openbrim()
# mma.openBrIM = eET.Element('TAG', xbb='nani')
ShowTree(mma.openBrIM)

#test Group
print("==== test Group ====")
ggg=Group('test Group')
ggg.append(mma)
print(ggg.openBrIM)
ShowTree(ggg.openBrIM)

#test ProjGroups
print("==== test ProjGroup ====")
new_proj=ProjGroups('NewProj')
new_proj.set_dbconfig()
# new_proj._init_mongo_doc()
ShowTree(new_proj.openBrIM)

print("=== test find a doc in mongo ===")
maa = Material(2,None)
maa.set_dbconfig('fours','Material')
# maa.show_material_property()
maa.get_mongo_doc()
# maa.show_material_property()
maa.set_openbrim()
ShowTree(maa.openBrIM)

print("Test Shapes and Sections")
# rectangle
trec=Shape(1, 'Test_Rectangel', RectangleOBShape, 20,20, is_cut=False)
ShowTree(trec.openBrIM)
# circle
tcir=Shape(2, 'Test_Circle', OBCircle, 10,5, is_cut=True)
ShowTree(tcir.openBrIM)
# polygon
tpol=Shape(3, 'Test_polygon', PolygonOBShape, (0,0),(10,0),(10,20),(0,10), is_cut=True)
ShowTree(tpol.openBrIM)

ts = Section(5,'Test', trec, tpol)

MARC = ProjGroups("MARC_sensor")
MARC.sec_group.append(trec, tcir,tpol, ts)

mat1 = OBMaterial('C4000Psi', 'Deck Concrete', 'Concrete')
mat1.mat_property(d='0.000002248', E=3604, a=0.000055, Fc28=4)
mat1.show_mat_table()

ds201 = PyElmt('Sensor Test',201)
ds201.mysql_conn(**config)
info = ds201.mysql_read('sensorId', 'sensor', 'manufacturerName', 'modelNumber',fetch_type='one')

config = dict(user='root', password='qyd123', host='127.0.0.1', database='bridge_test', port = 3306)

config = dict(user='root', password='qyd123', host='127.0.0.1', database='bridge_test', port = 3306, path = 'c:\\Users\\yqin78\\Proj.Python\\PyOpenBrIM\\server backup\\20180327_161910_20\\U116_ADC_B2.dat')
di = Sensor(202,'Test dat path','test',config)
di.plot_dat()
print('file path'+di.datpath)
print('config: '+str(di.db))
'''''
