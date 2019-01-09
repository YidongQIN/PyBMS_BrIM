#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""

import datetime as dt

import matplotlib.pyplot as plt
import numpy as np

from BrIMcollection import *


class CADDrawing(DocumentBrIM):

    def __init__(self, cad_file_path, id=None):
        self.check_file_type(cad_file_path, 'dwg')
        super(CADDrawing, self).__init__(id, 'CAD', cad_file_path)


class Media(DocumentBrIM):

    def __init__(self, file_path, id=None):
        self.check_file_type(file_path, '.jpg')
        super(Media, self).__init__(id, 'Media', file_path)


class BridgeProject(DocumentBrIM):

    def __init__(self, name, latitude, longitude, length, structural_type, file_path):
        super(BridgeProject, self).__init__(name, 'BridgeProject', file_path)
        # self._id=0 # relationship of bridgeid and ObjectId(=_id) in MongoDB?
        self.latitude, self.longitude = latitude, longitude
        self.length = length
        self.structural_type = structural_type
        if self.structural_type not in ['girder', 'arch', 'cable-stay', 'suspension']:
            print('#Special bridge structural type')


class MonitorExperiment(DocumentBrIM):

    def __init__(self, ext_id, bridge, start_datetime, end_datetime, des=None):
        _name = 'Experiment_{}'.format(bridge)
        self.bridge = bridge
        self.start = dt.datetime(*self._format_datetime(start_datetime))
        self.end = dt.datetime(*self._format_datetime(end_datetime))
        super(MonitorExperiment, self).__init__(_name, ext_id, des)

    @property
    def experiment_period(self):
        print("Monitor Experiment <{}>".format(self.name))
        print(" * Start: {}".format(self.start))
        print(" * until: {}".format(self.end))
        return self.end - self.start

    @staticmethod
    def _format_datetime(datetime):
        """process of DateTime int transferred to to a list of dt objects,
        such as 201801010203 (AM 2:03, Jan 1st, 2018) to 2018,01,01,02,03.
        :returns:
        (_year, _month, _day, _hour, _minute)
        """
        _dt = str(datetime)
        assert len(_dt) == 12
        return list(map(int, [_dt[0:4], _dt[4:6], _dt[6:8], _dt[8:10], _dt[10:12]]))


class SensorData(DocumentBrIM):

    def __init__(self, data_path, id=None):
        self.check_file_type(data_path, 'dat')
        super(SensorData, self).__init__(id, 'Data', data_path)
        try:
            self.sensordata = np.loadtxt(data_path)
        except OSError as e:
            print(e)
        plt.figure()
        plt.title(self._id + "and its FFT")
        self.plot()
        self.fourier()
        plt.tight_layout()
        plt.show()

    def plot(self):
        plt.subplot(211)
        plt.plot(self.sensordata)
        plt.xlabel('Sampling Point')
        plt.ylabel('Sensor Data Value')
        plt.title("Sensor Data Plot of " + self._id)

    def fourier(self):
        sp = np.fft.fft(self.sensordata)
        freq = np.fft.fftfreq(self.sensordata.shape[-1])
        plt.subplot(212)
        plt.plot(freq, sp.real, freq, sp.imag)
        plt.xlabel('Frequency')
        plt.ylabel('dB')
        plt.title('FFT of {}'.format(self._id))


if __name__ == '__main__':
    media1 = Media('c:\\Users\\yqin78\\Downloads\\xxx.md', 8)
    print(media1)
