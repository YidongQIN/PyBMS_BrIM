#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""

from BMS_BrIM.Abstract import *







class Beam(PhysicalELMT):

    def __init__(self, node1, node2,
                 section, material=None,
                 beam_id=None, beam_name=None):
        self.link_node(node1, 1)
        self.link_node(node2, 2)
        self.set_section(section)
        self.set_material(material)
        super(Beam, self).__init__('Beam', beam_id, beam_name)
        self.set_openbrim(OBFELine, OBLine)


class Surface(PhysicalELMT):

    def __init__(self, node1, node2, node3, node4,
                 thick_prm, material,
                 deck_id=None, deck_name=None):
        super(Surface, self).__init__('Surface', deck_id, deck_name)
        # self.set_section(section)
        self.set_parameter('thick_prm', thick_prm)
        self.set_material(material)
        self.link_node(node1, 1)
        self.link_node(node2, 2)
        self.link_node(node3, 3)
        self.link_node(node4, 4)
        self.set_openbrim(OBFESurface, OBSurface)


if __name__ == '__main__':
    print("This is Py_Physical")
