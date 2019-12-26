# -*- coding: utf-8 -*-
"""
test_yqd.py - YQD tester
Created on May 20 2017
@author: c0redumb
"""

from yahoo_quote_download import yqd, validater


def load_quote(ticker):
    print('===', ticker, '===')
    print(yqd.load_yahoo_quote(ticker, '20181201', '20181231'))
    print(yqd.load_yahoo_quote(ticker, '20181201', '20181231', 'dividend'))
    print(yqd.load_yahoo_quote(ticker, '20181201', '20181231', 'split'))


def test_validate():
    print("Testing validator ...")
    data = ['Date,Open,High,Low,Close,Adj Close,Volume',
            '2020-01-01,100.10,101.20,99.50,100.70,100.70,100000',
            '2020-01-02,105.10,101.20,99.50,100.70,100.70,150000',
            '2020-01-03,100.10,101.20,99.50,200.70,160.70,120000',
            ''
            ]
    print("Original Data:", data)
    print("Validated Data:", validater.validate('TEST', data))


def test():
    # Download quote for stocks
    load_quote('QCOM')
    load_quote('C')

    # Download quote for index
    load_quote('^DJI')

    # Test validating data
    test_validate()


if __name__ == '__main__':
    test()
