#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
This is the base class for all the Interfaces of BMS_BrIM.
As interfaces provide the PyELMT with interoperability with other software,
the interfaces should have dumping/pickling/serialization function to organize data.
"""


class BrIM_interface(object):
    """"""

    def _attr_to_mongo_dict(self):
        return {}

    def update_attr(self, **attributes_dict):
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print('<{}> changed by update_attr()'.format(self))
                    print(' .{} -> {}'.format(_k, _v))
            except KeyError:
                print("<{}> new attribute by update_attr()".format(self))
                print(' .{} -> {}'.format(_k, _v))
            self.__dict__[_k] = _v

    def _attr_pick(self, *pick_list):
        """pick up some of the attributes"""
        _d = dict()
        for _pick in pick_list:
            try:
                _d[_pick] = self.__dict__[_pick]
            except KeyError:
                # print("PyELMT._attr_pick(): No '{}' in {}".format(_pick, self.name))
                pass
        return _d

    def _attr_pop(self, *pop_list):
        """pop attributes out and return the rest."""
        _d = dict()
        for _k, _v in self.__dict__.items():
            if (_k not in pop_list) and _v:
                _d[_k] = _v
        return _d

    def check_attrib(self, type):
        _pick=list()
        for _k, _v in self.__dict__.items():
            if BrIM_interface.check_class(_v, type):
                _pick.append(_k)
        return _pick


    @staticmethod
    def check_class(obj, type):
        if isinstance(obj, type): return True
        return False


"""
def _attr_to_mongo_dict(self: PyELMT):

    def is_unacceptable(one_item):
        _unaccept_type = (PyELMT, PyOpenBrIMElmt)
        if isinstance(one_item, _unaccept_type):
            return True
        return False

    def should_pop(attribute_value):
        if isinstance(attribute_value, (tuple, list)):
            _to_list = list(attribute_value)
            return is_unacceptable(_to_list[0])
        return is_unacceptable(attribute_value)

    def _pop_list(elmt):
        _pop_key = ['db_config', 'openBrIM']
        for _k, _v in elmt.__dict__.items():
            if should_pop(_v):
                _pop_key.append(_k)
        _pop_key=list(set(_pop_key))
        return _pop_key

    _after_pop = _attr_pop(elmt, *_pop_list(elmt))
    return _after_pop
"""

if __name__ == '__main__':
    pass
