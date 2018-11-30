#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
import collections
import json


class PyBrIM(collections.UserDict):

    def __init__(self, brim_id, brim_type, **brim_data):
        self._id = brim_id
        self.type = brim_type
        super(PyBrIM, self).__init__(**brim_data)

    def link(self, key: str, element):
        if isinstance(element, PyBrIM):
            self.__setitem__(key, element)

    def __str__(self):
        return "{}_{}\n  ->{}".format(self.type, self._id,
                                      super(PyBrIM, self).__str__())

    def jsondumps(self):
        return json.dumps(self, indent=4, default=lambda obj: obj.__dict__)

    def __iter__(self):
        return iter(self.data.items())

    # attributes can be used for getting information, but not recommended
    def __setattr__(self, key, value):
        if key in ('_id', 'type', 'data'):
            # print('set default attr', key)
            super(PyBrIM, self).__setattr__(key, value)
        elif key in self.data.keys():
            print('set attr in .data items', key)
            super(PyBrIM, self).__setitem__(key, value)
        else:
            print("New attribute:", key, "=", value)
            super(PyBrIM, self).__setitem__(key, value)

    def __getattr__(self, item):
        try:
            return self.data[item]
        except KeyError:
            print("No attribute found:", item)
            return

    def __delattr__(self, item):
        try:
            super(PyBrIM, self).__delattr__(item)
        except AttributeError:
            try:
                super(PyBrIM, self).__delitem__(item)
            except KeyError:
                print('Cannot find attribute to del:', item)


class DocumentBrIM(PyBrIM):

    def __init__(self, brim_id, brim_type, **brim_data):
        super(DocumentBrIM, self).__init__(brim_id, brim_type, **brim_data)


class EquipmentBrIM(PyBrIM):
    pass


class AbstractBrIM(PyBrIM):
    pass


class PhysicalBrIM(PyBrIM):
    pass


if __name__ == '__main__':
    mat = PyBrIM(2, 'material', a=100, fc=999)
    # print(mat.jsondumps())
    test = PyBrIM(1, 'non-type', section='SECT', material='MAT')
    test.link('material', mat)
    print(test)
    print(test.jsondumps())
