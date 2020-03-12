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
yqdownload -t ticker -f datafile [-b begindate] [-e enddate] [-m maxretries] [-v verbose] [-h]
</code></pre>
where
* ticker - (Required) the ticker to download, e.g., MSFT (Microsoft) or ^DJI (Dow Jones Industrial index). Please check Yahoo financial webpage for the tickers they use.
* datafile - (Required) the file where the downloaded data is saved to.
* begindate - (Optional) the beginning date of the download in the format of YYYY-MM-DD. If not provided, the data will be incrementally downloaded based on the data in the data file. If all fails, the default is 1970-01-01.
* enddate - (Optional) the ending date of the download in the format of YYYY-MM-DD. If not provided, the default is the current day.
* maxretries - (Optional) max number of retries. Occationally, the download will reach an error. This is the maximum number of retries in such cases. The default is 5.
* verbose - (Optional) verbose level. The default is 1. You may use 0 to make it really quiet.
* As usual, you may use -h or --help options to see all the supported options.

## License
This code in this project is available through "Simplified BSD License".
