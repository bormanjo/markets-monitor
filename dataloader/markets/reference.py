import iexfinance as iex
import pandas as pd
from datetime import datetime, date, timedelta


_symbol_type_mapping = {"ad": "ADR",
                        "re": "REIT",
                        "ce": "Closed End Fund",
                        "si": "Secondary Issue",
                        "lp": "Limited Partnership",
                        "cs": "Common Stock",
                        "et": "ETF"
}

today = datetime.today()
three_months_ago = today - timedelta(days = 30 * 3)
five_years_ago = today - timedelta(days = 360 * 5)
                        
def get_symbols():
    """
    Retreives a table of valid symbols for which data may be retrieved.
    Returns a DataFrame.
    """
    
    symbols = iex.get_available_symbols()
    return pd.DataFrame(data=symbols)

def get_symbol_types():
    """
    Retrieves a mapping of symbol types in the IEX data feed
    Returns a dictionary.
    """
    
    return _symbol_type_mapping

def get_market_stats_recent():
    """
    Retrieves a table of recent market statistics.
    Returns a DataFrame.
    """
    
    stats = iex.get_stats_recent()
    return pd.DataFrame(stats)