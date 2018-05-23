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
        self.mysql = dict()

    def openbrim(self, *args, **kwargs):
        """OpenBrIM is geometry model and FEM model"""
        print(args, kwargs)

    def model(self, model_class, *args, **kwargs):
        """get model: database, fem or geo"""
        return model_class(*args, **kwargs)

    def model_fem(self, fem_class=None, *args, **kwargs):
        if fem_class:
            return fem_class(*args, **kwargs)
        else:
            return self.fem_class(*args, **kwargs)

    def model_geo(self, geo_class=None, *args, **kwargs):
        if geo_class:
            return geo_class(*args, **kwargs)
        else:
            return self.geo_class(*args, **kwargs)

    def model_db(self,db_class, *args, **kwargs):
        """MySQL or NoSQL"""
        if db_class:
            print(*args, **kwargs)
        return dict(id=self.id)

    # def add_attr(self, **dict):
    #     """add a dict as attributes.
    #     The situation of attribute is complex and different elements will hace totally different attributes"""
    #     print("= = You are changing __dict__ of <{}>".format(self.name))
    #     self.__dict__ = {**self.__dict__, **dict}
    #     # be careful, not sure if this is safe
    #     # ! also, the new attrib may not be recognized by IDE

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
        except:
            raise

    def relationship(self):
        """read child nodes and parent nodes from database"""
        pass

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

    def description(self, des):
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
            self.mysql_read(self.id, 'table name', 'MaterialColumn')

    def set_section(self, sec: (OBSection, str)):
        if sec:
            self.section = sec
        else:
            self.mysql_read(self.id, 'table name', 'SectionColumn')
