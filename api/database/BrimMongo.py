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
from gridfs import *


class brimMongo(object):

    def __init__(self, database, table=None, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.client = mg.MongoClient(self.host, self.port)
        self.db_name = database
        self.tb_name = table
        self.db = self.client[self.db_name]

    def __enter__(self, new_db_name=None):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('MongoDB connection finished')
        if exc_tb:
            print("Mongo Error Type : {}".format(exc_type))
            print("----- Error Value: {}".format(exc_val))
            print("----- Error is at: {}".format(exc_tb))

    def gridfs(self, fs_name='Photo'):
        """create / connect to the GridFS collections"""
        self.fs = GridFS(self.db, fs_name)

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

    def insert_file(self, pic_path, file_name):
        """read the pic in path, and insert into Mongo as the file_name"""
        with open(pic_path, 'rb') as image:
            data = image.read()
            id = self.fs.put(data, filename=file_name)
            print(file_name, '._id =', id)

    def get_file(self, file_name, save_folder, new_name=None):
        """:file_name is the name in MongoDB GridFS collection,
        save_folder is where to store the pic as a new file,
        if new_name is not assigned, the file_name is used for the new file."""
        file = self.fs.get_version(file_name, 0)
        data = file.read()
        if new_name:
            save_path = save_folder + new_name + '.png'
        else:
            save_path = save_folder + file_name + '.png'
        with open(save_path, 'wb') as out:
            print(save_path)
            out.write(data)

    def delFile(self, Obj_Id):
        self.fs.delete(Obj_Id)

    def listName(self):
        print(self.fs.list())

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
    pic_src = 'c:\\Users\\yqin78\\Proj.Python\\PyBMS_BrIM\\_data\\MARCpic\\Photos_1.jpg'
    pic_sv = 'c:\\Users\\yqin78\\Proj.Python\\PyBMS_BrIM\\_data\\MARCpic\\'

    with brimMongo('fours') as db:
        db.have_a_look('Parameter')
        db.gridfs('TestPh')
        db.insert_file(pic_src, 'test_gridfs')

    with brimMongo('fours') as db:
        db.gridfs('TestPh')
        db.listName()
        db.get_file('test_gridfs', pic_sv, 'read from gridfs')
