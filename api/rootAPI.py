#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
import json

import api.openbrim as ob


class BrimAPI(object):

    def __init__(self, brim_data, config):
        """init is config"""
        self._check_dict(brim_data)
        self.info = self._mapping(brim_data, self.map)
        self._check_dict(config)
        self.interface = self._connect(config)

    def _check_dict(self, data_dict):
        """check the configs. SHOULD be override"""
        assert isinstance(data_dict, dict)
        return data_dict

    def _connect(self, config):
        """return interface. SHOULD be override"""
        pass

    @property
    def map(self):
        """{origin_key: new_key}. For eET, like {'name':'N'}"""
        return self._map

    @property
    def map_inverse(self):
        return {v: k for k, v in self._map.items()}

    @map.setter
    def map(self, map_dict):
        """args check is in concrete class. """
        # for _k, _v in map_dict:
        #     pass
        self._map = map_dict

    @staticmethod
    def _mapping(data_dict, directed_map):
        """map the data_dict.keys to required keys."""
        _info = dict()
        for _k, _v in data_dict.items():
            try:
                _new_key = directed_map[_k]
                _info[_new_key] = _v
            except KeyError as e:
                # greed or?
                # _info[_k]=_v
                print('Missing attriubte mapping', e)
        return _info

    def _process(self):
        """the api will do sth, dumps or loads"""
        pass

    def dumps(self):
        self._mapping(self.info, self.map)

    def save_file(self, file_path='file'):
        """dump the api info into json"""
        if not file_path:
            file_path = '{}.data'.format(self)
        _j = json.dumps(self.info, indent=2)
        with open(file_path, 'w') as _f:
            _f.write(_j)


class openbrim_api(BrimAPI):

    def __init__(self, brim_data):
        """to connect OpenBrIM"""
        self.map = {'name': 'N', 'type': 'T'}
        #@TODO change the type? need ad map of BrIMcollection.type -> ParamML.type
        super(openbrim_api, self).__init__(brim_data, config=None)

    def _connect(self, config):
        super(openbrim_api, self)._connect(config)
        return ob.ParamMLelmt('O', self.info['name'], **self.info).elmt


if __name__ == '__main__':
    print("This is {}, which has ".format(__file__))
    print(dir())


"""
dir in PyBrIM:
- 'Abstract', 
- 'AbstractBrIM', 
- 'Accelerometer', 
- 'Beam', 
- 'BridgeProject', 
- 'CADDrawing', 
- 'CoatingDamage', 
- 'Condition', 
- 'Corrosion', 
- 'Deformation', 
- 'Displacemeter', 
- 'DocumentBrIM', 
- 'EquipmentBrIM', 
- 'FENode', 
- 'Group', 
- 'InspectionRecord', 
- 'Loose', 
- 'Material', 
- 'Media', 
- 'MonitorExperiment', 
- 'NetworkUnit', 
- 'Parameter', 
- 'PhysicalBrIM', 
- 'PyBrIM', 
- 'Section', 
- 'Sensor', 
- 'SensorData', 
- 'Shape', 
- 'ShapeCircle', 
- 'ShapePolygon', 
- 'ShapeRectangle', 
- 'StrainGauge', 
- 'Surface', 
- 'TemperatureSensor', 

dir in ParamML:
- 'BoltedPlateGeo', 
- 'CubeGeo', 
- 'LineCubeOB', 
- 'OBCircle', 
- 'OBExtends', 
- 'OBFELine', 
- 'OBFENode', 
- 'OBFESurface', 
- 'OBGroup', 
- 'OBLine', 
- 'OBMaterial', 
- 'OBPoint', 
- 'OBProject', 
- 'OBSection', 
- 'OBShape', 
- 'OBSurface', 
- 'OBText3D', 
- 'OBUnit', 
- 'OBVolume', 
- 'Oelmt', 
- 'ParamMLelmt', 
- 'Pelmt', 
- 'PlateFEM', 
- 'PolygonOBShape', 
- 'RectangleOBShape', 
- 'ShowTable', 
- 'ShowTree', 
- 'StraightBeamFEM', 
- 'StraightBeamGeo', 

"""