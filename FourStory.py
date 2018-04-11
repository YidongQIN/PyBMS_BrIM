#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

from ClassPyOpenBrIM import *
import math

if __name__ == '__main__':
    fourstorey = Project('The 4 Story Model')
    # 1. Materials
    steel = Material('Steel1', mat_type="steel", des="steel of girder")
    steel.mat_property(d="0", E="209", Nu="0.3", a="0.0000065", Fy="50", Fu="65")
    Group('Material Group', steel).attach_to(fourstorey)

    # 2. Sections
    # 2.0 sec_par
    height = PrmElmt('Height', 300.0, des='Vertical space between two storey')
    t_deck = PrmElmt('Thick_deck', 13, 'Thickness of each deck')
    l_deck = PrmElmt('Length_deck', 405.0, 'Length of each deck')
    w_deck = PrmElmt('Width_deck', 303.0, 'Width of each deck')
    t_colm = PrmElmt('Thick_column', 1.0, 'Thickness of each column')
    w_colm = PrmElmt('Width_column', 25.0, 'Width of each column')
    '''''
            i1      i2      i3      i4      i5
    L4L:    3.15    3.25    7.58    2.27    3.50
    L4R:    3.87    2.24    7.75    2.79    3.70
    L3L:    3.45    2.86    7.61    2.48    3.18
    L3R:    3.90    2.40    7.60    2.70    3.72
    '''
    in_1 =PrmElmt('Interval_1', 35.6, 'interval from edge to the first column')
    in_2 =PrmElmt('Interval_2', 26.2, 'interval from the first column to the second column')
    in_3 =PrmElmt('Interval_3', 76.4, 'interval from the first column to the second column')

    # 2.1 deck
    # 2.2 column
    # 2.3 nut
    # 2.4 track

    # 3. FE elements
    # 4. Loading Conditions
    # 5. Geometric model

    ShowTree(fourstorey)
    fourstorey.save_project()
