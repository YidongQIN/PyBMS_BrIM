#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
new sensor class in MongoDB instead of MySQL in lab
"""
from BMS_BrIM.Py_Physical import *


class Sensor(PhysicalELMT):

    def __init__(self, id, name, sensor_type='Sensor', x=0, y=0, z=0, direction='X'):
        super(Sensor, self).__init__(sensor_type, id, name)
        self.x = x
        self.y = y
        self.z = z
        self.direction = direction
        self.set_openbrim(OBFENode, CubeGeo, length=10, width=10, thick=10)
        self.openBrIM['geo'].set_basepoint(x, y, z)

    def install_at(self, node, direction):
        pass
