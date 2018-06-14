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

    def set_database(self):
        """write info into the database"""
        try:
            collection = self.db_config['table']
        except KeyError:
            collection = input('No table/collection name found')
        self.mongo_write(collection)

    def get_database(self):
        try:
            collection = self.db_config['table']
        except KeyError:
            collection = input('No table/collection name found')
        _results = self.mongo_read(collection)
        print(
            "Read from MongoDB <{}>.{} where _id={}".format(self.db_config['database'], self.db_config['table'], self.id))
        # print(_results)
        # print("====")
        return _results

    def set_openbrim(self, model_class, ob_class, **attrib_dict):
        """create a OpenBrim XML string"""
        _model = ob_class(name=self.name, **attrib_dict)
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

    def set_dbconfig(self, database, table, **db_config):
        try:
            db_config['database'] = database
            if self.type == 'Sensor':
                # for now, only Sensor use MySQL
                self._conn_mysql(**db_config)
            else:
                self._conn_mongo(**db_config)
        except KeyError as e:
            print('Missing setting for db')
            print(e)
        self.db_config['table'] = table
        # print(self.db_config)

    def _conn_mongo(self, database, host='localhost', port=27017, **kwargs):
        """get db config and connect to MongoDB"""
        self.db_config = {'host': host, 'port': port, 'database': database}

    def mongo_read(self, collection):
        """read information form mongodb.collection where _id=self.id"""
        try:
            with ConnMongoDB(**self.db_config) as _db:
                return _db.find_by_kv(collection, '_id', self.id)
        except BaseException as e:
            print('Error when reading from MongoDB')
            raise e

    def _conn_mysql(self, database, user, password, host='localhost', port=3306, **kwargs):
        """get db config and connect to MySQL"""
        self.db_config = {'user': user, 'password': password, 'database': database,
                          'host': host, 'port': port}

    def mongo_write(self, collection):
        """find, then insert or update"""
        try:
            with ConnMongoDB(**self.db_config) as _db:
                _data = dict(self.__dict__)
                _data.pop('openbrim')
                _data.pop('db_config')
                _data['_id']=self.id
                _id = _db.insert_data(collection, **_data)
                # _id = _db.insert_elmt(collection, self)
                #@TODO
                self.id = _id  # if no id, then return the ObjectId as self.id
                print("{}.id has been changed to {}".format(self.name, _id))
        except BaseException as e:
            print('Error when writing into MongoDB')
            raise e

    def mysql_read(self, id_name, table, *columns, fetch_type='ALL', with_des=False):
        try:
            with ConnMySQL(**self.db_config) as _db:
                _db.select(id_name, self.id, self.db_config['database'], table, *columns)
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
            with ConnMySQL(**self.db_config) as _db:
                return _db.insert(table, *data)
        except TypeError as e:
            print('<{}> Type Error\n  {}'.format(self.name, e))
        except BaseException as e:
            print('<{}> Error\n  {}'.format(self.name, e))

    def mysql_update(self, id_name, table, *data):
        """update the records of the element"""
        try:
            with ConnMySQL(**self.db_config) as _db:
                _condition = '{}={}'.format(id_name, self.id)
                _db.update(table, *data, condition=_condition)
                return
        except BaseException as e:
            raise e

    def describe(self, des):
        """describe, attached documents, etc"""
        assert isinstance(des, str)
        self.des = des


    def attr_to_dict(self):
        """dump some of the attributes to dict"""
        _d = dict(**self.__dict__)
        # some attribute cannot be imported to MongoDB
        _d.pop('openbrim')
        _d.pop('db_config')
        return _d



class AbstELMT(PyElmt):

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """abstract elements, such as material, section, load case"""
        super(AbstELMT, self).__init__(elmt_type, elmt_id, elmt_name)


class RealELMT(PyElmt):
    """PyReal is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(RealELMT, self).__init__(elmt_type, elmt_id, elmt_name)
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
