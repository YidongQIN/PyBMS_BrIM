#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM
'''

import mysql.connector as mc

from PyOpenBrIM import *


class Cuboid(OBVolume):

    def __init__(self, length, width, thick, cuboid_name=''):
        super(Cuboid, self).__init__(OBSurface(OBPoint(-width / 2, -length / 2, 0),
                                               OBPoint(width / 2, -length / 2, 0),
                                               OBPoint(width / 2, length / 2, 0),
                                               OBPoint(-width / 2, length / 2, 0)),
                                     OBSurface(OBPoint(-width / 2, -length / 2, thick),
                                               OBPoint(width / 2, -length / 2, thick),
                                               OBPoint(width / 2, length / 2, thick),
                                               OBPoint(-width / 2, length / 2, thick)),
                                     cuboid_name)


class RealObj(object):
    geomodel: OBObjElmt
    femodel: OBObjElmt

    def __init__(self, obj_id, obj_type, geo_class, fem_class, section_obj, material_obj):
        self.id = obj_id
        self.type = obj_type
        self.geo_class = geo_class
        self.fem_class = fem_class
        self.section = section_obj
        self.material = material_obj

    def geo_xml(self, *define, **dicts):
        self.geomodel = self.geo_class(*define, **dicts)

    def fem_xml(self, *define, **dicts):
        self.femodel = self.fem_class(*define, **dicts)


class Beam(RealObj):

    def __init__(self, beam_id, *points, section):
        super(Beam, self).__init__(beam_id, 'BEAM', OBLine, OBFELine, section, None)
        if len(points) == 2:
            if isinstance(points[0], OBPoint) and isinstance(points[1], OBPoint):
                self.two_point(*points)
            elif isinstance(points[0], OBFENode) and isinstance(points[1], OBFENode):
                self.two_node(*points)
        elif len(points) == 6:
            for a in points:
                if not isinstance(a, (float, int)):
                    print("Beam {}'s Coordinates must be numbers".format(self.id))
            self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = points
        self.section = section
        self.geo_xml(OBPoint(self.x1, self.y1, self.z1), OBPoint(self.x2, self.y2, self.z2), section=self.section)
        self.fem_xml(OBFENode(self.x1, self.y1, self.z1), OBFENode(self.x2, self.y2, self.z2), section=self.section)
        # Line() material is included in section definition

    def two_point(self, point1, point2):
        self.x1 = point1.x
        self.y1 = point1.x
        self.z1 = point1.x
        self.x2 = point2.x
        self.y2 = point2.x
        self.z2 = point2.x

    def two_node(self,node1, node2):
        self.x1 = node1.x
        self.y1 = node1.x
        self.z1 = node1.x
        self.x2 = node2.x
        self.y2 = node2.x
        self.z2 = node2.x

    def coordinates(self, x1, y1, z1, x2, y2, z2):
        self.x1 = x1
        self.y1 = y1
        self.z1 = z1
        self.x2 = x2
        self.y2 = y2
        self.z2 = z2


class BoltedPlate(OBObjElmt):

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

    def geom(self):
        """a Surface Elmt, use real number not parameters"""
        plate_def = OBSurface(OBPoint(0, 0),
                              OBPoint(self.length, 0),
                              OBPoint(self.length, self.width),
                              OBPoint(0, self.width),
                              thick_par=self.thick,
                              material_obj=self.material,
                              surface_name=self.name)
        holes = []
        for i in range(self.column):
            for j in range(self.row):
                hole = OBCircle('hole_{}_{}'.format(i, j),
                                radius=self.diameter / 2,
                                x=self.xclearance + i * self.x_sp,
                                y=self.yclearance + j * self.y_sp)
                hole.sub(OBPrmElmt('IsCutout', 1))
                holes.append(hole)
        plate_def.sub(*holes)
        return plate_def

    def fem(self):
        pass

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = OBProject(self.name, 'template')
        plateproj.sub(self.geom())
        self.elmt = plateproj
        return plateproj


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
            col_name = [i[0] for i in self.cur.describe]
            return col_name, result
        else:
            return result

    def fetch_all(self):
        result = self.cur.fetchall()
        desc = self.cur.describe
        d = []
        for inv in result:
            _d = {}
            for i in range(0, len(inv)):
                _d[desc[i][0]] = str(inv[i])
                d.append(_d)
        return d  # a list of dicts

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
