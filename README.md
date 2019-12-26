# yahoo_quote_download

## Introduction
This project is for downloading Yahoo financial EOD (End-of-Day) data of stock and market indexes.

## Background
Yahoo has provided the EOD financial data service for a long time and it has been well-used. However, starting on May 2017, Yahoo financial has terminated that service without warning. This is confirmed by a Yahoo employee in forum posts.

However, it is later found that despite that the service has been terminated, the Yahoo financial EOD data is still available, though with some authentication steps added and some changes in format. The [technical details](https://github.com/c0redumb/yahoo_quote_download/blob/master/details.md) are described in a separate document.

This project provides a way to continue obtaining the same data.

## Installation
This is a Python project. So Python should be installed first. This project works with either Python2 or Python3.

To install this project On Windows / Linux, you may simply do
<pre><code>
pip install yahoo_quote_download
</code></pre>

## Data Download
The main entry point is a commandline application. To download EOD data for a ticker, please try
<pre><code>
yqdownload [-t ticker] [-s startdate] [-e enddate] [-f datafile]
</code></pre>
where
* ticker - the ticker to quote, e.g., MSFT (Microsoft) or ^DJI (Dow Jones Industrial index). Please check Yahoo financial webpage for the tickers they use.
* startdate/enddate - the starting and ending date of the download. It is in the format of YYYY-MM-DD.
* datafile - the file where the downloaded data is saved to. If the file exists, the existing content will be overwritten.
As usual, you may use -h or --help options to see all the supported options.

Note: This sample commandline application is provided for illustration purposes. Please do not overuse or abuse the data provided by Yahoo. Losing that would be a lost to all of us. I will put together an incremental downloader when I have more time.

## License
This code in this project is available through "Simplified BSD License".