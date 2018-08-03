#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""
from BMS_BrIM.PyELMT import *


class Node(PhysicalELMT):

    def __init__(self, x, y, z=0,
                 dx=0, dy=0, dz=0,
                 rx=0, ry=0, rz=0,
                 node_id=None, node_name=None):
        super(Node, self).__init__('Node', node_id, node_name)
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.rx = rx
        self.ry = ry
        self.rz = rz


class Beam(PhysicalELMT):

    def __init__(self, node1:Node, node2:Node, beam_id, section_id, material_id, beam_name):
        #@TODO node OR node_id?
        self.material=material_id
        self.section=section_id
        self.nodes=[node1, node2]
        super(Beam, self).__init__('Beam', beam_id, beam_name)

class Deck(PhysicalELMT):
    pass

if __name__ == '__main__':
    print("This is Py_Physical")
