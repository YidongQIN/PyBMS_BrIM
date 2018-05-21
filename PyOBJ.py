#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""

from PyPackOB import *
from PyDatabase import *

class PyElmt(object):

    def __init__(self, elmt_type, elmt_id):
        self.id = elmt_id
        self.type = elmt_type
        # self.node OR model or elmt ?
        self.db = None
        self.model=None


    def model(self):
        """get model, fem or geo"""
        pass

    def get_dbconfig(self, **db_config):
        """get db config and connect to db"""
        for k in ['user','password', 'host','port','database']:
            if k not in db_config.keys():
                print('{} should be provided in database config'.format(k))
                break
        self.db = db_config

    def read_db(self, sql):
        pass

    # def get_db(self, db_config):
    #     """user, passwd, host, database, port"""
    #     self.dbconfig = dict(db_config)  # copy a dict
    #     db = ConnMySQL(**self.dbconfig)
    #     sql = 'select {} from bridge_test.{} where sensorID ={}'.format(", ".join(col_names), tbname, self.id)
    #     db.query(sql)
    #     info = db.fetch_row()
    #     db.close()
    #     return info


    def openbrim(self):
        """ may not"""
        pass



class PyAbst(PyElmt):

    def __init__(self, obj_type, obj_id):
        """abstract elements, such as material, section, load case"""
        super(PyAbst, self).__init__(obj_type,obj_id)
        self.name = '{}_{}'.format(self.type, self.id)


class PyReal(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, obj_type, obj_id):
        """real members of structure"""
        super(PyReal, self).__init__(obj_type, obj_id)
        self.name = '{}_{}'.format(self.type, self.id)
        self.geo_class: OBObjElmt
        self.fem_class: OBObjElmt
        self.section = None
        self.material = None
        self.dbconfig = None
        # self.description = None

    def init_by_db(self):
        pass

    def init_by_io(self):
        pass

    def read_db(self):
        pass

    def set_attr_value(self):
        pass
    def set_material(self, mat: (OBMaterial, OBExtends, str)):
        if mat:
            self.material = mat
        else:
            self.read_db()

    def set_section(self, sec: (OBSection, str)):
        if sec:
            self.section = sec
        else:
            self.read_db()

    def describe_it(self, des):
        self.description = des
