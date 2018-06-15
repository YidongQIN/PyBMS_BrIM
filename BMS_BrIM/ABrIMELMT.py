#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
"""

from Interfaces.BrDatabase import *
from Interfaces.BrOpenBrIM import *


class PyElmt(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        self.id = elmt_id
        self.type = elmt_type
        if elmt_name:
            self.name = elmt_name
        else:
            self.name = elmt_type + '_' + str(elmt_id)
        self.db_config: dict = None
        self.openbrim = dict()  # or a dict of eET.elements?
        self.des: str = None

    def set_mongo_doc(self):
        """write info into the mongo.collection.document"""
        with ConnMongoDB(**self.db_config) as _db:
            _db.update_data(self.db_config['table'], self.id,
                            **self._attr_to_mongo_dict(self))

    def get_mongo_doc(self):
        with ConnMongoDB(**self.db_config) as _db:
            _result = _db.find_by_kv(self.db_config['table'], '_id', self.id)
            _newattr = self._mongo_id_to_self_id(_result)
            self.check_update_attr(**_newattr)
            return _newattr

    def set_openbrim(self, model_class, ob_class, **attrib_dict):
        """create a OpenBrim XML string"""
        _model:PyOpenBrIMElmt = ob_class(**attrib_dict)
        if model_class in ['fem', 'geo']:
            self.openbrim[model_class] = _model
            return self.openbrim[model_class]
        else:
            print('the Model class of {} should be FEM, GEO'.format(self.name))
            raise ValueError

    def get_openbrim(self):
        pass

    def set_sap2k(self):
        pass

    def get_sap2k(self):
        pass

    #
    def check_update_attr(self, **attributes_dict):
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print('!Attribute changed! {}.{}->{}'.format(self.name, _k, _v))
            except KeyError:
                pass
            self.__dict__[_k] = _v

    def set_dbconfig(self, database, table, **db_config):
        db_config['database'] = database
        db_config['table'] = table
        if self.type == 'Sensor':  # for now, only Sensor use MySQL
            self._set_mysql_config(**db_config)
        else:
            self._set_mongo_config(**db_config)

    def _set_mongo_config(self, database, table, host='localhost', port=27017):
        """get db config and connect to MongoDB"""
        self.db_config = {'host': host, 'port': port, 'database': database, 'table': table}

    def _set_mysql_config(self, database, user, password, host='localhost', port=3306, **kwargs):
        """get db config and connect to MySQL"""
        self.db_config = {'user': user, 'password': password, 'database': database,
                          'host': host, 'port': port}
        if 'table' not in kwargs.keys():
            print('The table/collection name is needed')
        self.db_config['table'] = kwargs['table']

    def describe(self, des):
        """describe, attached documents, etc"""
        assert isinstance(des, str)
        self.des = des

    @staticmethod
    def _attr_pop_some(elmt, *pop_list):
        _d = dict(elmt.__dict__.items())
        for _pop in pop_list:
            try:
                _d.pop(_pop)
            except KeyError:
                print("No {} in the attributes of {}".format(_pop, elmt.name))
        return _d

    @staticmethod
    def _attr_pick_some(elmt, *pick_list):
        _d = dict()
        for _pick in pick_list:
            try:
                _d[_pick] = elmt.__dict__[_pick]
            except KeyError:
                pass
        return _d

    @staticmethod
    def _attr_to_mongo_dict(elmt):
        """dump some of the attributes to dict.
        the default pop out list is: 'openbrim','db_config'. """
        return AbstELMT._attr_pop_some(elmt, 'id', 'openbrim', 'db_config')

    @staticmethod
    def _mongo_id_to_self_id(doc: dict):
        """change the field(key) '_id' to 'id'. """
        _d = {**doc}
        _d['id'] = _d['_id']
        _d.pop('_id')
        return _d


class AbstELMT(PyElmt):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """abstract elements, such as material, section, load case"""
        super(AbstELMT, self).__init__(elmt_type, elmt_id, elmt_name)


class PhysicalELMT(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(PhysicalELMT, self).__init__(elmt_type, elmt_id, elmt_name)
        self.section = None
        self.material = None
        self.dimension = dict()
        self.position = dict()
        self.direction = dict()


    # may not use the below

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
