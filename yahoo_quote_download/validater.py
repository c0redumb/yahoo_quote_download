# -*- coding: utf-8 -*-
"""
validate.py - Trivial data validater
Created on December 24, 2019
@author: c0redumb
"""

# To make print working for Python2/3
from __future__ import print_function


def validate(ticker, data, begindate='1920-01-01', verbose=0):
    '''
    This function perform a query and extract the matching cookie and crumb.
    '''
    new_data = []
    last_date = None
    for line in data:
        # Filename lines, usually the first line
        # Zero length lines, usually the last line
        if len(line) == 0 or line.startswith('Date'):
            new_data.append(line)
            continue

        # Extract all the fields
        try:
            field = line.split(',')
            d = field[0]
            o = float(field[1])
            h = float(field[2])
            l = float(field[3])
            c = float(field[4])
            adj_c = float(field[5])
        except:
            #print("Failed to parse:", line)
            continue

        # This is a wierd quirk we need to check
        invalid_date = False
        if last_date is None:
            if d < begindate:
                invalid_date = True
            last_date = d
        else:
            if d <= last_date:
                invalid_date = True
            else:
                last_date = d
        if invalid_date:
            if verbose > 0:
                print("!!! {}: Invalid date {} in data".format(
                    ticker, field[0]))
                continue

        # Verify that the open/close is within the high/low range
        mid = (h + l) / 2
        corrected = False
        if o > h * 1.0001 or o < l * 0.9999:
            o = mid
            corrected = True
            if verbose > 0:
                print("!!! {}: Open is out of range on {}".format(
                    ticker, field[0]))

        if c > h * 1.0001 or c < l * 0.9999:
            if c != 0.0:
                adj_c *= mid / c
            else:
                adj_c = mid
            c = mid
            corrected = True
            if verbose > 0:
                print("!!! {}: Close is out of range on {}".format(
                    ticker, field[0]))

        if corrected:
            if verbose > 5:
                print(line)
            line = "{},{},{},{},{},{},{}".format(
                field[0], o, h, l, c, adj_c, field[6])
            if verbose > 5:
                print(line)
        new_data.append(line)

    return new_data
