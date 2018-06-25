#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from BMS_BrIM.PyELMT import *


class ProjGroups(AbstractELMT):

    def __init__(self, name, template='empty'):
        """project is a new MongoDB, so no id"""
        super(ProjGroups, self).__init__('Project', elmt_id=0, elmt_name=name)
        self.template = template
        self.openbrim = OBProject(name, template)
        self.openbrim.sub(*self._proj_sub_groups())

    def _proj_sub_groups(self):
        self.prm_group = OBGroup('Parameter Group') #@TODO use class Group
        self.mat_group = OBGroup('Material Group')
        self.sec_group = OBGroup('Section Group')
        self.fem_group = OBGroup('FEM Model')
        self.geo_group = OBGroup('Geometry Model')
        return [self.prm_group, self.mat_group, self.sec_group, self.fem_group, self.geo_group]
        # self.sub(self.prm_group, self.mat_group, self.sec_group, self.fem_group, self.geo_group)

    # def _set_mongo_config(self, database=None, table=None, host='localhost', port=27017):
    #     super(ProjGroups, self)._set_mongo_config(self.name, table, host='localhost', port=27017)

    def set_dbconfig(self, database=None, table=None, **db_config):
        super(ProjGroups, self).set_dbconfig(self.name, table=None, **db_config)

    def set_mongo_doc(self):
        with ConnMongoDB(**self.db_config) as _db:
            self.projinfo = _db.insert_data('ProjectInfo',
                                            _id=0, OpenBrIM_Template=self.template)
            self.prm_mongo=_db.insert_data('Parameter')
            self.mat_mongo=_db.insert_data('Material')
            self.sec_mongo=_db.insert_data('Section')
            self.fem_mongo=_db.insert_data('FEM Model')
            self.geo_mongo=_db.insert_data('Geometry Model')

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
                else:
                    # all other elements are Real, have both fem and geo
                    self.fem_group.sub(member)
                    self.geo_group.sub(member)
            except BaseException as e:
                print('= = Some error about {} has been ignored'.format(member.name))
                print(e)

class Group(AbstractELMT):

    def __init__(self, name):
        super(Group, self).__init__('Group',None,name)
        self.openbrim:OBGroup=None
        self.db_config=None
        self.table_name=self.name#@TODO


class Parameter(AbstractELMT):

    def __init__(self, prm_id, prm_name, prm_value):
        super(Parameter, self).__init__('Parameter', prm_id, prm_name)
        self.value = prm_value


class Material(AbstractELMT):
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

    def set_openbrim(self, model_class='abst', ob_class=OBMaterial, **attrib_dict):
        _mat_attr = PyElmt._attr_pick(self, 'name', 'des', 'id', *Material._describe_dict)
        return super(Material, self).set_openbrim(model_class, ob_class, **_mat_attr)
        # return self.openbrim[model_class]


class Section(AbstractELMT):
    pass


class BeamDesign(PhysicalELMT):

    def __init__(self, beam_id, beam_name):
        # init no so many parameters, put the points and nodes to set_model() methods
        super(BeamDesign, self).__init__('BEAM', beam_id, beam_name)
        self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = [None] * 6


class PlateDesign(PhysicalELMT):

    def __init__(self, plate_id):
        super(PhysicalELMT, self).__init__('Plate', plate_id)
