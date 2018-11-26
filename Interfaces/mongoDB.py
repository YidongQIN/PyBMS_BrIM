#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
问题是这个mongo与openbrim的逻辑不通。ob打包了一个elmt用于处理所有数据，而这个mongo直接操作了数据库，即直接在self上进行操作。
"""
import bson
import pymongo as mg
# from Interfaces.toMongo import *



class ConnMongoDB(object):

    def __init__(self, database, host='localhost', port=27017, **kwargs):
        self.host = host
        self.port = port
        self.db_name = database
        if 'table' in kwargs.keys():
            self.collection = kwargs['table']
        self.client = mg.MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        # print("MongoDB connected.\n -  <{}> has collections of:\n\t{}".format(self.db_name, self.db.collection_names(False)))

    def __enter__(self, new_db_name=None):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('MongoDB connection finished')
        if exc_tb:
            print("Mongo Error Type : {}".format(exc_type))
            print("----- Error Value: {}".format(exc_val))
            print("----- Error is at: {}".format(exc_tb))

    def new_db(self, new_db_name):
        self.db_name = new_db_name
        self.db = self.client[self.db_name]

    def col_find_one(self, collection, condition, if_print):
        """ if the condition is not just one field"""
        _result = self.db[collection].find_one(condition)
        if if_print:
            print("Searched Collection of <{}> where {}".format(collection, condition))
            if _result:
                for _k, _v in _result.items():
                    print(' -  ', _k, '=', _v)
            else:
                print(" -  NO document")
        return _result

    def col_find_all(self, collection, condition):
        """ if the condition is not just one field"""
        cursor = self.db[collection].find(condition)
        _l = [doc for doc in cursor]
        print("Searched in <{}> where {}".format(collection, condition))
        print(
            "Found {} document(s)".format(len(_l)))
        if _l:
            for a in _l:
                print("  - {}".format(a))
        return _l

    def find_by_kv(self, collection, key_field, value, if_print=False):
        """find one document and return a BSON"""
        _condition = {key_field: value}
        # print('find by kv',self.col_find_one(collection, _condition))
        return self.col_find_one(collection, _condition, if_print)

    def findall_by_kv(self, collection, key_field, value):
        """find all documents matched the condition, return a list"""
        _condition = {key_field: value}
        return self.col_find_all(collection, _condition)

    def have_a_look(self, collection):
        print("Docs in <{}>:".format(collection))
        cursor = self.db[collection].find()
        for i in cursor:
            print('  - ' + str(i))

    def insert_data(self, collection, **data):
        try:
            return self.db[collection].insert({**data})
        except mg.errors.DuplicateKeyError:
            print("#Existed doc in collection <{}>".format(collection))
            print(" -", data)
        except bson.errors.InvalidDocument as e:
            print("!Encoding object to {} error:".format(collection), e)
            print(" -", data)

    def update_data(self, collection, id, **data):
        """equals to: return self.db[collection].update({'_id': id}, _data, True)"""
        if self.find_by_kv(collection, '_id', id):
            print('Existed doc in <{}>, ._id={}'.format(collection, id))
            # later, maybe use findall to check if exist doc of same content
            return self.db[collection].update({'_id': id}, data, True)
        else:
            print('New doc in <{}>, ._id={}'.format(collection, id))
            return self.insert_data(collection, **data)


class hasMongo(object):

    def __init__(self, _id):
        self._id = _id

    def _attr_to_mongo_dict(self):
        def is_unacceptable(one_item):
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
            _pop_key = list(set(_pop_key))
            return _pop_key

        _after_pop = self.attr_pop(self, *_pop_list(self))
        return _after_pop

    def set_mongo_config(self, database, table, host='localhost', port=27017):
        """get db config and connect to MongoDB"""
        self.db_config = {'database': database, 'table': table,
                          'host': host, 'port': port, }

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
