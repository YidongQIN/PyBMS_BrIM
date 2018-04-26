#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM
'''

import mysql.connector as mc

from PyOpenBrIM import *


class ConnMySQL(object):

    def __init__(self, host, database, user, password, port, charset="utf8"):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        try:
            self.conn = mc.connect(host=self.host, port=self.port,
                                   user=self.user, password=self.password)
            # self.conn.autocommit(False)
            # self.conn.set_character_set(self.charset)
            self.cur = self.conn.cursor()
        except mc.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def __del__(self):
        self.close()

    def select_db(self, db):
        try:
            self.conn.select_db(db)
        except mc.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except mc.Error as e:
            print("Mysql Error:%s\nSQL:%s" % (e, sql))

    def fetch_row(self, with_description=False):
        result = self.cur.fetchone()
        if with_description:
            col_name = [i[0] for i in self.cur.description]
            return col_name, result
        else:
            return result

    def fetch_all(self):
        result = self.cur.fetchall()
        desc = self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
                d.append(_d)
        return d # a list of dicts

    def insert(self, table_name, data):
        columns = data.keys()
        _prefix = "".join(['INSERT INTO `', table_name, '`'])
        _fields = ",".join(["".join(['`', column, '`']) for column in columns])
        _values = ",".join(["%s" for i in range(len(columns))])
        _sql = "".join([_prefix, "(", _fields, ") VALUES (", _values, ")"])
        _params = [data[key] for key in columns]
        return self.cur.execute(_sql, tuple(_params))

    def update(self, tbname, data, condition):
        _fields = []
        _prefix = "".join(['UPDATE `', tbname, '`', 'SET'])
        for key in data.keys():
            _fields.append("%s = %s" % (key, data[key]))
        _sql = "".join([_prefix, _fields, "WHERE", condition])

        return self.cur.execute(_sql)

    def delete(self, tbname, condition):
        _prefix = "".join(['DELETE FROM  `', tbname, '`', 'WHERE'])
        _sql = "".join([_prefix, condition])
        return self.cur.execute(_sql)

    def get_last_insert_id(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()


class BoltedPlate(ObjElmt):

    def __init__(self, plate_name,
                 thick, length, width,
                 diameter, xclearance, yclearance,
                 column, row,
                 material='steel'):
        super(BoltedPlate, self).__init__('Surface', plate_name)
        self.thick = self.prm_to_value(thick)
        self.length = self.prm_to_value(length)
        self.width = self.prm_to_value(width)
        self.diameter = self.prm_to_value(diameter)
        self.xclearance = self.prm_to_value(xclearance)
        self.yclearance = self.prm_to_value(yclearance)
        self.column = self.prm_to_value(column)
        self.row = self.prm_to_value(row)
        self.material = material
        self.x_sp = (self.length - 2 * self.xclearance) / (self.column - 1)
        self.y_sp = (self.width - 2 * self.yclearance) / (self.row - 1)
        # self.Pthick = self.prm_to_name(thick)
        #         # self.Plength = self.prm_to_name(length)
        #         # self.Pwidth = self.prm_to_name(width)
        #         # self.Pdiameter = self.prm_to_name(diameter)
        #         # self.Pxclearance = self.prm_to_name(xclearance)
        #         # self.Pyclearance = self.prm_to_name(yclearance)
        #         # self.Pcolumn = self.prm_to_name(column)
        #         # self.Prow = self.prm_to_name(row)

    def geom(self):
        """a Surface Elmt, use real number not parameters"""
        plate_def = Surface(Point(0, 0),
                            Point(self.length, 0),
                            Point(self.length, self.width),
                            Point(0, self.width),
                            thick_par=self.thick,
                            material_obj=self.material,
                            surface_name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = Circle('hole_{}_{}'.format(i, j),
                              radius=self.diameter / 2,
                              x=self.xclearance + i * self.x_sp,
                              y=self.yclearance + j * self.y_sp)
                hole.sub(PrmElmt('IsCutout', 1))
                holes.append(hole)
        plate_def.sub(*holes)
        return plate_def

    def fem(self):
        """FEM is totally different from geometry model.
        it needs Nodes, not only Points: both coordinates(x,y,z)and fixity,
        and connection with other elements. """
        pass

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = Project(self.name, 'template')
        plateproj.sub(self.geom())
        self.elmt = plateproj
        return plateproj

    # def as_prmodel(self):
    #     """to generate a ParamML model that can be modified in the APP.
    #     *** GIVEN UP
    #     the REPEAT in ParamML is complex, so that the row number and the column number is nut parameterized"""
    #     paramodel = Surface(Point(0, 0),
    #                         Point('lengthOfPlate', 0),
    #                         Point('lengthOfPlate', 'widthOfPlate'),
    #                         Point(0, 'widthOfPlate'),
    #                         thick_par='thickOfPlate',
    #                         material_obj=self.material,
    #                         surface_name=self.name)
    #     holes = []
    #     for i in range(self.column):
    #         for j in range(self.row):
    #             hole = Circle('hole_{}_{}'.format(i, j),
    #                           radius='diaOfHole/2',
    #                           x='x_clearOfHole + ' + str(i * self.x_sp),
    #                           y='y_clearOfHole + ' + str(j * self.y_sp))
    #             hole.sub(PrmElmt('IsCutout', 1))
    #             holes.append(hole)
    #     paramodel.sub(*holes)
    #     t = PrmElmt('thickOfPlate', self.Pthick, 'Thickness of each plate')
    #     l_p = PrmElmt('lengthOfPlate', self.Plength, 'Length of each plate')
    #     w = PrmElmt('widthOfPlate', self.Pwidth, 'Width of each plate')
    #     d = PrmElmt('diaOfHole', self.Pdiameter, 'Diameter of each hole')
    #     x_clear = PrmElmt('x_clearOfHole', self.Pxclearance, 'x clearance from the edge to the hole')
    #     y_clear = PrmElmt('y_clearOfHole', self.Pyclearance, 'y clearance from the edge to the hole')
    #     paramodel.sub(t, l_p, w, d, x_clear, y_clear)  # , col_num, row_num)
    #     return paramodel


class Sensor(ObjElmt):
    def __init__(self, sensor_id, sensor_type, des, database_config):
        super(Sensor, self).__init__('Sensor', sensor_id, D=des)
        self.id = sensor_id
        self.type = sensor_type
        self.db = database_config  # user, passwd, host, database, port
        # self.des = des
        # self.x, self.y, self.z, self.dx, self.dy, self.dz
        self.get_install()
        self.get_model()


    def read_table(self, tbname):
        db = ConnMySQL(**self.db)
        sql = 'select * from bridge_test.{} where sensorID ={}'.format(tbname,self.id)
        db.query(sql)
        info = db.fetch_row(True)
        for i in range(len(info[0])):
            print('{}: {}'.format(info[0][i], info[1][i]))
        db.close()

    def get_install(self):
        db = ConnMySQL(**self.db)
        sql = 'select PositionX, PositionY, PositionZ, DirectionX, DirectionY, DirectionZ from bridge_test.sensorchannelinstallation where sensorId ={}'.format(self.id)
        db.query(sql)
        self.x, self.y, self.z, self.dx, self.dy, self.dz = db.fetch_row()
        db.close()

    def get_model(self, dimension1=10, dimension2=10, dimension3=10):
        db = ConnMySQL(**self.db)
        sql1 = 'select manufacturerName, modelNumber from bridge_test.sensor where sensorId = {}'.format(self.id)
        db.query(sql1)
        self.fac, self.model =db.fetch_row()
        sql2 = 'select dimension1, dimension2, dimension3 from bridge_test.sensorchannelinstallation where sensorId = {}'.format(self.id)
        db.query(sql2)
        self.width, self.length, self.thick = db.fetch_row()
        if not self.width:
            self.width =dimension1
        if not self.length:
            self.width =dimension2
        if not self.thick:
            self.width =dimension3
        db.close()


    def geom(self):
        """ OpenBrIM geometry model"""
        if not (self.x, self.y, self.z):
            print('Sensor {} position information is required'.format(self.name))
        if not (self.dx, self.dy, self.dz):
            print('Sensor {} direction information is required'.format(self.name))

    def fem(self):
        """FEM model. For sensor, it's just a node."""
        node = FENode(self.x, self.y, self.z, self.name)
        # not sure if realizable?
        # when create a FEM, cannot insert the node into this position
        # because it will change the node number and element
        return node

    def direction_setting(self):
        # if self.dx^2+self.dy^2+self.dz^2 != 1:
        #     print('Error in Direction data')
        if self.dx == 1:
            return {"RZ": "0"}
        if self.dy == 1:
            return {"RZ": "PI/2"}
        if self.dz == 1:
            return {"RY": "PI/2"}


class Temperature(Sensor):
    pass


class StrainGauge(Sensor):
    def __init__(self, sg_id, des, database_config):
        super(StrainGauge, self).__init__(sg_id, 'strainGauge', des, database_config)
        self.name = 'SG{}'.format(sg_id)
        self.id = sg_id
        # self.width = 2
        # self.length = 10
        # self.thick = 1

    def geom(self):
        """no size"""
        ss = Surface(Point(-self.length / 2, -self.width / 2),
                     Point(self.length / 2, -self.width / 2),
                     Point(self.length / 2, self.width / 2),
                     Point(-self.length / 2, self.width / 2),
                     thick_par=1,
                     material_obj='Sensor_StrainGauge',
                     surface_name=self.name)
        ss.add_attr(X=self.x, Y=self.y, Z=self.z, Color='#DC143C')
        ss.add_attr(**self.direction_setting())
        return ss


class Accelerometer(Sensor):
    def __init__(self, ac_id, des, database_config):
        super(Accelerometer, self).__init__(ac_id, 'accelerometer', des, database_config)
        self.name = 'AC{}'.format(ac_id)
        self.id = ac_id
        self.width = 30
        self.length = 50
        self.thick = 25
        # self.direction = direction  # X, Y, or Z

    def geom(self):
        ac = Volume('AC{}'.format(self.id), self.x, self.y, self.z)
        ac.add_attr(Color='#DC143C')
        ac.set_surface(Point(-self.width / 2, -self.length / 2, 0),
                       Point(self.width / 2, -self.length / 2, 0),
                       Point(self.width / 2, self.length / 2, 0),
                       Point(-self.width / 2, self.length / 2, 0))
        ac.set_surface(Point(-self.width / 2, -self.length / 2, self.thick),
                       Point(self.width / 2, -self.length / 2, self.thick),
                       Point(self.width / 2, self.length / 2, self.thick),
                       Point(-self.width / 2, self.length / 2, self.thick))
        return ac

class Displacement(Sensor):
    def __init__(self, ds_id, des, database_config):
        super(Displacement, self).__init__(ds_id, 'Displacement', des, database_config)
        self.name='DS{}'.format(ds_id)
        self.id=ds_id

    def link_to_node(self):
        pass

    def geom(self):
        # line=Line(Point())
        # box = Volume()
        # ds=Group(self.name,line,box)
        pass
