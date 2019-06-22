import pandas as pd
from . import _config

# http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs
# ftp://ftp.nasdaqtrader.com/symboldirectory/


def get_listed():
    """Returns a DataFrame of all NASDAQ listings"""
    # Read the file containing listings
    df = pd.read_csv("./dataloader/" + _config.LISTED_FILE, sep='|')

    # Drop the last row (contains extraneous data on file creation time)
    df.drop(df.tail(1).index, inplace=True)

    # Fill NaN's with empty strings
    df.fillna("")

    return df


def get_symbols():
    return get_listed()
