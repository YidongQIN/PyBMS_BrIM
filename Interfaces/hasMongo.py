#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
from Interfaces.toMongo import *
from Interfaces.BrIM_interface import BrIM_interface


class hasMongo(BrIM_interface):

    def __init__(self, _id):
        self._id = _id


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
                _ = _db.update_data(_col, self._id, **_attr_to_mongo_dict(self))
            else:
                _db.update_data(_col, self._id, **_attr_to_mongo_dict(self))
                print("{}._id is set to {} based on MongoDB doc".format(self.name, self._id))

    def get_mongo_doc(self, if_print=False):
        with ConnMongoDB(**self.db_config) as _db:
            _result = _db.find_by_kv(self.db_config['table'], '_id', self._id, if_print)
            self.update_attr(**_result)
            return _result




if __name__ == '__main__':
    pass
