import iexfinance as iex
import pandas as pd
from datetime import datetime, date

def get_realtime_quote(tickers):
    """
    Retrieves realtime prices for a ticker or list of tickers.
    Returns a DataFrame.
    """
    
    symbols = []
    prices = []
    
    if isinstance(tickers, str):
        # Get quote and provide a single entry
        quote = iex.stock.Stock(tickers).get_price()
        
        prices.append(quote)
        symbols.append(tickers)
        
    elif isinstance(tickers, list):
        # Get quotes and provide multiple entries
        quotes = iex.stock.Stock(tickers).get_price()
        
        for sym, px in quotes.items():
            symbols.append(sym)
            prices.append(px)
    else:
        raise Warning("Argument passed to tickers is not a symbol or list of symbols")
    
    # Return entries
    return pd.DataFrame({"Symbols": symbols, "Price": prices})

def get_last_trade(tickers):
    """
    Retrieves the last trade executed (price and size) for the given ticker(s).
    Returns a DataFrame.
    """
    
    last = iex.get_market_last(tickers)
    
    return pd.DataFrame(last)
    

def get_historical(tickers, start=date.today(), end=date.today(), period="daily"):
    """
    Retrieves historical OHLCV pricing data for a ticker or list of tickers. IEX limits historical data to 5 Years.
    :param period: Defaults to 'daily'. Also accepts 'weekly', 'monthly', 'yearly'.
    Returns a DataFrame.
    """
    
    # Check period
    if not period in ['daily', 'weekly', 'monthly', 'yearly']:
        raise ValueError("Argument passed to 'period' parameter: '{}' is invalid.".format(period))
        
    # Check dates
    if not (isinstance(start, datetime) or isinstance(start, pd.date)):
        raise ValueError("Argument passed to 'start' parameter: '{}' is invalid.".format(start))
        
    if not (isinstance(end, datetime) or isinstance(end, pd.date)):
        raise ValueError("Argument passed to 'end' parameter: '{}' is invalid.".format(end))
    
    # Retrieve data in pandas format
    df = iex.stocks.get_historical_data(tickers, start, end, output_format="pandas")
    
    return df

def get_intraday(ticker, start=date.today()):
    """
    Retrieves historical intraday (minutely) OHLCV pricing data for a ticker. IEX limits historical intraday data to 3 months.
    May only retrieve one day at a time.
    Returns a DataFrame.
    """
       
    # Check dates
    if not (isinstance(start, datetime) or isinstance(start, pd.date)):
        raise ValueError("Argument passed to 'start' parameter: '{}' is invalid.".format(start))
        
    if not (isinstance(end, datetime) or isinstance(end, pd.date)):
        raise ValueError("Argument passed to 'end' parameter: '{}' is invalid.".format(end))
        
    # Retrieve data
    df = iex.stocks.get_historical_intraday(ticker, start, output_format="pandas")
    
    # Return OHLCV
    cols = ["open", "high", "low", "close", "volume"]
    return df[cols]
        
def get_realtime_book(tickers):
    """
    Retrieves book information for the given ticker(s).
    Returns a DataFrame.
    """
    
    # Get book data for all tickers
    books = iex.get_market_book(tickers)
    
    # DF for output data
    out = pd.DataFrame()
    
    # For each symbol, symbol's book
    for sym, book in books.items():
        
        # Tabulate the bids, asks
        bids = pd.DataFrame(book["bids"])
        asks = pd.DataFrame(book["asks"])
        
        # Define price types
        bids["type"] = "bid"
        asks["type"] = "ask"
        
        # Append together
        book_df = bids.append(ask)
        
        # Denote the corresponding symbol
        book_df["ticker"] = sym
        
        # Append to output
        out = out.append(book_df, ignore_index=True)
        
    # Return collected book data
    return out
        
    
    