# -*- coding: utf-8 -*-
"""
yqd.py - Yahoo Quote Downloader
Created on May 18 2017
@author: c0redumb
"""

# To make print working for Python2/3
from __future__ import print_function

# Use six to import urllib so it is working for Python2/3
from six.moves import urllib
# If you don't want to use six, please comment out the line above
# and use the line below instead (for Python3 only).
#import urllib.request, urllib.parse, urllib.error

import time
import gzip
import io

'''
Starting on May 2017, Yahoo financial has terminated its service on
the well used EOD data download without warning. This is confirmed
by Yahoo employee in forum posts.

Yahoo financial EOD data, however, still works on Yahoo financial pages.
These download links uses a "crumb" for authentication with a cookie "B".
This code is provided to obtain such matching cookie and crumb.
'''

# Build the cookie handler
import http.cookiejar
cj = http.cookiejar.CookieJar()
cookier = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(cookier)
urllib.request.install_opener(opener)

# Cookie and corresponding crumb
_cookie = None
_crumb = None

# Headers to fake a user agent
_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


import json
from datetime import datetime

def _get_cookie_crumb():
    '''
    This function is now a placeholder as the v8 API currently does not require crumbs.
    '''
    global _cookie, _crumb
    _cookie = 'ready'
    _crumb = 'not_needed'


def load_yahoo_quote(ticker, begindate, enddate, info='quote'):
    '''
    This function load the corresponding history/divident/split from Yahoo using v8 API.
    The "begindate" and "enddate" are in the format of YYYYMMDD.
    The "info" can be "quote" for price, "dividend" for dividend events,
    or "split" for split events.
    '''
    # Prepare the parameters and the URL
    tb = time.mktime((int(begindate[0:4]), int(
        begindate[4:6]), int(begindate[6:8]), 4, 0, 0, 0, 0, 0))
    te = time.mktime((int(enddate[0:4]), int(
        enddate[4:6]), int(enddate[6:8]), 18, 0, 0, 0, 0, 0))

    param = dict()
    param['period1'] = int(tb)
    param['period2'] = int(te)
    param['interval'] = '1d'
    param['includeAdjustedClose'] = 'true'
    
    # Always get all events to be sure
    param['events'] = 'div|split'
    
    params = urllib.parse.urlencode(param)
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?{}'.format(
        ticker, params)
    
    req = urllib.request.Request(url, headers=_headers)

    # Perform the query
    try:
        f = urllib.request.urlopen(req, timeout=10)
        data = f.read()
        if f.info().get('Content-Encoding') == 'gzip' or data.startswith(b'\x1f\x8b'):
            data = gzip.decompress(data)
        out = json.loads(data.decode('utf-8'))
    except Exception as e:
        # print("Error fetching data:", e)
        return []

    # Parse JSON and format as CSV-like list of strings
    res = out.get('chart', {}).get('result', [])
    if not res:
        return []
    
    result = res[0]
    timestamps = result.get('timestamp', [])
    indicators = result.get('indicators', {})
    quote = indicators.get('quote', [{}])[0]
    adjclose = indicators.get('adjclose', [{}])[0].get('adjclose', [])
    events = result.get('events', {})

    lines = []
    if info == 'quote':
        lines.append('Date,Open,High,Low,Close,Adj Close,Volume')
        for i in range(len(timestamps)):
            dt = datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d')
            line = '{},{},{},{},{},{},{}'.format(
                dt,
                quote.get('open', [None]*len(timestamps))[i],
                quote.get('high', [None]*len(timestamps))[i],
                quote.get('low', [None]*len(timestamps))[i],
                quote.get('close', [None]*len(timestamps))[i],
                adjclose[i] if i < len(adjclose) else '',
                quote.get('volume', [None]*len(timestamps))[i]
            )
            lines.append(line)
    elif info == 'dividend':
        lines.append('Date,Dividends')
        divs = events.get('dividends', {})
        # Sort dividends by date
        for ts in sorted(divs.keys()):
            dt = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')
            lines.append('{},{}'.format(dt, divs[ts].get('amount')))
    elif info == 'split':
        lines.append('Date,Stock Splits')
        splits = events.get('splits', {})
        for ts in sorted(splits.keys()):
            dt = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d')
            lines.append('{},{}'.format(dt, splits[ts].get('splitRatio')))
    
    return lines
