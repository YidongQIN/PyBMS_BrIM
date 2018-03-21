#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
use ClassPyOpenBrIM to generate the xml file of MARC Bridge.
"""

from ClassPyOpenBrIM import *

if __name__ == '__main__':
    marc=PyOpenBrIMElmt('MARC_OOP')
    # Units are in default template of new_project
    marc.new_project()

    # 1. Material


    # 2. Sections


    # 3. Structural Parameter


    # 4. Points


    # 5. Lines


    # 6. Surfaces



    # 7. Save and Show
    ShowTree(marc)
    marc.save_project()


