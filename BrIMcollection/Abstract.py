#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python BrIM for Abstract element
"""
from BrIMcollection.PyBrIM import *


class Parameter(PyBrIM):

    def __init__(self, id, para_name, para_value):
        super(Parameter, self).__init__(id, 'Parameter')
        self['name']=para_name
        self['value']=para_value


if __name__ == '__main__':
    p1=Parameter(1, 'test_P', 20)
    print(p1.__dict__)
    print(p1.name)
