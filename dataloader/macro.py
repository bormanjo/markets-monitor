from fredapi import Fred
from . import cfg
import configparser
import pandas as pd
from pandas.tseries.offsets import BDay

_USD_YLD_CURVE = {
    "30 Yr":{
        "Years": 30,
        "id": "DGS30"
    },
    "20 Yr":{
        "Years": 20,
        "id": "DGS20"
    },
    "10 Yr":{
        "Years": 10,
        "id": "DGS10"
    },
    "7 Yr":{
        "Years": 7,
        "id": "DGS7"
    },
    "5 Yr":{
        "Years": 5,
        "id": "DGS5"
    },
    "2 Yr":{
        "Years": 2,
        "id": "DGS2"
    },
    "1 Yr":{
        "Years": 1,
        "id": "DGS1"
    },
    "6 Mo":{
        "Years": 0.5,
        "id": "DGS6MO"
    },
    "3 Mo":{
        "Years": 0.25,
        "id": "DGS3MO"
    },
    "1 Mo":{
        "Years": 0.083,
        "id": "DGS1MO"
    },
    "Overnight":{
        "Years": 1.0/360.0,
        "id": "DFF"
    }
}


def get_api_key():
    _cfg = configparser.ConfigParser()
    _cfg.read(cfg.DL_CFG_FILE)
    return _cfg["API KEY"]["FRED"]


fred = Fred(get_api_key())


def get_treasury_curve(end_dates):
    """Return the USD Treasury Curve as of the given end_date"""
    if not isinstance(end_dates, list):
        end_dates = [end_dates]

    result = []

    for end_date in end_dates:
        start_date = end_date - BDay(2)

        for maturity, meta in _USD_YLD_CURVE.items():
            tsy_data = fred.get_series(
                meta["id"],
                observation_start=start_date,
                observation_end=end_date
            ).tail(1)
            result.append({
                "Label": maturity,
                "Year": meta["Years"],
                "Rate": tsy_data[0],
                "Date": tsy_data.index.date[0]
            })

    return pd.DataFrame(result)

