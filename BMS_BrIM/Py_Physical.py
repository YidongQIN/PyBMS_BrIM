#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""

from BMS_BrIM.Py_Abstract import *


class PhysicalELMT(PyElmt):
    """PhysicalELMT is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""
    _DICT_FEM_CLASS = dict(Node=OBFENode,
                           Line=OBFELine,
                           Beam=OBFELine,
                           Truss=StraightBeamFEM,
                           Surface=OBFESurface,
                           BoltedPlate=OBFESurface,
                           Volume=OBVolume)
    _DICT_GEO_CLASS = dict(Node=OBPoint,
                           Line=OBLine,
                           Beam=OBLine,
                           Truss=OBLine,
                           Surface=OBSurface,
                           BoltedPlate=BoltedPlateGeo,
                           Volume=OBVolume)

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(PhysicalELMT, self).__init__(elmt_type, elmt_id, elmt_name)
        self.material: Material = None
        self.section: Section = None
        self.node: list = list()
        self.openBrIM=dict(fem=None, geo=None)
        # init the OpenBrIM model
        self.set_openbrim()


    def set_openbrim(self, ob_class_fem=None, ob_class_geo=None, **attrib_dict):
        if not ob_class_fem:
            ob_class_fem = PhysicalELMT._DICT_FEM_CLASS[self.type]
        if not ob_class_geo:
            ob_class_geo = PhysicalELMT._DICT_FEM_CLASS[self.type]
        # set fem openbrim model
        _ob_models = list()
        for _ob in ob_class_fem, ob_class_geo:
            # openBrIM is one of the PyELMT interfaces
            _ob_elmt = PyElmt.set_openbrim(self, _ob, **attrib_dict)
            _ob_models.append(_ob_elmt)
        self.openBrIM = dict(zip(['fem', 'geo'], _ob_models))
        return self.openBrIM

    def set_material(self, material):
        """ openbrim & mongodb"""
        self.material = material
        self.materialOB = material.openBrIM
        self.material_id = material._id

    def set_section(self, section):
        self.section = section
        self.sectionOB = section.openBrIM
        self.section_id = section._id

    def link_node(self, node, node_num):
        """link to a Node"""
        self.__dict__["node{}".format(node_num)]=node
        self.__dict__["node{}OB".format(node_num)]=node.openBrIM
        self.__dict__["node{}_id".format(node_num)]=node._id
        # self.nodeOB.append(node.openBrIM)


class Beam(PhysicalELMT):

    def __init__(self, node1, node2,
                 section, material,
                 beam_id=None, beam_name=None):
        self.set_material(material)
        self.set_section(section)
        self.link_node(node1,1)
        self.link_node(node2,2)
        super(Beam, self).__init__('Beam', beam_id, beam_name)
        self.set_openbrim(OBFELine, OBLine)


class Deck(PhysicalELMT):

    def __init__(self, node1, node2, node3, node4,
                 section, material,
                 deck_id=None, deck_name=None):
        self.set_material(material)
        self.set_section(section)
        self.link_node(node1, 1)
        self.link_node(node2, 2)
        self.link_node(node3, 3)
        self.link_node(node4, 4)
        super(Deck, self).__init__('Deck', deck_id, deck_name)


if __name__ == '__main__':
    print("This is Py_Physical")
