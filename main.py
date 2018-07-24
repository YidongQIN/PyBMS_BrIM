from BMS_BrIM import *


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
