#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
import collections


class PyBrIM(collections.UserDict):

    def __init__(self, brim_id, brim_type, **brim_data):
        self._id = brim_id
        self.type = brim_type
        super(PyBrIM, self).__init__(**brim_data)

    @property
    def brim(self):
        """rename the UserDict.data{} as PyBrIM.brim{}"""
        return self.data

    def __repr__(self):
        return "{}_{}".format(self.type, self._id)

    def __iter__(self):
        return iter(self.data.items())
        # return iter(self.data.items())

    def __getattr__(self, item):
        try:
            return self.data[item]
        except KeyError:
            print("No attribute:", item)
            return

    def __setattr__(self, key, value):
        if key in ('_id', 'type', 'data'):
            super(PyBrIM, self).__setattr__(key, value)
        elif key in self.data.keys():
            super(PyBrIM, self).__setitem__(key, value)
        else:
            print("New attribute:", key, "=", value)
            #@TODO how to check if the new item is supported?
            super(PyBrIM, self).__setitem__(key, value)


if __name__ == '__main__':
    test = PyBrIM(1, 'test', section='sss', mat='material')
    print(test.__dict__)
    print(test.section)
    test.section = "re sec"
    test.wrong = "new section"
    print(test.section)
    print(test.__dict__)
