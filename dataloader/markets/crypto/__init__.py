from .crypto import get_symbols

# Note that cryptos can essentially be retrieved through the same functions as in stocks
# The 'crypto's module is a design choice

from ..stocks import get_realtime_quote, get_last_trade, get_historical, get_intraday, get_realtime_book     