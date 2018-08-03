# usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
BrIM use database to store the information of elements.
structural members, like beams, columns, are stored in NoSQL
and non-structural members, such as sensor, etc.

"""

import bson
import pymongo as mg


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
        print("All documents in <{}> are:".format(collection))
        cursor = self.db[collection].find()
        for i in cursor:
            print('  - ' + str(i))

    def insert_data(self, collection, **data):
        try:
            return self.db[collection].insert({**data})
        except mg.errors.DuplicateKeyError:
            print("This document already exists")
        except bson.errors.InvalidDocument:
            print("Cannot encode object")

    def update_data(self, collection, id, **data):
        """equals to: return self.db[collection].update({'_id': id}, data, True)"""
        if self.find_by_kv(collection, '_id', id):
            print('Find this doc._id = {} in MongoDB'.format(id))
            # later, maybe use findall to check if exist doc of same content
            return self.db[collection].update({'_id': id}, data, True)
        else:
            print('Insert into MongoDB')
            return self.insert_data(collection, **data)

    # below are methods for element, should not be use.
    # Mongo focus on the methods of CURD in Mongo, not info process of element
    '''''''''
    def update_elmt(self, collection, elmt):
        """first find, then update or insert"""
        try:
            if self.find_by_kv(collection, '_id', elmt.id):
                print("Document <'_id'> = {} already exits".format(elmt.id))
            else:
                print('New document will be inserted.')
            self.update_data(collection, elmt.id, **self.modify_field_value(elmt))
            # self.db[collection].update({'_id': elmt.__dict__['id']}, self.modify_field_value(elmt), True)
        except AttributeError as e:
            print("The elmt <{}> does not have a <'id'> attribute".format(elmt.name or elmt))
            print(e)

    def insert_elmt(self, collection, elmt):
        """elmt has __dict__"""
        self.insert_data(collection, **self.modify_field_value(elmt))

    def delete_elmt(self, collection, elmt):
        try:
            if self.find_by_kv(collection, '_id', elmt.id):
                self.db[collection].delete_one({'_id': elmt.id})
                print('Successfully Delete the element whose id={}'.format(elmt.id))
            else:
                print('Cannot find such a document in Collection <{}> with id={}'.format(collection, elmt.id))
        except:
            print('Deleting element <{}> error'.format(elmt))
            raise

    @staticmethod
    def modify_field_value(elmt, *pop_list):
        """transfer the element to dict of attributes.
                        no empty attribute and change 'id' to '_id'. """
        from BMS_BrIM import ABrIMELMT
        assert isinstance(elmt, ABrIMELMT.PyElmt)
        field_value = dict()
        for _key, _value in elmt.__dict__.items():
            if _value:
                field_value[_key] = _value
        try:
            field_value['_id'] = field_value['id']
            print("Document's '_id' is {}".format(field_value['_id']))
            field_value.pop('id')
        except KeyError:
            print("No '_id' field contained, will be assigned automatically")
        for _pop in pop_list:
            field_value.pop(_pop)
        field_value.pop('openbrim')
        field_value.pop('db_config')
        return field_value
    '''''''''


if __name__ == "__main__":
    with ConnMongoDB('fours') as db:
        db.have_a_look('Parameter')
