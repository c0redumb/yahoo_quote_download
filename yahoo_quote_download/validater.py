# -*- coding: utf-8 -*-
"""
validate.py - Trivial data validater
Created on December 24, 2019
@author: c0redumb
"""

# To make print working for Python2/3
from __future__ import print_function


def validate(ticker, data):
    '''
    This function perform a query and extract the matching cookie and crumb.
    '''
    new_data = []
    for line in data:
        # Filename lines, usually the first line
        # Zero length lines, usually the last line
        if len(line) == 0 or line.startswith('Date'):
            new_data.append(line)
            continue

        # Extract all the fields
        field = line.split(',')
        o = float(field[1])
        h = float(field[2])
        l = float(field[3])
        c = float(field[4])
        adj_c = float(field[5])

        # Verify that the open/close is within the high/low range
        corrected = False
        if o > h:
            o = h
            corrected = True
            print("!!! {}: Open is out of range on {}".format(
                ticker, field[0]))
        elif o < l:
            o = l
            corrected = True
            print("!!! {}: Open is out of range on {}".format(
                ticker, field[0]))

        if c > h:
            adj_c *= h / c
            c = h
            corrected = True
            print("!!! {}: Close is out of range on {}".format(
                ticker, field[0]))
        elif c < l:
            adj_c *= l / c
            c = l
            corrected = True
            print("!!! {}: Close is out of range on {}".format(
                ticker, field[0]))

        if corrected:
            # print(line)
            line = "{},{},{},{},{},{},{}".format(
                field[0], o, h, l, c, adj_c, field[6])
            # print(line)
        new_data.append(line)

    return new_data
