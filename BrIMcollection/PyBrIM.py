#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
import collections
import json
import os


class PyBrIM(collections.UserDict):

    def __init__(self, brim_id, brim_type, **brim_data):
        """id is the name"""
        self._id = brim_id
        self.type = brim_type
        super(PyBrIM, self).__init__(**brim_data)
        self.api = dict()

    def link(self, key: str, element):
        if isinstance(element, PyBrIM):
            self.__setitem__(key, element._id)
        elif isinstance(element, (str, float, int)):
            self.__setitem__(key, element)

    def __str__(self):
        return "#{}_{}~{}".format(self.type, self._id,
                                  super(PyBrIM, self).__str__())

    def jsondumps(self):
        return json.dumps(self, indent=4, default=lambda obj: obj.__dict__)

    def __iter__(self):
        return iter(self.data.items())

    # attributes can be used for getting information, but not recommended
    def __setattr__(self, key, value):
        if key in ('_id', 'type', 'data', 'api'):
            # print('set default attr', key)
            super(PyBrIM, self).__setattr__(key, value)
        elif key in self.data.keys():
            print('set attr in .data items', key)
            super(PyBrIM, self).__setitem__(key, value)
        elif key in self.api.keys():
            print('@TODO set application interface', key)
            # super(PyBrIM, self).__setitem__(key, value)
            # @TODO
            return
        else:
            print("New attribute:", key, "=", value)
            super(PyBrIM, self).__setitem__(key, value)

    def __getattr__(self, item):
        try:
            return self.data[item]
        except KeyError:
            print("No attribute found:", item)
            return

    def __delattr__(self, item):
        try:
            super(PyBrIM, self).__delattr__(item)
        except AttributeError:
            try:
                super(PyBrIM, self).__delitem__(item)
            except KeyError:
                print('Cannot find attribute to del:', item)

    # api are interfaces for other software
    def setter_api(self):
        """decorator for api.setter(): self.data -> other model"""
        pass

    def getter_api(self):
        """decorator for api.getter(): other model -> self.data"""
        pass


class DocumentBrIM(PyBrIM):

    def __init__(self, brim_id, brim_type, file_path, **brim_data):
        if not os.path.isfile(file_path):
            print('<<', file_path, ">> file not found")
            # raise FileNotFoundError
        super(DocumentBrIM, self).__init__(brim_id, brim_type,
                                           **brim_data, file=file_path)

    @staticmethod
    def check_file_type(file, *extension):
        """check if the file's extension == the given ext"""
        ext = os.path.splitext(file)[-1].lower()
        # print(extension)
        # print(ext)
        if ext in extension:
            return True
        elif ext[1:] in extension:
            return True
        else:
            print('The extension', ext, 'is not in', extension)
            return False


class EquipmentBrIM(PyBrIM):

    def __init__(self, brim_id, brim_type, **brim_data):
        super(EquipmentBrIM, self).__init__(brim_id, brim_type, **brim_data)
        self.api['OpenBrIM_GEO'] = None


class AbstractBrIM(PyBrIM):

    def __init__(self, brim_id, brim_type, **brim_data):
        super(AbstractBrIM, self).__init__(brim_id, brim_type, **brim_data)
        self.api['OpenBrIM_FEM'] = None


class PhysicalBrIM(PyBrIM):

    def __init__(self, brim_id, brim_type, material=None, **brim_data):
        super(PhysicalBrIM, self).__init__(brim_id, brim_type, **brim_data)
        self.api['OpenBrIM_FEM'] = None
        self.api['OpenBrIM_GEO'] = None
        self.set_material(material)

    def set_material(self, material):
        if material:
            assert isinstance(material, AbstractBrIM)
            self.link('material', material)


if __name__ == '__main__':
    mongo_4 = 'c:\\Users\\yqin78\\Proj.Python\\PyBMS_BrIM\\_data\\mongo_fourstory.txt'
    doc = DocumentBrIM(3, 'ext', "adfasdf", read='Unread')
    print(doc)
    doc.api['ob'] = 'Doc_No_OB'
    print(doc.__dict__)
