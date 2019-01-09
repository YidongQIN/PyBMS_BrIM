#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
from BrIMcollection.PyBrIM import *


class NetworkUnit(PhysicalBrIM):

    def __init__(self, id, *channel, experiment=None):
        super(NetworkUnit, self).__init__(id, 'NetworkUnit')
        self['channel'] = channel
        self.link('experiment', experiment)

    def channel_install(self, **channel_sensor):
        self.channel_sensor: dict
        for _c, _s in channel_sensor.items():
            assert isinstance(_c, str) and isinstance(_s, Sensor), TypeError
            if _c not in self.channel:
                print("! New channel <{}> added to {}".format(_c, self.name))
            self.channel_sensor[_c] = _s._id


if __name__ == '__main__':
    from BrIMcollection.Physical import Sensor
