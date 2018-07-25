#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yidong QIN'

"""
PyMODM is a generic ODM on top of PyMongo, the MongoDB Python driver. 
"""

from pymodm.connection import connect



if __name__ == "__main__":
    print(__author__)
    mongo_str="mongodb://localhost:27017/fours"
    connect(mongo_str,alias='fs')