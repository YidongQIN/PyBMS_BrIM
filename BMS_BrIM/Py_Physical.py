#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""

from BMS_BrIM.Py_Abstract import *
from Interfaces import *


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
        self.sectoin: Section = None
        # init the OpenBrIM model
        self.set_openbrim()

    @property
    def obrim(self):
        return self.openBrIM

    @obrim.setter
    def obrim(self, *ob_classes):
        assert len(ob_classes) == 2
        if not ob_classes[0] in [OBFESurface, OBFENode, OBFELine]:
            print("Wrong OpenBrIM FEM class")
            raise ValueError
        if not ob_classes[1] in [OBLine, OBSurface, OBVolume, OBCircle, OBExtends]:
            print("Wrong OpenBrIM FEM class")
            raise ValueError
        self.get_openbrim(*ob_classes)

    def set_openbrim(self, ob_class_fem=None, ob_class_geo=None, **attrib_dict):
        if not ob_class_fem:
            ob_class_fem = PhysicalELMT._DICT_FEM_CLASS[self.type]
        if not ob_class_geo:
            ob_class_geo = PhysicalELMT._DICT_FEM_CLASS[self.type]
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

    def link_node(self, node):
        """link to a Node"""



class Beam(PhysicalELMT):

    def __init__(self, node1: Node, node2: Node,
                 section: Section, material: Material,
                 beam_id=None, beam_name=None):
        self.material_id = material._id
        self.section_id = section._id
        self.node1OB = node1.openBrIM
        self.node2OB = node2.openBrIM
        self.sectionOB = section.openBrIM
        super(Beam, self).__init__('Beam', beam_id, beam_name)
        self.set_openbrim(OBFELine, OBLine)


class Deck(PhysicalELMT):

    def __init__(self, node1: Node, node2: Node, node3: Node, node4: Node,
                 section: Section, material: Material,
                 deck_id=None, deck_name=None):
        self.material_id = material._id
        self.section_id = section._id
        self.nodes_id = [node1._id, node2._id, node3._id, node4._id]
        super(Deck, self).__init__('Deck', deck_id, deck_name)


if __name__ == '__main__':
    print("This is Py_Physical")
