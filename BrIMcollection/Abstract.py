#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python BrIM for Abstract element
"""
from BrIMcollection.PyBrIM import *


class Parameter(AbstractBrIM):

    def __init__(self, id, para_name, para_value):
        super(Parameter, self).__init__(id, 'Parameter')
        self['name'] = para_name
        self['value'] = para_value


class Material(AbstractBrIM):
    _DESCRIBE_DICT = dict(d="Density",
                          E="Modulus of Elasticity",
                          a="Coefficient of Thermal Expansion",
                          Nu="Poisson's Ratio",
                          Fc28="Concrete Compressive Strength",
                          Fy="Steel Yield Strength",
                          Fu="Steel Ultimate Strength")

    def __init__(self, id, mat_type, **mat_property):
        """id is name, mat_type is 'Steel','Concrete', etc."""
        super(Material, self).__init__(id, mat_type, **mat_property)

    def show_mat_property(self):
        print('# Material Property <{}>'.format(self._id))
        for _k, _v in self.data.items():
            if _v:
                print(' - ', _k, '=', _v)

class Shape(AbstractBrIM):

    def __init__(self, id, shape_type, *node_list):
        super(Shape, self).__init__(id, shape_type)
        #@TODO

class Section(AbstractBrIM):

    def __init__(self, id, *shape, material=None):
        super(Section, self).__init__(id,'Section')
        self['material']=material
        for _s in shape:
            self[]

if __name__ == '__main__':
    p1 = Parameter(1, 'test_P', 20)
    print(p1.__dict__)
    print(p1.name)
    m1=Material('steel1','Steel', a=100, fc=599, fu=1111)
    # print(m1.__dict__)
    # print(m1.a)
    m1.show_mat_property()
