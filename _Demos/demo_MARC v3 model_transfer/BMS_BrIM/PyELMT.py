#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
PyELMT gets all interfaces' methods.
Each PyELMT has 3 kinds of attributes:
1. distinguished naming: type+id.
2. characteristic attr: depends on element typy. 
    For example, Material will have E=elastic module, d=density, etc. While Parameter will only have a value.
3. Interfaces. A OpenBrIM interface, a MongoDB interface.
    Each Interface will have two 
"""
from Interfaces import *


class PyElmt(object):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """Basic attributes for a PyELMT is type, id.
        name is optional, as well as description.
        Each interface has a corresponding attribute"""
        self._id = elmt_id
        self.type = elmt_type
        if elmt_name:
            self.name = elmt_name
        else:
            self.name = elmt_type + '_' + str(elmt_id)
        # two interfaces: Database and OpenBrIM
        self.db_config: dict = dict()  # dict(database=, table=, user=,...)
        self.openBrIM: dict or PyOpenBrIMElmt  # dict of eET.elements

    # MongoDB methods: setting; setter, getter;
    def set_mongo_doc(self):
        """write info into the mongo.collection.document"""
        with ConnMongoDB(**self.db_config) as _db:
            _col = self.db_config['table']
            if not self._id:
                self._id = _db.insert_data(_col, **_attr_to_mongo_dict(self))
            elif not _db.find_by_kv(_col, 'name', self.name):
                _ = _db.update_data(_col, self._id, **_attr_to_mongo_dict(self))
            else:
                _db.update_data(_col, self._id, **_attr_to_mongo_dict(self))
                print("<{}> is in <{}>, ObjectID={}".format(self.name, _col, self._id))

    def get_mongo_doc(self, if_print=False):
        with ConnMongoDB(**self.db_config) as _db:
            _result = _db.find_by_kv(self.db_config['table'], '_id', self._id, if_print)
            self.check_update_attr(_result)
            return _result

    def set_openbrim(self, ob_class, **attrib_dict):
        # update the __dict__ with the attrib_dict
        # don't update the element.__dict__ with the attrib_dict. Because attrib_dict is used to add other redundancy info.
        # self.__dict__.update(**attrib_dict)
        # get attributes required by the OpenBrIM type
        _required_attr: dict = _attr_pick(self, *ob_class._REQUIRE)
        # packaging the attributes for the OpenBrIM elements
        _openbrim_attrib = {**attrib_dict, **_required_attr}
        try:
            # openBrIM is one of the PyELMT interfaces
            _openbrim_model: PyOpenBrIMElmt = ob_class(**_openbrim_attrib)
            return _openbrim_model
        except TypeError as e:
            print("<>.set_openbrim()".format(self.name), e)
            return

    def get_openbrim(self, model_class=None):
        if not model_class:
            return self.openBrIM
        else:
            try:
                return self.openBrIM[model_class]
            except KeyError:
                print("{} has no OpenBrIM model of {}".format(self.name, model_class))
                return

    def set_sap2k(self):
        pass

    def get_sap2k(self):
        pass

    def check_update_attr(self, attributes_dict: dict):
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print("PyELMT.update from MongoDB:")
                    print('  <{}> Attribute changed!'.format(self.name))
                    print('  * {} -> {}'.format(_k, _v))
            except KeyError:
                print("PyELMT.update from MongoDB:")
                print("  <{}> gets new attribute!".format(self.name))
                print('  * {} -> {}'.format(_k, _v))
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


def _attr_pick(elmt, *pick_list):
    """keys are from the pick_list, and find corresponding attributes from the element.__dict__."""
    _d = dict()
    for _pick in pick_list:
        try:
            _d[_pick] = elmt.__dict__[_pick]
        except KeyError:
            # print("PyELMT.attr_pick(): No '{}' in {}".format(_pick, elmt.name))
            pass
    return _d


def _attr_pop(elmt, *pop_list):
    _d = dict()
    for _k, _v in elmt.__dict__.items():
        if (_k not in pop_list) and _v:
            _d[_k] = _v
    return _d


def _attr_to_mongo_dict(elmt: PyElmt):
    """dump some of the attributes to dict.
    the default pop out list is: 'openbrim','db_config'. """
    return _attr_pop(elmt, 'openBrIM', 'db_config',
                     'section_ob', 'section',
                     'material_ob', 'material',
                     'thick_prm_ob', 'thick_prm',
                     'shape', 'shape_ob',
                     'node1', 'node1_ob',
                     'node2', 'node2_ob',
                     'node3', 'node3_ob',
                     'node4', 'node4_ob',
                     )


def parameter_format(k):
    if isinstance(k, int):
        return k
    elif isinstance(k, float):
        try:
            return int(k)
        except ValueError:
            return k
    elif isinstance(k, str):
        try:
            return float(k)
        except ValueError:
            return k
    else:
        from BMS_BrIM.Py_Abstract import Parameter
        if isinstance(k, Parameter):
            return k.value
        else:
            print("Error formatting parameter")
            print(type(k))
            return


class XY(object):
    def __init__(self, x=0, y=0):
        if x is not None:
            self.x = parameter_format(x)
        if y is not None:
            self.y = parameter_format(y)


class XYZ(object):

    def __init__(self, x=0, y=0, z=0):
        if x is not None:
            self.x = parameter_format(x)
        if y is not None:
            self.y = parameter_format(y)
        if z is not None:
            self.z = parameter_format(z)


class RXYZ(object):

    def __init__(self, rx=0, ry=0, rz=0):
        self.rx = rx
        self.ry = ry
        self.rz = rz
