# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Bridge inspection information
"""

from BMS_BrIM.PyELMT import *


class Damage(object):
    def __init__(self):
        self.status='Commm'

    def inspected(self):
        print(self.status)
        self.status='IIIII'
        print(self.status)

class Corrosion(Damage):
    pass

class Deformation(Damage):
    pass

class CoatingDamage(Damage):
    pass

class Loose(Damage):
    pass

if __name__ == '__main__':
    a = PyELMT
