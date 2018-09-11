#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
from Interfaces.toMongo import *
from Interfaces.BrIMInterface import BrIMInterface



class hasMongo(BrIMInterface):

    def __init__(self, _id):
        self._id = _id

    def _attr_to_mongo_dict(self):
        def is_unacceptable(one_item):
            # _unaccept_type = (PyELMT, PyOpenBrIMElmt)

            if not isinstance(one_item, (str, int, float)):
                return True
            return False

        def should_pop(attribute_value):
            if isinstance(attribute_value, (tuple, list)):
                _to_list = list(attribute_value)
                return is_unacceptable(_to_list[0])
            return is_unacceptable(attribute_value)

        def _pop_list(elmt):
            _pop_key = ['db_config', 'openBrIM']
            for _k, _v in elmt.__dict__.items():
                if should_pop(_v):
                    _pop_key.append(_k)
            _pop_key=list(set(_pop_key))
            return _pop_key

        _after_pop = self.attr_pop(self, *_pop_list(self))
        return _after_pop


    def set_mongo_config(self, database, table, host='localhost', port=27017):
        """get db config and connect to MongoDB"""
        self.db_config = {'database': database, 'table': table,
                          'host': host, 'port': port,}

    def set_mongo_doc(self):
        """write info into the mongo.collection.document"""
        with ConnMongoDB(**self.db_config) as _db:
            _col = self.db_config['table']
            if not self._id:
                self._id = _db.insert_data(_col, **self._attr_to_mongo_dict())
            elif not _db.find_by_kv(_col, 'name', self.name):
                _ = _db.update_data(_col, self._id, **self._attr_to_mongo_dict())
            else:
                _db.update_data(_col, self._id, **self._attr_to_mongo_dict())
                print("{}._id is set to {} based on MongoDB doc".format(self.name, self._id))

    def get_mongo_doc(self, if_print=False):
        with ConnMongoDB(**self.db_config) as _db:
            _result = _db.find_by_kv(self.db_config['table'], '_id', self._id, if_print)
            self.update(**_result)
            return _result






if __name__ == '__main__':
    pass
