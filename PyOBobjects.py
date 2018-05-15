#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

'''
Templates for OpenBrIM
'''

import mysql.connector as mc

from PyOpenBrIM import *


class Cuboid(Volume):

    def __init__(self, length, width, thick, cuboid_name=''):
        super(Cuboid, self).__init__(Surface(Point(-width / 2, -length / 2, 0),
                                             Point(width / 2, -length / 2, 0),
                                             Point(width / 2, length / 2, 0),
                                             Point(-width / 2, length / 2, 0)),
                                     Surface(Point(-width / 2, -length / 2, thick),
                                             Point(width / 2, -length / 2, thick),
                                             Point(width / 2, length / 2, thick),
                                             Point(-width / 2, length / 2, thick)),
                                     cuboid_name)





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
        pass

    def as_proj(self):
        """as a template in OpenBrIM Library"""
        plateproj = Project(self.name, 'template')
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
            print("Mysql Error {:d}: {}".format(e.args[0], e.args[1]))

    def __del__(self):
        self.close()

    def select_db(self, db):
        try:
            self.conn.select_db(db)
        except mc.Error as e:
            print("Mysql Error {:d}: {}".format(e.args[0], e.args[1]))

    def query(self, sql):
        try:
            n = self.cur.execute(sql)
            return n
        except mc.Error as e:
            print("Mysql Error:{}\nSQL:{}".format(e, sql))

    def fetch_row(self, with_description=False):
        result = self.cur.fetchone()
        if with_description:
            col_name = [i[0] for i in self.cur.description]
            return dict((col,res) for col, res in zip(col_name,result))
        else:
            return result

    def fetch_all(self, with_description=False):
        result = self.cur.fetchall() # a list of tuples
        col_name = [i[0] for i in self.cur.description]
        # only cur.description[0] is the column name
        d = []
        if with_description:
            for oneline in result:
                d.append(dict((col,res) for col, res in zip(col_name,oneline)))
            return d
        else:
            return result

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
