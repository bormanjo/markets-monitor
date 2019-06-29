import configparser
import ftplib
import os
from datetime import date
from . import cfg

# Constants

FTP_ADDR = cfg.FTP_ADDR
SYMBOL_DIR = cfg.FTP_SYMBOL_DIR
LISTED_FILE = cfg.FTP_LISTED_FILE


def _update_nyse_listed():
    """Gets the index of current listings on NASDAQ"""
    ftp = ftplib.FTP(FTP_ADDR)    
    ftp.login("Anonymous", "Guest")
    ftp.cwd(SYMBOL_DIR)

    # TODO - Assert that location of listed file is inside dataloader/
    ftp.retrbinary("RETR " + LISTED_FILE, open("./dataloader/" + LISTED_FILE, 'wb').write)
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

# Config.ini File -----------------------------------------------------------------------------------------------------


_CFG_FILE = cfg.DL_CFG_FILE

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

    # When deployed on heroku, find the API Keys as an environment variable
    _cfg['API KEY'] = {
        'quandl': os.environ['API_KEY_QUANDL'],
        'fred': os.environ['API_KEY_FRED']
    }
    
    with open(_CFG_FILE, 'w') as cfg_file:
        _cfg.write(cfg_file)
        
    _update(_cfg)

# Cache Directory -----------------------------------------------------------------------------------------------------

_CACHE_DIR = cfg.DL_CACHE_DIR

# Create directory if it does not already exist
if not _CACHE_DIR.exists():
    os.mkdir(_CACHE_DIR)
