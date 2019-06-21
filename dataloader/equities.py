import pandas as pd
import datetime
import yfinance

period_mapping = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "10 Years": "10y",
    "Year-to-date": "ytd",
    "Max": "max"
}

interval_mapping = {
    "1 Minute": "1m",
    "2 Minute": "2m",
    "5 Minute": "5m",
    "15 Minute": "15m",
    "30 Minute": "30m",
    "60 Minute": "60m",
    "90 Minute": "90m",
    "1 Hour": "1h",
    "1 Day": "1d",
    "5 Day": "5d",
    "1 Week": "1wk",
    "1 Month": "1mo",
    "3 Month": "3mo"
}

market_start = "09:30"
market_end = "16:00"
        
def get_historical(tickers, period="ytd", start_date=None, end_date=None, **kwargs):
    """Returns historical EoD or Intraday data for the given tickers"""
    return yfinance.download(
        tickers,
        period=period, 
        start=start_date, 
        end=end_date,
        progress=False,
        **kwargs
    )
            