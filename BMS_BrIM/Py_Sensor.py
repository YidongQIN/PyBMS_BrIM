#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
new sensor class in MongoDB instead of MySQL in lab
"""

import datetime as dt

import matplotlib.pyplot as plt
import numpy as np

from BMS_BrIM.Py_Physical import *


class MonitorExperiment(Document):

    def __init__(self, ext_id, bridge, start_datetime, end_datetime, des=None):
        _name = 'Experiment_{}'.format(bridge)
        self.bridge = bridge
        self.start = dt.datetime(*self._prc_dt(start_datetime))
        self.end = dt.datetime(*self._prc_dt(end_datetime))
        super(MonitorExperiment, self).__init__(_name, ext_id, des)

    @property
    def experiment_period(self):
        print("Monitor Experiment <{}>".format(self.name))
        print(" * Start: {}".format(self.start))
        print(" * until: {}".format(self.end))
        return self.end - self.start

    @staticmethod
    def _prc_dt(datetime):
        """process of DateTime int transferred to to a list of dt objects,
        such as 201801010203 (AM 2:03, Jan 1st, 2018) to 2018,01,01,02,03.
        :returns:
        (_year, _month, _day, _hour, _minute)
        """
        _dt = str(datetime)
        assert len(_dt) == 12
        return list(map(int, [_dt[0:4], _dt[4:6], _dt[6:8], _dt[8:10], _dt[10:12]]))


class NetworkUnit(PhysicalELMT):

    def __init__(self, unit_id, *channel, experiment=None):
        super(NetworkUnit, self).__init__('NetworkUnit', unit_id)
        self.channel: list = channel
        self.experiment, self.experiment_id = self.experiment_install(experiment)

    def experiment_install(self, experiment: MonitorExperiment):
        try:
            self.experiment = experiment
            self.experiment_id = experiment._id
            return experiment, experiment._id
        except AttributeError as e:
            print("Error in NetworkUnit.experiment_install()")
            print(e)

    def channel_install(self, **channel_sensor):
        self.channel_sensor: dict
        for _c, _s in channel_sensor.items():
            assert isinstance(_c, str) and isinstance(_s, Sensor), TypeError
            if _c not in self.channel:
                print("! New channel <{}> added to {}".format(_c, self.name))
            self.channel_sensor[_c] = _s._id


class Sensor(PhysicalELMT):

    def __init__(self, sensor_id, sensor_type='Sensor',
                 x=0, y=0, z=0, direction=None,
                 unit: NetworkUnit = None, channel: str = None,
                 manufacture_model=None,
                 datapath: str = None, *arg, **kwargs):
        super(Sensor, self).__init__(sensor_type, sensor_id)
        self.x, self.y, self.z = x, y, z
        self.direction = direction
        self.unit, self.channel = self.unit_install(unit, channel)
        self.manufactureModel = manufacture_model
        self.datapath = datapath
        self.des = arg
        self.update_attr(**kwargs)

    def install_at(self, *position):
        if len(position) == 1 and isinstance(position[0], FENode):
            self.x, self.y, self.z = position[0].x, position[0].y, position[0].z
        elif len(position) == 3:
            self.x, self.y, self.z = position
            assert isinstance(self.x, (float, int))
            assert isinstance(self.y, (float, int))
            assert isinstance(self.z, (float, int))

    def unit_install(self, unit: NetworkUnit, channel: str):
        if channel in unit.channel:
            print("Channel exists")
        else:
            print("No channel, should define the channel first.")
        self.unit, self.channel = unit, channel
        return unit, channel


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
        plt.title(self.title + "and its FFT")

        self.plot()
        self.fourier()
        plt.tight_layout()
        plt.show()

    def plot(self):
        plt.subplot(211)
        plt.plot(self.data)
        plt.xlabel('Sampling Point')
        plt.ylabel('Sensor Data Value')
        plt.title("Sensor Data Plot of " + self.title)

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
