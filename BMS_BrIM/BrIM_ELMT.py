#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""

"""
from BMS_BrIM import *

class Beam(BeamDesign, Inspection):

    def __init__(self, beam_id, beam_name):
        # init no so many parameters, put the points and nodes to set_model() methods
        super(BeamDesign, self).__init__('BEAM', beam_id, beam_name)
        self.x1, self.y1, self.z1, self.x2, self.y2, self.z2 = [None] * 6


class Plate(PlateDesign):

    def __init__(self, plate_id):
        super(PhysicalELMT, self).__init__('Plate', plate_id)