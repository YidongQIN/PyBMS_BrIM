#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
This is the base class for all the Interfaces of BMS_BrIM.
As interfaces provide the PyELMT with interoperability with other software,
the interfaces should have dumping/pickling/serialization function to organize data.
"""
import json


class BrIMInterface(object):
    """Basic class for all interfaces."""

    # 1. I/O function
    def input(self, source, data_format):
        """read a file or a string."""

        def input_file(file_path):
            with open(file_path, 'r') as f:
                return f.read()

        def input_json(json_str):
            _d = json.loads(json_str)
            return _d

        def input_xml(xmi_str):
            print("BrIM_Interface.input_xml() undone")
            return xmi_str

        if data_format == "file":
            self.loads(input_file(source))
        elif data_format == "json":
            self.loads(input_json(source))
        elif data_format == "xml":
            self.loads(input_xml(source))
        else:
            print("Unknown Data format")

    def output(self, file_path):
            """write the attributes into JSON"""
            _j = json.dumps(self.__dict__, indent=2)
            if not file_path:
                file_path = "{}.json".format(self.name)
            with open(file_path, 'w') as _f:
                _f.write(_j)
            print("<{}> data stored in {}".format(self.name, file_path))


    def dumps(self):
        """dump self.__dict__ to str"""
        pass

    def loads(self, data):
        """load other data format to dict"""
        pass

    def update(self, **attributes_dict):
        """update self.__dict__ with new attributes"""
        for _k, _v in attributes_dict.items():
            try:
                if not _v == self.__dict__[_k]:
                    print('<{}> changed by update()'.format(self))
                    print(' .{} -> {}'.format(_k, _v))
            except KeyError:
                print("<{}> new attribute by update()".format(self))
                print(' .{} -> {}'.format(_k, _v))
            self.__dict__[_k] = _v

    def attr_pick(self, *pick_list):
        """pick up some of the attributes"""
        _d = dict()
        for _pick in pick_list:
            try:
                _d[_pick] = self.__dict__[_pick]
            except KeyError:
                print("attr_pick(): No '{}'".format(_pick))
        return _d

    def attr_pop(self, *pop_list):
        """pop attributes out and return the rest."""
        _d = dict()
        for _k, _v in self.__dict__.items():
            if (_k not in pop_list) and _v:
                _d[_k] = _v
        return _d

    def check_attrib(self, type):
        _pick = list()
        for _k, _v in self.__dict__.items():
            if self.check_class(_v, type):
                _pick.append(_k)
        return _pick

    def check_class(self, obj, type):
        if isinstance(obj, type):
            return True
        print(" # interface.check_class()", obj, "not type of", type)
        return False




if __name__ == '__main__':
    pass
