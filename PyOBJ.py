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

    def __init__(self, elmt_type, elmt_id):
        self.id = elmt_id
        self.type = elmt_type
        self.db = dict()

    def openbrim(self):
        """ may not"""
        pass

    def model(self):
        """get model, fem or geo"""
        pass

    # @test
    def add_attr(self, **dict):
        #@TODO is this safe? useful?
        self.__dict__ = {**self.__dict__, **dict}

    def set_dbconfig(self, **db_config):
        """get db config and connect to db"""
        try:
            for _k in ['user', 'password', 'host', 'port', 'database']:
                self.db[_k] = db_config[_k]
        except KeyError as e:
            print('<{}> db_config Missing Key = {}'.format(self.name, e))

    def read_db(self, id_name, table, *columns, fetch_type='ALL', with_des=False):
        try:
            with ConnMySQL(**self.db) as _db:
                _db.select(id_name, self.id, self.db['database'], table, *columns)
                if fetch_type is 'ALL':
                    _result = _db.fetch_all(with_des)
                    # return a list of tuples: [(),(),...]
                else:
                    _result = _db.fetch_row(with_des)
                    # return a tuple
                print("SQL result is:\n  {}".format(_result))
                return _result
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def write_db(self):
        """first check if exist, then update or insert"""
        pass

    def relationship(self):
        pass

    @property
    def name(self):
        return '{}_{}'.format(self.type, self.id)

    def description(self, des):
        self.des = des

    @property
    def geo_class(self):
        type_to_geo = dict(Line=OBLine, Plate=OBSurface)
        try:
            return type_to_geo[self.type]
        except:
            return

    @property
    def fem_class(self):
        type_to_fem = dict(Line=OBFELine, Plate=OBFESurface)
        try:
            return type_to_fem[self.type]
        except:
            return

    @property
    def abs_class(self):
        type_to_abs = dict(Material=OBMaterial, Section=OBSection)
        try:
            return type_to_abs[self.type]
        except:
            return


class PyAbst(PyElmt):

    def __init__(self, elmt_type, elmt_id):
        """abstract elements, such as material, section, load case"""
        super(PyAbst, self).__init__(elmt_type, elmt_id)


class PyReal(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id):
        """real members of structure"""
        super(PyReal, self).__init__(elmt_type, elmt_id)
        self.section = None
        self.material = None
        self.alpha = 0  # the status index
        # self.description = None

    def init_by_db(self):
        pass

    def init_by_io(self):
        pass

    def set_attr_value(self):
        pass

    def set_material(self, mat: (OBMaterial, OBExtends, str)):
        if mat:
            self.material = mat
        else:
            self.read_db(self.id, 'table name', 'MaterialColumn')

    def set_section(self, sec: (OBSection, str)):
        if sec:
            self.section = sec
        else:
            self.read_db(self.id, 'table name', 'SectionColumn')
