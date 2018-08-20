#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
new sensor class in MongoDB instead of MySQL in lab
"""
import matplotlib.pyplot as plt
import numpy as np

from BMS_BrIM.Py_Physical import *


class Sensor(PhysicalELMT):

    def __init__(self, sensor_id, sensor_type='Sensor',
                 x=0, y=0, z=0, direction=None,
                 datapath=None, unit=None, channel=None,
                 *arg, **kwargs):
        super(Sensor, self).__init__(sensor_type, sensor_id)
        self.x, self.y, self.z = x, y, z
        self.direction = direction
        self.datapath = datapath
        self.unit, self.channel = unit, channel
        self.des = arg
        self.check_update_attr(**kwargs)

    def install_at(self, *position):
        if isinstance(position[0], FENode):
            self.x, self.y, self.z = position[0].x, position[0].y, position[0].z
        elif len(position) == 3:
            self.x, self.y, self.z = position
            assert isinstance(self.x, (float, int))
            assert isinstance(self.y, (float, int))
            assert isinstance(self.z, (float, int))


class NetworkUnit(PhysicalELMT):

    def __init__(self, unit_id, experiment_id):
        super(NetworkUnit, self).__init__('UnitClient', unit_id, 'Unit_{}'.format(experiment_id))


class MonitorExperiment(object):

    def __init__(self, ext_id, bridge_id):
        self._id = ext_id
        self.bridge_id = bridge_id


class DatProc(object):
    """Get and process of sensor _data"""

    def __init__(self, title, file_path):
        """Get .dat file in a particular path"""
        self.title = title
        try:
            self.data = np.loadtxt(file_path)
            # print(self.data.shape) # =(6000,)
        except OSError as e:
            print(e)
        plt.figure()
        plt.title(self.title+"and its FFT")

        self.plot()
        self.fourier()
        plt.tight_layout()
        plt.show()

    def plot(self):
        plt.subplot(211)
        plt.plot(self.data)
        plt.xlabel('Sampling Point')
        plt.ylabel('Sensor Data Value')
        plt.title("Sensor Data Plot of "+self.title)

    def fourier(self):
        sp = np.fft.fft(self.data)
        freq = np.fft.fftfreq(self.data.shape[-1])
        plt.subplot(212)
        # plt.plot(sp)
        plt.plot(freq, sp.real, freq, sp.imag)
        plt.xlabel('Frequency')
        plt.ylabel('dB')
        plt.title('FFT of {}'.format(self.title))
        # plt.show()
