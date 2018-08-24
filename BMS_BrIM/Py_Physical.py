#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Physical Elements
"""

from BMS_BrIM.Py_Abstract import *

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


class PhysicalELMT(PyElmt):
    """PhysicalELMT is used to represent real members of bridges.
    it contains parameters of the element, by init() or reading database.
    Thus it could exports geometry model, FEM model and database info
    later, some other methods may be added, such as SAP2K model method"""

    def __init__(self, elmt_type, elmt_id, elmt_name=None):
        """real members of structure"""
        super(PhysicalELMT, self).__init__(elmt_type, elmt_id, elmt_name)
        self.material: Material = None
        self.section: Section = None
        self.node: list = list()
        self.openBrIM = dict(fem=None, geo=None)

    def set_openbrim(self, ob_class_fem=None, ob_class_geo=None, **attrib_dict):
        if not ob_class_fem:
            ob_class_fem = _DICT_FEM_CLASS[self.type]
        if not ob_class_geo:
            ob_class_geo = _DICT_FEM_CLASS[self.type]
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
        if material:
            self.material = material
            self.material_ob = material.openBrIM
            self.material_id = material._id
        else:
            self.material_ob = self.section.material_ob
            self.material_id = self.section.material_id

    def set_section(self, section):
        self.section = section
        self.section_ob = section.openBrIM
        self.section_id = section._id

    def set_parameter(self, p_name, parameter):
        self.__dict__[p_name] = parameter
        self.__dict__["{}_ob".format(p_name)] = parameter.openBrIM
        self.__dict__["{}_id".format(p_name)] = parameter._id

    def link_node(self, node, node_num):
        """link to a Node"""
        self.__dict__["node{}".format(node_num)] = node
        self.__dict__["node{}_ob".format(node_num)] = node.openBrIM
        self.__dict__["node{}_id".format(node_num)] = node._id
        # self.nodeOB.append(node.openBrIM)



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
        self.set_material(material)
        # self.set_section(section)
        self.set_parameter('thick_prm', thick_prm)
        self.link_node(node1, 1)
        self.link_node(node2, 2)
        self.link_node(node3, 3)
        self.link_node(node4, 4)
        super(Surface, self).__init__('Surface', deck_id, deck_name)
        self.set_openbrim(OBFESurface, OBSurface)


if __name__ == '__main__':
    print("This is Py_Physical")
