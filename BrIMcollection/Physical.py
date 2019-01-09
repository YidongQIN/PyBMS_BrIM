#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical brim element
"""
import re

import numpy as np

from BrIMcollection.PyBrIM import *


class Beam(PhysicalBrIM):

    def __init__(self, node1, node2, section, material, id=None):
        super(Beam, self).__init__(id, 'Beam', material=material)
        self.link('node_1', node1)
        self.link('node_2', node2)
        self.link('section', section)


class Surface(PhysicalBrIM):

    def __init__(self, node1, node2, node3, node4,
                 thick_prm, material, id=None):
        super(Surface, self).__init__(id, 'Surface', material=material)
        self.link('node_1', node1)
        self.link('node_2', node2)
        self.link('node_3', node3)
        self.link('node_4', node4)
        self.link('thickness', thick_prm)


class Sensor(PhysicalBrIM):

    def __init__(self, type, id, **kwargs):
        """**kwargs = *, x=0, y=0, z=0, fenode, direction=None,
        unit=None, channel: str = None,manufacture_model, sensor_data"""
        super(Sensor, self).__init__(id, type)
        for k, v in kwargs:
            self.link(k, v)

    def store_data(self, sensor_data):
        """store the data in a .dat file or MongoDB?"""
        if isinstance(sensor_data, str):
            assert re.match('.*\.dat', sensor_data)
            print("Sensor {} data is store a the file:".format(self.name), sensor_data)
            return np.loadtxt(sensor_data).tolist()
        elif isinstance(sensor_data, list):
            for _d in sensor_data:
                assert isinstance(_d, (float, int))
            print("Total number of sensor data is", len(sensor_data))
            return sensor_data

    def install_position(self, *position):
        """a FENode or 3 coordinates"""
        try:
            if len(position) == 1 and isinstance(position[0], FENode):
                _x, _y, _z = position[0].x, position[0].y, position[0].z
            elif len(position) == 3:
                _x, _y, _z = position
                assert isinstance(_x, (float, int))
                assert isinstance(_y, (float, int))
                assert isinstance(_z, (float, int))
            else:
                print("! Position Error {}".format(self.name))
                return
        except AttributeError:
            print("Position not defined.")
            return
        return _x, _y, _z

    def unit_channel_install(self, unit, channel: str):
        """"""
        try:
            if channel in unit.channel:
                print("Confirmed Channel: {}.{}->{}".format(unit.name, channel, self.name))
            else:
                print("No channel, should define the channel first.")
        except AttributeError:
            print("Unit and channel are not defined.")
        return unit, channel

    def manufacture(self, manufacture, model):
        self.link('manufacture', manufacture)
        self.link('model', model)


class TemperatureSensor(Sensor):

    def __init__(self, id, **kwargs):
        super(TemperatureSensor, self).__init__('TemperatureSensor', id, **kwargs)


class StrainGauge(Sensor):

    def __init__(self, id, **kwargs):
        super(StrainGauge, self).__init__('StrainGauge', id, **kwargs)


class Accelerometer(Sensor):

    def __init__(self, id, **kwargs):
        super(Accelerometer, self).__init__('Accelerometer', id, **kwargs)


class Displacemeter(Sensor):

    def __init__(self, id, **kwargs):
        super(Displacemeter, self).__init__('Displacemeter', id, **kwargs)


if __name__ == '__main__':
    from BrIMcollection.Abstract import *

    n1 = FENode(0, 0, 0, id=1)
    n2 = FENode(2, 0, 0, id=2)
    n3 = FENode(3, 0, 0, id=3)
    n4 = FENode(4, 0, 0, id=4)
    n5 = FENode(5, 0, 0, id=5)
    m1 = Material('Steel', f=66, id='m1')
    sec = Section(ShapeRectangle(5, 5), id='sect')
    b1 = Beam(n1, n2, sec, m1, id=100)
    print(b1)
