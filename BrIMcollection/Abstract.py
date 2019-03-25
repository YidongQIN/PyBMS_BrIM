#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
Python BrIM for Abstract element
"""

from BrIMcollection.PyBrIM import *


class Parameter(AbstractBrIM):

    def __init__(self, para_name, para_value, id=None):
        super(Parameter, self).__init__(id, 'Parameter')
        self['name'] = para_name
        self['value'] = para_value


class Material(AbstractBrIM):
    _DESCRIBE_DICT = dict(d="Density",
                          E="Modulus of Elasticity",
                          a="Coefficient of Thermal Expansion",
                          Nu="Poisson's Ratio",
                          Fc28="Concrete Compressive Strength",
                          Fy="Steel Yield Strength",
                          Fu="Steel Ultimate Strength")

    def __init__(self, mat_type, id=None, **mat_property):
        """id is name, mat_type is 'Steel','Concrete', etc."""
        super(Material, self).__init__(id, mat_type, **mat_property)

    def show_mat_property(self):
        print('# Material Property <{}>'.format(self._id))
        for _k, _v in self.data.items():
            if _v:
                print(' - ', _k, '=', _v)


class Shape(AbstractBrIM):

    def __init__(self, shape_type, id=None, **shape_data):
        super(Shape, self).__init__(id, shape_type, **shape_data)


class ShapePolygon(Shape):

    def __init__(self, *node_list, id=None):
        super(ShapePolygon, self).__init__(id, 'Polygon')
        for i in range(len(node_list)):
            assert isinstance(node_list[i], tuple), "Polygon Corner should be tuple."
            assert len(node_list[i]) == 2, "Polygon Corner has two coordinates."
            self['node_{}'.format(i + 1)] = node_list[i]


class ShapeRectangle(ShapePolygon):

    def __init__(self, width, length, id=None):
        assert isinstance(width, (int, float))
        assert isinstance(length, (int, float))
        super(ShapeRectangle, self).__init__((0, 0), (width, 0), (width, length), (0, length), id=id)


class ShapeCircle(Shape):

    def __init__(self, radius, id=None):
        assert isinstance(radius, (int, float))
        super(ShapeCircle, self).__init__(id, 'Circle', radius=radius)


class Section(AbstractBrIM):

    def __init__(self, *shape, material=None, id=None):
        super(Section, self).__init__(id, 'Section')
        self.link('material', material)
        for i in range(len(shape)):
            self.link('shape{}'.format(i + 1), shape[i])


class FENode(AbstractBrIM):

    def __init__(self, x, y, z, tx=0, ty=0, tz=0, rx=0, ry=0, rz=0, id=None):
        super(FENode, self).__init__(id, 'FENode')
        self['x'] = x
        self['y'] = y
        self['z'] = z
        self['tx'] = tx
        self['ty'] = ty
        self['tz'] = tz
        self['rx'] = rx
        self['ry'] = ry
        self['rz'] = rz


class Group(AbstractBrIM):
    """the purpose of grouping brim elements is to unify particular attribute or api"""

    def __init__(self, group_id, *group_member, **kwargs):
        super(Group, self).__init__(group_id, 'Group', **kwargs)
        self.append(*group_member)

    def unify_attrib(self, key, new_value):
        for m in self:
            m[key] = new_value

    def unify_api(self, api_name, new_api):
        for a in self.api:
            a[api_name] = new_api


class Condition(AbstractBrIM):

    def __init__(self, condition_state=1, *inspection):
        super(Condition, self).__init__(None, 'Condition', condition=condition_state)
        self.append(*inspection)

    def calc_condition_state(self):
        for _insp in self.data.values():
            try:
                self['condition'] = max(_insp['condition'], self['condition'])
            except AttributeError:
                # print('calculating condition state of', self._id)
                pass
            except TypeError:
                # print('calculating condition state of', self._id)
                pass
        return self.condition

    @staticmethod
    def ColorRGB_hex(condition_state, good=9, severe=0):
        """input a condition_state,
        good ~ start = 00FF00
        severe ~ end = FF0000
        interpolation between FF0000 and 00FF00
        :return color representing the condition of element"""
        start = (0, 255, 0)  # 00FF00
        end = (255, 0, 0)  # FF0000
        color = [0, 0, 0]
        for i in range(3):
            itp = start[i] + (end[i] - start[i]) / (severe - good) * (condition_state - good)
            color[i] = hex(int(itp))[2:].zfill(2).upper()
        return "#" + ''.join(color)


if __name__ == '__main__':
    m1 = Material('ccc', a=0.1, fc=30)
    sp1 = ShapePolygon((0, 0), (10, 0), (10, 10), (0, 10))
    rec = ShapeRectangle(12, 8)
    sp2 = ShapeCircle(6)
    sec1 = Section(sp1, material=m1)
    n1 = FENode(0, 0, 0, tz=-1)
    gp = Group('group', m1, sp1, sp2, sec1)
    # print(gp.__dict__)
    print(gp)
    gp.show()
