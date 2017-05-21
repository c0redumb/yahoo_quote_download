# yahoo_quote_download

Starting on May 2017, Yahoo financial has terminated its service on the well used EOD data download without warning. This is confirmed by Yahoo employee in forum posts.

Yahoo financial EOD data, however, still works on Yahoo financial pages. These download links uses a "crumb" for authentication with a cookie "B". This code is provided to obtain such matching cookie and crumb. This code also downloads end of day stock quote from Yahoo finance.

Once the cookie/crumb is obtained, the querying URL is as following:

```
https://query1.finance.yahoo.com/v7/finance/download/TTTT?period1=pppppppp&period2=qqqqqqqq&interval=1d&events=eeeeeeee&crumb=cccccccc
```

where

- TTTT - Ticker (e.g., AAPL, MSFT, etc.)
- pppppppp - Period1 is the timestamp (POSIX time stamp) of the beginning date
- qqqqqqqq - Period2 is the timestamp (POSIX time stamp) of the ending date
- eeeeeeee - Event, can be one of 'history', 'div', or 'split'
- cccccccc - Crumb

The CSV file downloaded through the new API has a few format differences from the CSV file from the original iChart source.

1. The order of data fields in each row is slightly different. The fields of the new API are as following (note that the order of the last two fields are swapped from before).
```
Date, Open, High, Low, Close, Adjusted Close, Volume
```

2. The order of the rows for historical quote by the new API is chronical (vs counter-chronical as the old API).
3. The order of the rows for splits/dividents seems random and is not chronically ordered.