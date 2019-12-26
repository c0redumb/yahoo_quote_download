# -*- coding: utf-8 -*-
"""
downloader.py - Commandline downloader
Created on December 25, 2019
@author: c0redumb
"""

import os
import traceback
from optparse import OptionParser

from yahoo_quote_download import yqd, validater


def main():
    # parse arguments
    parser = OptionParser()
    parser.add_option("-t", "--ticker", dest="ticker", action="store",
                      help="The ticker")
    parser.add_option("-b", "--begindate", dest="begindate", action="store",
                      help="The beginning date (YYYY-MM-DD)")
    parser.add_option("-e", "--enddate", dest="enddate", action="store",
                      help="The end date (YYYY-MM-DD)")
    parser.add_option("-f", "--datafile", dest="datafile", action="store",
                      help="The destination data file")
    global options
    (options, args) = parser.parse_args()

    print("     Ticker:", options.ticker)
    print("  Beginning:", options.begindate)
    print("     Ending:", options.enddate)
    print("       File:", options.datafile)

    try:
        data = yqd.load_yahoo_quote(options.ticker,
                                    options.begindate.replace('-', ""),
                                    options.enddate.replace('-', ''))
        vdata = validater.validate(options.ticker, data)
        with open(options.datafile, "w") as f:
            for line in vdata:
                f.write(line)
                f.write('\n')
    except:
        traceback.print_exc()


if __name__ == '__main__':
    main()
