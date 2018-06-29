#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python Elements for BrIM. 
"""

from BMS_BrIM.PyELMT import *


class Parameter(AbstractELMT):

    def __init__(self, prm_id, prm_name, prm_value):
        super(Parameter, self).__init__('Parameter', prm_id, prm_name)
        self.value = prm_value


class Material(AbstractELMT):
    _DESCRIBE_DICT = dict(d="Density",
                          E="Modulus of Elasticity",
                          a="Coefficient of Thermal Expansion",
                          Nu="Poisson's Ratio",
                          Fc28="Concrete Compressive Strength",
                          Fy="Steel Yield Strength",
                          Fu="Steel Ultimate Strength")

    def __init__(self, mat_id, mat_name, **mat_property):
        """Material name is mandatory. Material Type is Steel, Concrete, etc."""
        super(Material, self).__init__('Material', mat_id, mat_name)
        # self.stage = 'Design'
        if mat_property:
            self.set_property(**mat_property)

    def set_property(self, **mat_property):
        """set the property of material. should use key in:
        [d, E, a, Nu, Fc28, Fy, Fu]"""
        print("Material <{}> property setting:".format(self.name))
        for _k, _v in mat_property.items():
            self.__dict__[_k] = _v
            print("  - {}={}\t".format(_k, _v), end='')
            try:
                print('#', Material._DESCRIBE_DICT[_k])
            except KeyError:
                print("! UnKnown property")

    def show_material_property(self):
        print('# Material Property <{}>'.format(self.name))
        for _k, _v in self.__dict__.items():
            if _v:
                print(' - ', _k, '=', _v)

    # def set_openbrim(self, ob_class=OBMaterial, **attrib_dict):
    #     _mat_attr = PyElmt._attr_pick(self, 'name', 'des', 'id', *ob_class._REQUIRE)
    #     self.openBrIM = super(Material, self).set_openbrim(ob_class, **_mat_attr)
    #     return self.openBrIM
    # return self.openbrim[model_class]


class Shape(AbstractELMT):
    pass


class Section(AbstractELMT):
    pass


class Group(AbstractELMT):
    """Container of PyELMT = a OBGroup"""

    def __init__(self, name, *child):
        super(Group, self).__init__('Group', None, name)
        self.openBrIM = OBGroup(name)
        self.sub = list(*child)

    def append(self, *child):
        """get sub nodes, both the PyELMT and the OpenBrIM"""
        for _c in child:
            assert isinstance(_c, PyElmt)
            self.sub.append(_c)
            try:
                if isinstance(_c, AbstractELMT):
                    self.openBrIM.sub(_c.openBrIM)
                elif isinstance(_c, PhysicalELMT):
                    self.openBrIM.sub(_c.openBrIM['fem'])
                    self.openBrIM.sub(_c.openBrIM['geo'])
            except TypeError:
                print("! {} cannot add {}'s openBrIM Element".format(self.name, _c.name))

    def delete(self, *child):
        for _c in child:
            try:
                self.sub.pop(_c)
                self.openBrIM.del_sub(_c.openBrIM.elmt.tag, **_c.openBrIM.elmt.attrib)
            except TypeError:
                print("! {} cannot delete {}".format(self.name, _c.name))

    def __iter__(self):
        return self

    def __next__(self):
        return self.sub


class GroupCollection(Group):
    """A project has 6 groups, and these 6 groups are collections(tables) in MongoDB.
    PS: not all groups will be seen in MongoDB."""
    _DESCRIBE_DICT = {
        'basic_info': 'Basic Information about the project',
        'parameter': 'parameters of the model',
        'material': 'all materials',
        'section': 'all sections and shapes',
        'model_fem': 'FEM model, including FENodes, FELines, FESurfaces, etc',
        'model_geometry': 'Geometry Model',
    }

    def __init__(self, name, des=None):
        super(GroupCollection, self).__init__(name)
        self.mongoCollectionName = self.name
        if not des:
            try:
                des = GroupCollection._DESCRIBE_DICT[name]
            except KeyError:
                des = "Unknown Group. A NEW table/Collection in MongoDB."
        self.des = des  # description of the collection as _id=0


class ProjGroups(AbstractELMT):
    """a BrIM Project = Mongo Database = OpenBrIM_Project.
    There should be 6 groups( = collections = tables) where all info is stored.
    """

    def __init__(self, name, template='empty'):
        """project is a new MongoDB, so no id"""
        super(ProjGroups, self).__init__('Project', elmt_id=0, elmt_name=name)
        self.template = template
        self.openBrIM = OBProject(name, template)
        # Project cannot append sub, only its groups can
        self._proj_sub_groups()
        # automatically set up the MongoDB config
        self.set_dbconfig()
        self._init_mongo_doc()

    def _proj_sub_groups(self):
        self.proj_info = GroupCollection('basic_info')
        self.prm_group = GroupCollection('parameter')
        self.mat_group = GroupCollection('material')
        self.sec_group = GroupCollection('section')
        self.fem_group = GroupCollection('model_fem')
        self.geo_group = GroupCollection('model_geometry')
        self.sub = [self.proj_info, self.prm_group,
                    self.mat_group, self.sec_group,
                    self.fem_group, self.geo_group]
        for _s in self.sub:
            self.openBrIM.sub(_s.openBrIM)
        return self.sub

    def set_dbconfig(self, database=None, table=None, **db_config):
        super(ProjGroups, self).set_dbconfig(self.name, table=None, **db_config)

    def _init_mongo_doc(self):
        with ConnMongoDB(**self.db_config) as _db:
            for _col in self.sub:
                _db.update_data(_col.name, id=0, des=_col.des)

    def update_mongo(self):
        pass
