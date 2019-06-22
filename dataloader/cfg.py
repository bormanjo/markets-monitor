import pathlib

FTP_ADDR = "ftp.nasdaqtrader.com"
FTP_SYMBOL_DIR = "symboldirectory/"
FTP_LISTED_FILE = "nasdaqlisted.txt"

DL_DIR = pathlib.Path("./dataloader")
DL_CFG_FILE = DL_DIR / "config.ini"
DL_CACHE_DIR = DL_DIR / "cache"
