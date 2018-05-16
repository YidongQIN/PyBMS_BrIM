__author__ = 'Yidong QIN'

'''
Sensors definition in OpenBrIM
'''

import matplotlib.pyplot as plt
import numpy as np

from PyPackObj import *


class Sensor(ObjElmt):
    base_node: FENode

    def __init__(self, sensor_id, sensor_type, des: str, database_config: dict):
        super(Sensor, self).__init__('Sensor', sensor_id, D=des)
        self.id = sensor_id
        self.type = sensor_type
        self.name = '{}_{}'.format(sensor_type, sensor_id)
        dbconfig = dict(database_config)
        try:
            self.datpath = dbconfig.pop('path')
            # fileName is from the Server Setting JSON
        except KeyError:
            print('For the sensor <{}>,a "path" item is required in the config dictionary'.format(self.name))
        self.dbconfig = dbconfig  # user, passwd, host, database, port
        self.x, self.y, self.z, self.dx, self.dy, self.dz = self.get_install()
        self.width, self.length, self.thick = self.get_dimension()
        self.unitid, self.channel = self.get_unit_info()
        self.datpath = self.get_backup_filename()

    def read_db_one(self, tbname, *col_names):
        db = ConnMySQL(**self.dbconfig)
        sql = 'select {} from bridge_test.{} where sensorID ={}'.format(", ".join(col_names), tbname, self.id)
        db.query(sql)
        info = db.fetch_row()
        db.close()
        return info

    def print_dbinfo(self, tbname, *col_names):
        info = self.read_db_one(tbname, *col_names)
        for i in range(len(info)):
            print('{}: {}'.format(col_names[i], info[i]))

    def plot_dat(self):
        print('Dat backup file of <{}> is {}'.format(self.name, self.datpath))
        DatProc('Sensor data of {}'.format(self.name), self.datpath)

    def get_install(self):
        return self.read_db_one('sensorchannelinstallation', 'PositionX',
                                'PositionY', 'PositionZ', 'DirectionX',
                                'DirectionY', 'DirectionZ')

    def get_manufac(self):
        return self.read_db_one('sensor', 'manufacturerName', 'modelNumber')

    def get_dimension(self):
        return self.read_db_one('sensorchannelinstallation', 'dimension1', 'dimension2', 'dimension3')

    def get_unit_info(self):
        return self.read_db_one('sensorchannelinstallation', 'wirelessUnitId', 'channelID')

    def get_backup_filename(self):
        """fileName is U{unitID}_{ChannelID}.dat"""
        return '{}\\U{}_{}.dat'.format(self.datpath, self.unitid, self.channel)

    def geom(self):
        """ OpenBrIM geometry model"""
        if not (self.x, self.y, self.z):
            print('Sensor <{}> position required'.format(self.name))
        if not (self.dx, self.dy, self.dz):
            print('Sensor <{}> direction required'.format(self.name))

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
    def __init__(self, tp_id, des, database_config):
        super(Temperature, self).__init__(tp_id, 'Temperature', des, database_config)

    def geom(self):
        super(Temperature, self).geom()
        tp = Surface(Point(-self.length / 2, -self.width / 2),
                     Point(self.length / 2, -self.width / 2),
                     Point(self.length / 2, self.width / 2),
                     Point(-self.length / 2, self.width / 2),
                     thick_par=1,
                     material_obj='Sensor_Temperature',
                     surface_name=self.name)
        tp.add_attr(Color='#DC143C')
        tp.move_to(self.x, self.y, self.z)
        tp.rotate(self.dx, self.dy, self.dz)
        return tp

    def fem(self):
        pass


class StrainGauge(Sensor):
    def __init__(self, sg_id, des, database_config):
        super(StrainGauge, self).__init__(sg_id, 'strainGauge', des, database_config)

    def geom(self):
        super(StrainGauge, self).geom()
        ss = Surface(Point(-self.length / 2, -self.width / 2),
                     Point(self.length / 2, -self.width / 2),
                     Point(self.length / 2, self.width / 2),
                     Point(-self.length / 2, self.width / 2),
                     thick_par=1,
                     material_obj='Sensor_StrainGauge',
                     surface_name=self.name)
        ss.add_attr(Color='#DC143C')
        ss.move_to(self.x, self.y, self.z)
        ss.rotate(self.dx, self.dy, self.dz)
        return ss


class Accelerometer(Sensor):
    def __init__(self, ac_id, des, database_config):
        super(Accelerometer, self).__init__(ac_id, 'accelerometer', des, database_config)
        # self.name = 'AC{}'.format(ac_id)
        # self.id = ac_id

    def geom(self):
        super(Accelerometer, self).geom()
        ac = CubeGeo(self.width, self.length, self.thick)
        ac.add_attr(Color='#DC143C')
        ac.move_to(self.x, self.y, self.z)
        ac.rotate(self.dx, self.dy, self.dz)
        return ac


class Displacement(Sensor):
    def __init__(self, ds_id, des, database_config):
        super(Displacement, self).__init__(ds_id, 'Displacement', des, database_config)
        self.name = 'DS{}'.format(ds_id)
        self.id = ds_id

    def geom(self):
        super(Displacement, self).geom()
        line = Line(Point(0, 0, 0), Point(self.length, 0, 0), section=Section('', '', Circle('', 1)))
        box = CubeGeo(self.width, self.width, self.thick)
        box.move_to(self.length / 2, 0, -self.thick / 2)
        ds = Group(self.name, line, box)
        ds.add_attr(Color='#DC143C')
        ds.move_to(self.x, self.y, self.z)
        ds.rotate(self.dx, self.dy, self.dz)
        return ds


class NetworkUnit(object):
    """DAQ"""

    def __init__(self, unitid, dbconfig, *sensorlist):
        self.id = unitid
        self.dbconfig = dbconfig
        self.sensorlist = sensorlist

    def get_unit_info(self):
        return self.read_db_one('wirelessUnit', 'type', 'modelNumber')

    def get_channel_install(self):
        return self.read_db_all('sensorchannelinstallation', 'sensorId', 'monitoredAxis', 'channelId')

    def read_db_one(self, tbname, *col_names):
        db = ConnMySQL(**self.dbconfig)
        sql = 'select {} from bridge_test.{} where wirelessUnitID ={}'.format(", ".join(col_names), tbname, self.id)
        db.query(sql)
        info = db.fetch_row()
        return info

    def read_db_all(self, tbname, *col_names):
        db = ConnMySQL(**self.dbconfig)
        sql = 'select {} from bridge_test.{} where wirelessUnitID ={}'.format(", ".join(col_names), tbname, self.id)
        db.query(sql)
        info = db.fetch_all(True)
        return info


class Experiment(object):
    """specify a Experiment by recording task, procedure, data, etc"""

    def __init__(self, exptid, bridgeid, dbconfig):
        """shown as Text3D"""
        self.id = exptid
        self.bridgeid = bridgeid
        self.dbconfig = dbconfig
        self.name = exptid

    def geom(self, x, y, z, size):
        return Text3D(self.name, x, y, z, size)

    def get_expt_info(self):
        expt = self.read_db_one('experimentconfiguration', 'name', 'status')
        return expt

    def get_bridge_info(self):
        db = ConnMySQL(**self.dbconfig)
        sql = "select name, description, material, structuralType from bridge_test.bridge where bridgeId ={}".format(
            self.bridgeid)
        db.query(sql)
        info = db.fetch_row()
        return info

    def read_db_one(self, tbname, *col_names):
        db = ConnMySQL(**self.dbconfig)
        sql = 'select {} from bridge_test.{} where experimentconfigurationId ={}'.format(", ".join(col_names), tbname, self.bridgeid)
        db.query(sql)
        info = db.fetch_row()
        return info

    def read_db_all(self, tbname, *col_names):
        db = ConnMySQL(**self.dbconfig)
        sql = 'select {} from bridge_test.{} where experimentconfigurationId ={}'.format(", ".join(col_names), tbname,
                                                                                         self.id)
        db.query(sql)
        info = db.fetch_all(True)
        return info


class DatProc(object):
    """Get and process of sensor data"""

    def __init__(self, title, file_path):
        """Get .dat file in a particular path"""
        self.title = title
        try:
            self.data = np.loadtxt(file_path)
        except OSError as e:
            print(e)
        self.plot()
        self.fourier()

    def plot(self):
        plt.plot(self.data)
        plt.xlabel('Sampling Point')
        plt.ylabel('Value')
        plt.title(self.title)
        plt.show()

    def fourier(self):
        sp = np.fft.fft(self.data)
        freq = np.fft.fftfreq(self.data.shape[-1])
        plt.plot(freq, sp.real, freq, sp.imag)
        plt.xlabel('Frequency')
        plt.ylabel('dB')
        plt.title('FFT of {}'.format(self.title))
        plt.show()
