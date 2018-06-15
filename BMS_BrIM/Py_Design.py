#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from BMS_BrIM.PyELMT import *


class ProjGroups(AbstELMT):

    def __init__(self, name, template='empty'):
        super(ProjGroups, self).__init__(name, template)
        self.prm_group = OBGroup('Parameter Group')
        self.mat_group = OBGroup('Material Group')
        self.sec_group = OBGroup('Section Group')
        self.fem_group = OBGroup('FEM Model')
        self.geo_group = OBGroup('Geometry Model')
        self.sub(self.prm_group, self.mat_group, self.sec_group, self.fem_group, self.geo_group)

    def include(self, *members: PyElmt):
        """ add one member to the project"""
        for member in members:
            assert isinstance(member, PyElmt)
            # PyElmt may be abstract or real
            abs_dict = {'Parameter': self.prm_group,
                        'Section': self.sec_group,
                        'Material': self.mat_group}
            try:
                if member.type in abs_dict:
                    # abstract elements include Parameter, Section, Material
                    abs_dict[member.type].sub(member)
                    # @TODO member.model?
                else:
                    # all other elements are Real, have both fem and geo
                    self.fem_group.sub(member)
                    self.geo_group.sub(member)
            except BaseException as e:
                print('= = Some error about {} has been ignored'.format(member.name))
                print(e)


class Parameter(AbstELMT):

    def __init__(self, prm_id, prm_name, prm_value):
        super(Parameter, self).__init__('Parameter', prm_id, prm_name)
        self.value = prm_value


class Material(AbstELMT):
    _describe_dict = dict(d="Density",
                          E="Modulus of Elasticity",
                          a="Coefficient of Thermal Expansion",
                          Nu="Poisson's Ratio",
                          Fc28="Concrete Compressive Strength",
                          Fy="Steel Yield Strength",
                          Fu="Steel Ultimate Strength")

    def __init__(self, mat_id, mat_name):
        """Material name is mandatory. Material Type is Steel, Concrete, etc."""
        super(Material, self).__init__('Material', mat_id, mat_name)
        self.stage = 'Design'

    def set_property(self, **mat_dict):
        """set the property of material. should use key in:
        [d, E, a, Nu, Fc28, Fy, Fu]"""
        print("Set Material <{}> properties to:".format(self.name))
        for _k, _v in mat_dict.items():
            self.__dict__[_k] = _v
            print("- {}={}\t".format(_k, _v), end='')
            try:
                print('#', Material._describe_dict[_k])
            except KeyError:
                print("! UnKnown property")

    def set_openbrim(self, model_class='fem', ob_class=OBMaterial, **attrib_dict):
        _mat_attr = PyElmt._attr_pick(self, 'name', 'des', 'id', *Material._describe_dict)
        return super(Material, self).set_openbrim(model_class, ob_class, **_mat_attr)
        # return self.openbrim[model_class]


class Section(AbstELMT):
    pass


class BeamDesign(PhysicalELMT):

    def __init__(self, beam_id, beam_name):
        # init no so many parameters, put the points and nodes to set_model() methods
        super(BeamDesign, self).__init__('BEAM', beam_id, beam_name)
        self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = [None] * 6


class PlateDesign(PhysicalELMT):

    def __init__(self, plate_id):
        super(PhysicalELMT, self).__init__('Plate', plate_id)
