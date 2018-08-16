#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
new sensor class in MongoDB instead of MySQL in lab
"""
from BMS_BrIM.Py_Physical import *
from BMS_BrIM.Py_Abstract import Node


class Sensor(PhysicalELMT):

    def __init__(self, id, name, sensor_type='Sensor',
                 x=0, y=0, z=0, direction=None,
                 datapath=None, unit=None, channel=None,
                 *arg, **kwargs):
        super(Sensor, self).__init__(sensor_type, id, name)
        self.x, self.y, self.z = x, y, z
        self.direction = direction
        self.datapath = datapath
        self.unit, self.channel = unit, channel
        self.des = arg
        self.check_update_attr(kwargs)
        # self.set_openbrim(OBFENode, LineCubeOB,
        #                   line_length=30, line_radius=1,
        #                   cube_length=18, cube_width=12, cube_thick=8)

    def install_at(self, *position):
        if isinstance(position[0], Node):
            self.x, self.y, self.z = position[0].x, position[0].y, position[0].z
        elif len(position) == 3:
            self.x, self.y, self.z = position
