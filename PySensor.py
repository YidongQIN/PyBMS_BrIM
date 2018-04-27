__author__ = 'Yidong QIN'

'''
Sensors definition in OpenBrIM
'''


from PyOBobjects import *

#@TODO data process. check numpy lib

class Sensor(ObjElmt):
    base_node: FENode

    def __init__(self, sensor_id, sensor_type, des, database_config):
        super(Sensor, self).__init__('Sensor', sensor_id, D=des)
        self.id = sensor_id
        self.type = sensor_type
        self.db = database_config  # user, passwd, host, database, port
        #@TODO database_config include the file path of backups
        # self.des = des
        # self.x, self.y, self.z, self.dx, self.dy, self.dz
        self.get_install()
        self.get_model()

    def read_table(self, tbname, *col_names):
        db = ConnMySQL(**self.db)
        sql = 'select {} from bridge_test.{} where sensorID ={}'.format(", ".join(col_names), tbname, self.id)
        db.query(sql)
        info = db.fetch_row()
        for i in range(len(info)):
            print('{}: {}'.format(col_names[i], info[i]))
        db.close()

    def get_install(self):
        db = ConnMySQL(**self.db)
        sql = 'select PositionX, PositionY, PositionZ, DirectionX, DirectionY, DirectionZ from bridge_test.sensorchannelinstallation where sensorId ={}'.format(
            self.id)
        db.query(sql)
        self.x, self.y, self.z, self.dx, self.dy, self.dz = db.fetch_row()
        db.close()

    def get_model(self, dimension1=10, dimension2=10, dimension3=10):
        db = ConnMySQL(**self.db)
        sql1 = 'select manufacturerName, modelNumber from bridge_test.sensor where sensorId = {}'.format(self.id)
        db.query(sql1)
        self.fac, self.model = db.fetch_row()
        sql2 = 'select dimension1, dimension2, dimension3 from bridge_test.sensorchannelinstallation where sensorId = {}'.format(
            self.id)
        db.query(sql2)
        self.width, self.length, self.thick = db.fetch_row()
        if not self.width:
            self.width = dimension1
        if not self.length:
            self.width = dimension2
        if not self.thick:
            self.width = dimension3
        db.close()

    def geom(self):
        """ OpenBrIM geometry model"""
        if not (self.x, self.y, self.z):
            print('Sensor {} position information is required'.format(self.name))
        if not (self.dx, self.dy, self.dz):
            print('Sensor {} direction information is required'.format(self.name))

    def set_base_node(self, fenode):
        if isinstance(fenode, FENode):
            self.base_node = fenode
        else:
            print('{}.base_node is not a FENode'.format(self.name))

    def fem(self):
        """FEM model. For sensor, it's just a node."""
        node = FENode(self.x, self.y, self.z, self.name)
        # not sure if realizable?
        # when create a FEM, cannot insert the node into this position
        # because it will change the node number and element
        return node


class Temperature(Sensor):
    #@TODO
    pass


class StrainGauge(Sensor):
    def __init__(self, sg_id, des, database_config):
        super(StrainGauge, self).__init__(sg_id, 'strainGauge', des, database_config)
        self.name = 'SG{}'.format(sg_id)
        self.id = sg_id

    def geom(self):
        ss = Surface(Point(-self.length / 2, -self.width / 2),
                     Point(self.length / 2, -self.width / 2),
                     Point(self.length / 2, self.width / 2),
                     Point(-self.length / 2, self.width / 2),
                     thick_par=1,
                     material_obj='Sensor_StrainGauge',
                     surface_name=self.name)
        ss.add_attr(Color='#DC143C')
        self.move_to(self.x, self.y, self.z)
        self.rotate(self.dx, self.dy, self.dz)
        return ss


class Accelerometer(Sensor):
    def __init__(self, ac_id, des, database_config):
        super(Accelerometer, self).__init__(ac_id, 'accelerometer', des, database_config)
        self.name = 'AC{}'.format(ac_id)
        self.id = ac_id
        self.width = 30
        self.length = 50
        self.thick = 25

    def geom(self):
        ac = Cuboid(self.width,self.length,self.thick)
        ac.add_attr(Color='#DC143C')
        self.move_to(self.x, self.y, self.z)
        self.rotate(self.dx, self.dy, self.dz)
        return ac


class Displacement(Sensor):
    def __init__(self, ds_id, des, database_config):
        super(Displacement, self).__init__(ds_id, 'Displacement', des, database_config)
        self.name = 'DS{}'.format(ds_id)
        self.id = ds_id

    def geom(self):
        line = Line(Point(0, 0, 0), Point(self.length, 0, 0))
        box = Cuboid(20, self.width, self.thick)
        box.move_to(self.length/2,0,0)
        ds = Group(self.name, line, box)
        ds.add_attr(Color='#DC143C')
        self.move_to(self.x, self.y, self.z)
        self.rotate(self.dx, self.dy, self.dz)
