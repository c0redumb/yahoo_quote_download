# -*- coding: utf-8 -*-
"""
downloader.py - Commandline downloader
Created on December 25, 2019
@author: c0redumb
"""

import os
import time
import datetime
import traceback
import argparse

from yahoo_quote_download import yqd, validater, __version__


def main():
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Yahoo Quote Downloader v' + __version__)
    parser.add_argument("-t", "--ticker", dest="ticker",
                        required=True, help="The ticker")
    parser.add_argument("-b", "--begindate", dest="begindate",
                        help="The beginning date (YYYY-MM-DD)")
    parser.add_argument("-e", "--enddate", dest="enddate",
                        help="The end date (YYYY-MM-DD)")
    parser.add_argument("-f", "--datafile", dest="datafile",
                        required=True, help="The destination data file")
    parser.add_argument("-m", "--max-retry", dest="maxretries", default=5, type=int,
                        help="The maximum number of retries")
    parser.add_argument("-v", "--verbose", dest="verbose", default=1, type=int,
                        help="Verbose level")
    args = parser.parse_args()

    if args.verbose > 0:
        print("Downloading {} ...".format(args.ticker))

    # Increment mode (only download the necessary data after what is already in the datafile)
    # Increment mode is only used when
    #       - A last date can be extracted from the datafile AND
    #       - A beginning date is not specified in the commandline
    increment_mode = False
    data_in_file = []
    today = datetime.datetime.today()
    today_str = today.strftime('%Y-%m-%d')

    # Determine the starting date if it is not provided
    # If it can be extracted from the last line of the data file, then we use the next day
    # Otherwise we use a standard starting date 1970-01-01
    if args.begindate is None:
        # Try to extract the last day in the data file
        if os.path.exists(args.datafile):
            with open(args.datafile) as df:
                # Read all the lines that is currently in datafile
                for cnt, line in enumerate(df):
                    if len(line) >= 10:  # At least has a date
                        data_in_file.append(line)
                # Extract the last date
                try:
                    # Extract the first day date (in case we need to redownload the whole thing)
                    firstline = data_in_file[1]
                    firstday_str = firstline.split(',')[0].strip()
                    firstday = datetime.datetime.strptime(
                        firstday_str, '%Y-%m-%d')
                    # Extract the last day date (for increment mode)
                    lastline = data_in_file[-1]
                    lastday_str = lastline.split(',')[0].strip()
                    lastday = datetime.datetime.strptime(
                        lastday_str, '%Y-%m-%d')
                    if lastday_str >= today_str:
                        if args.verbose > 0:
                            print('{}: datafile ({}) is update to today {}'.format(
                                args.ticker, lastday_str, today_str))
                            print('Nothing to download')
                        return
                    nextday = lastday + datetime.timedelta(days=1)
                    nextday_str = nextday.strftime('%Y-%m-%d')
                    if args.verbose > 5:
                        print('Last Date:', lastday_str,
                              ', Next Day:', nextday_str,
                              ', First Day:', firstday_str)
                    args.begindate = nextday_str
                    # All good, and set the increment mode
                    increment_mode = True
                except:
                    if args.verbose > 0:
                        print('!!! {}: failed to extract last date from date file'.format(
                            args.ticker))
                    data_in_file = []
    if args.begindate is None:
        # Two cases we are here:
        #   1. The datafile does not exist yet, or
        #   2. The datefile exists, but we failed to extract the last date
        args.begindate = '1970-01-01'

    # Determine the end date if it is not provided
    # It will be default to today's date
    if args.enddate is None:
        args.enddate = today_str

    # Print the parameters
    if args.verbose > 1:
        print("     Ticker:", args.ticker)
        print("  Beginning:", args.begindate)
        print("     Ending:", args.enddate)
        print("       File:", args.datafile)

    success = False
    for itry in range(args.maxretries):
        try:
            # Do a download of split and divident first in increment mode.
            # If such events exist, the scale will be adjusted for the entire sequence.
            # In those cases, we will need to redownload from the very beginning.
            if increment_mode:
                div_data = yqd.load_yahoo_quote(args.ticker,
                                                args.begindate.replace(
                                                    '-', ""),
                                                args.enddate.replace('-', ''),
                                                info='dividend')
                has_div_event = (len(div_data) > 2 and len(div_data[-1]) > 10)
                split_data = yqd.load_yahoo_quote(args.ticker,
                                                  args.begindate.replace(
                                                      '-', ""),
                                                  args.enddate.replace(
                                                      '-', ''),
                                                  info='split')
                has_split_event = (
                    len(split_data) > 2 and len(split_data[-1]) > 10)
                if has_div_event or has_split_event:
                    print('!!! {}: Has a recent event (dividend or split)')
                    args.begindate = firstday
                    increment_mode = False

            # Finally download the data
            data = yqd.load_yahoo_quote(args.ticker,
                                        args.begindate.replace('-', ""),
                                        args.enddate.replace('-', ''))
            success = True
            break
        except:
            if args.verbose > 2:
                print("Try {}/{} failed".format(itry + 1, args.maxretries))
            # traceback.print_exc()

            # Download failed. Will retry in 2 seconds, until maxretries is reached,
            # Setting _crumb to None will force yqd to obtain a new set of cookies.
            # This solves the intermittent "401 Unauthorized" issue.
            yqd._crumb = None
            time.sleep(2)

    if success:
        if args.verbose > 0:
            print("Data download successful")
        #print("Dump", data)
        vdata = validater.validate(
            args.ticker, data, begindate=args.begindate, verbose=args.verbose)
        with open(args.datafile, "w") as f:
            if increment_mode:
                # Write back the original data in file
                for line in data_in_file:
                    f.write(line)
                # Remove the field headline for the newly downloaded data
                del vdata[0]
            for line in vdata:
                # Skip lines that are empty
                if len(line) == 0:
                    continue
                f.write(line)
                f.write('\n')
    else:
        print("!!! {}: Download unsuccessful!".format(args.ticker))


if __name__ == '__main__':
    main()
