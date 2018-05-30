#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
This is the most important part of my BMS based on BIM.

It is the bridge between the Modelling and the codes.
PyOBJ inherits from PyOB->PyPackOB and PyDB, as well as other software like PySAP2K in the future.
and then is used for PyElement, PySensor or PyInspection.

PyOpenBrIM->PyPackOB  PyDatabase  Py_other_interface...
\__________________________________________/
                     |
                   *PyOBJ*
                     |
/------------------------------------------\ 
PyElement   PySensor  PyInspection  Py...
"""

from PyDatabase import *
from PyPackOB import *


class PyElmt(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        self.id = elmt_id
        self.type = elmt_type
        self.name = elmt_name
        self.mysql = {}
        self.des = None

    def openbrim(self, *args, **kwargs):
        """OpenBrIM is geometry model and FEM model"""
        print(self.name)
        print(args, kwargs)

    def model(self, model_class, *args, **kwargs):
        """get model: database, fem or geo"""
        print(self.name)
        return model_class(*args, **kwargs)

    #@TODO 把对象的属性分配称两个dict，分别是fem和geo生成所用
    @property
    def model_fem(self):
        """how to judge which prms are required by the fem_class() ?"""
        # return self.fem_class(OBFENode(0,0,0), OBFENode(10,10,10), section='LineSection')
        return self._model_fem
        #@TODO return self.fem_class(**args_of_fem)

    @model_fem.setter
    def model_fem(self, femodel):
        """most cases, unused, should be generated automatically"""
        self._model_fem = femodel

    @property
    def model_geo(self):
        return self.geo_class(OBPoint(0, 0, 0), OBPoint(10, 10, 10), section='LineSection')

    def model_db(self, db_class, *args, **kwargs):
        """MySQL or NoSQL"""
        if db_class:
            print(*args, **kwargs)
        return dict(id=self.id)

    def mysql_conn(self, **db_config):
        """get db config and connect to db"""
        try:
            for _k in ['user', 'password', 'host', 'port', 'database']:
                self.mysql[_k] = db_config[_k]
        except KeyError as e:
            print('<{}> db_config Missing Key = {}'.format(self.name, e))

    def mysql_read(self, id_name, table, *columns, fetch_type='ALL', with_des=False):
        try:
            with ConnMySQL(**self.mysql) as _db:
                _db.select(id_name, self.id, self.mysql['database'], table, *columns)
                _result = _db.fetch(fetch_type, with_des)
                print("SQL result is:\n  {}".format(_result))
                return _result
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def mysql_insert(self, table, *data):
        """first check if exist, then update or insert"""
        try:
            with ConnMySQL(**self.mysql) as _db:
                _db.insert(table, *data)
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def mysql_update(self, id_name, table, *data):
        """update the records of the element"""
        try:
            with ConnMySQL(**self.mysql) as _db:
                _condition = '{}={}'.format(id_name, self.id)
                _db.update(table, *data, condition=_condition)
                return
        except BaseException as e:
            raise e

    def relationship(self):
        """read child nodes and parent nodes from database"""
        pass

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

    def description(self, des):
        assert isinstance(des, str)
        self.des = des


class PyAbst(PyElmt):

    def __init__(self, elmt_type, elmt_id, elmt_name):
        """abstract elements, such as material, section, load case"""
        super(PyAbst, self).__init__(elmt_type, elmt_id, elmt_name)


class PyReal(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id, elmt_name):
        """real members of structure"""
        super(PyReal, self).__init__(elmt_type, elmt_id, elmt_name)
        self.section = None
        self.material = None
        self.dimension = dict(d1=None)
        self.position = dict(x=None, y=None, z=None) #@TODO points or coordinates?
        self.direction = dict(dx=None, dy=None, dz=None)
        self.alpha = 0  # the status index

    def init_by_db(self):
        pass

    def init_by_io(self):
        pass

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
