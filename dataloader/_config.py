import configparser
import pathlib
import ftplib
from datetime import date

# Constants

FTP_ADDR = "ftp.nasdaqtrader.com"
SYMBOL_DIR = "symboldirectory/"
LISTED_FILE = "nasdaqlisted.txt"

def _update_nyse_listed():
    """Gets the index of current listings on NASDAQ"""
    ftp = ftplib.FTP(FTP_ADDR)    
    ftp.login("Anonymous", "Guest")
    ftp.cwd(SYMBOL_DIR)
    ftp.retrbinary("RETR " + LISTED_FILE, open(LISTED_FILE, 'wb').write)
    ftp.quit()
    
    return True
    
def _update(cfg):
    """Updates NYSE listings and last update date"""
    
    # Update NYSE data
    _update_nyse_listed()
    
    # Overwrite the date
    cfg['DATA']['Last Update'] = str(date.today())
    
    # Save to file
    with open(_CFG_FILE, 'w') as cfg_file:
        cfg.write(cfg_file)
        
    return True

_CFG_FILE = pathlib.Path("./dataloader/config.ini")

_cfg = configparser.ConfigParser()

if _CFG_FILE.exists():
    # Read config file
    _cfg.read(_CFG_FILE)
    
    # Check if not updated today
    if _cfg['DATA']['Last Update'] != date.today():
        # Update listings and config
        _update(_cfg)
    else:
        # No update
        pass
        
else:
    # Config file does not exist
    _cfg['DATA'] = {
        'Last Update': date.today()
    }
    
    with open(_CFG_FILE, 'w') as cfg_file:
        _cfg.write(cfg_file)
        
    _update(_cfg)
