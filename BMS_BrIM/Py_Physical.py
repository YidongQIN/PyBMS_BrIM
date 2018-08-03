#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""
from BMS_BrIM.Py_Abstract import *


class Node(PhysicalELMT):

    def __init__(self, x, y, z=0,
                 tx=0, ty=0, tz=0,
                 rx=0, ry=0, rz=0,
                 node_id=None, node_name=None):
        super(Node, self).__init__('Node', node_id, node_name)
        self.x = x
        self.y = y
        self.z = z
        self.tx = tx
        self.ty = ty
        self.tz = tz
        self.rx = rx
        self.ry = ry
        self.rz = rz
        self.set_openbrim(OBFENode, OBPoint)

    def set_node_attr(self, node_attr, value):
        assert node_attr in ['x', 'y', 'z', 'tx', 'ty', 'tz', 'rx', 'ry', 'rz']
        self.__dict__[node_attr] = value
        # update the mongoDB and openbrim
        self.set_openbrim()
        self.set_mongo_doc()


class Beam(PhysicalELMT):

    def __init__(self, node1: Node, node2: Node, section: Section, material: Material, beam_id=None, beam_name=None):
        self.material = material
        self.section = section
        self.nodes = [node1, node2]
        super(Beam, self).__init__('Beam', beam_id, beam_name)


class Deck(PhysicalELMT):

    def __init__(self, node1: Node, node2: Node, node3: Node, section: Section, material: Material,
                 deck_id=None, deck_name=None):
        self.material = material
        self.section = section
        self.nodes = [node1, node2, node3]
        super(Deck, self).__init__('Deck', deck_id, deck_name)


if __name__ == '__main__':
    print("This is Py_Physical")
