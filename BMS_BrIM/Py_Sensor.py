#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
new sensor class in MongoDB instead of MySQL in lab
"""

from BMS_BrIM.Py_Physical import *


class Sensor(PhysicalELMT):

    def __init__(self, sensor_id, name, sensor_type='Sensor',
                 x=0, y=0, z=0, direction=None,
                 datapath=None, unit=None, channel=None,
                 *arg, **kwargs):
        super(Sensor, self).__init__(sensor_type, sensor_id, name)
        self.x, self.y, self.z = x, y, z
        self.direction = direction
        self.datapath = datapath
        self.unit, self.channel = unit, channel
        self.des = arg
        self.check_update_attr(kwargs)

    def install_at(self, *position):
        if isinstance(position[0], FENode):
            self.x, self.y, self.z = position[0].x, position[0].y, position[0].z
        elif len(position) == 3:
            self.x, self.y, self.z = position


class NetworkUnit(PhysicalELMT):

    def __init__(self, unit_id, experiment_id):
        super(NetworkUnit, self).__init__('UnitClient', unit_id, 'Unit_{}'.format(experiment_id))


class MonitorExperiment(object):

    def __init__(self, ext_id, bridge_id):
        self._id = ext_id
        self.bridge_id = bridge_id
