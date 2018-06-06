#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
"""

from Interfaces.BrDatabase import *
from Interfaces.BrXML import *


class PyElmt(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        self.id = elmt_id
        self.type = elmt_type
        if elmt_name:
            self.name = elmt_name
        else:
            self.name = elmt_type + '_' + str(elmt_id)
        self.db: dict = None
        self.node: (OBObjElmt, OBPrmElmt) = None
        self.des: str = None

    def set_database(self, **db_config):
        try:
            if self.type == 'Sensor':
                # for now, only Sensor use MySQL
                self._conn_mysql(**db_config)
            else:
                self._conn_mongo(**db_config)
        except KeyError as e:
            print('Missing setting for db')
            print(e)

    def _conn_mysql(self, database, user, password, host='localhost', port=3306):
        """get db config and connect to MySQL"""
        self.db = {'user': user, 'password': password, 'database': database,
                   'host': host, 'port': port}

    def _conn_mongo(self, database, host='localhost', port=27017):
        """get db config and connect to MongoDB"""
        self.db = {'host': host, 'port': port, 'database': database}

    def mysql_read(self, id_name, table, *columns, fetch_type='ALL', with_des=False):
        try:
            with ConnMySQL(**self.db) as _db:
                _db.select(id_name, self.id, self.db['database'], table, *columns)
                _result = _db.fetch(fetch_type, with_des)
                print("SQL result is:\n  {}".format(_result))
                return _result
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def mysql_write(self, id_name, table, *data):
        if self.mysql_read(id_name, table):
            self.mysql_update(id_name, table, *data)
        else:
            self.mysql_insert(table, *data)

    def mysql_insert(self, table, *data):
        """first check if exist, then update or insert"""
        try:
            with ConnMySQL(**self.db) as _db:
                _db.insert(table, *data)
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def mysql_update(self, id_name, table, *data):
        """update the records of the element"""
        try:
            with ConnMySQL(**self.db) as _db:
                _condition = '{}={}'.format(id_name, self.id)
                _db.update(table, *data, condition=_condition)
                return
        except BaseException as e:
            raise e

    def mongo_read(self, collection):
        try:
            with ConnMongoDB(**self.db) as _db:
                _db.find_by_kv(collection, '_id', self.id)
        except BaseException as e:
            print('Error when reading from MongoDB')
            raise e

    def mongo_write(self, collection):
        """find, then insert or update"""
        try:
            with ConnMongoDB(**self.db) as _db:
                _db.insert_elmt(collection, self)
        except BaseException as e:
            print('Error when writing into MongoDB')
            raise e

    @property
    def geo_class(self):
        type_to_geo = dict(Line=OBLine, Plate=OBSurface)
        try:
            return type_to_geo[self.type]
        except BaseException as e:
            raise e

    @property
    def fem_class(self):
        type_to_fem = dict(Line=OBFELine, Plate=OBFESurface)
        try:
            return type_to_fem[self.type]
        except BaseException as e:
            raise e

    @property
    def abs_class(self):
        type_to_abs = dict(Material=OBMaterial, Section=OBSection)
        try:
            return type_to_abs[self.type]
        except BaseException as e:
            raise e

    def describe(self, des):
        """describe, attached documents, etc"""
        assert isinstance(des, str)
        self.des = des


class PyAbst(PyElmt):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """abstract elements, such as material, section, load case"""
        super(PyAbst, self).__init__(elmt_type, elmt_id, elmt_name)

    def model(self):
        return self.abs_class


class PyReal(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(PyReal, self).__init__(elmt_type, elmt_id, elmt_name)
        self.section = None
        self.material = None
        self.dimension = dict()
        self.position = dict()
        self.direction = dict()
        self.alpha = 0  # the status index
        self._model_fem = None


    def set_position(self, **pos):
        for k in pos:
            if k not in ['x', 'y', 'z']:
                print('= = Position of {} is recommended to be x,y,z'.format(self.name))
        self.position = pos

    def set_direction(self, **drc):
        for k in drc:
            if k not in ['dx', 'dy', 'dz']:
                print('= = Direction of {} is recommended to be dx,dy,dz'.format(self.name))
        self.direction = drc

    def set_dimension(self, **dims):
        for k in dims:
            if k not in ['length', 'width', 'thick']:
                print('= = Dimension of {} is recommended to be length, width, thick, etc'.format(self.name))
        self.dimension = dims

    def set_material(self, mat: (OBMaterial, OBExtends, str)):
        if mat:
            self.material = mat
        else:
            self.mysql_read(self.id, 'table name', 'MaterialColumn')

    def set_section(self, sec: (OBSection, str)):
        if sec:
            self.section = sec
        else:
            self.mysql_read(self.id, 'table name', 'SectionColumn')

    @property
    def model_fem(self):
        """how to judge which prms are required by the fem_class() ?"""
        # return self.fem_class(OBFENode(0,0,0), OBFENode(10,10,10), section='LineSection')
        return self._model_fem

    @model_fem.setter
    def model_fem(self, femodel):
        """most cases, unused, should be generated automatically"""
        self._model_fem = femodel

    @property
    def model_geo(self):
        return self.geo_class()
