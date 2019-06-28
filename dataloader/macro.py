from fredapi import Fred
from . import cfg
import configparser
import pandas as pd
from pandas.tseries.offsets import BDay
import datetime

maturities = [30, 20, 10, 7, 5, 2, 1]

UST_YLD_CURVE = {
    **{f"{yr} Yr": f"DGS{yr}" for yr in maturities},
    **{f"{mo} Mo": f"DGS{mo}MO" for mo in [6, 3, 1]},
    **{"Overnight": "DFF"}
}

USD_SWAP_RATES = {yr: f"ICERATES1100USD{yr}Y" for yr in maturities}


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

        for label, series_id in UST_YLD_CURVE.items():
            tsy_data = fred.get_series(
                series_id,
                observation_start=start_date,
                observation_end=end_date
            ).tail(1)
            result.append({
                "Label": label,
                "Year": label,
                "Rate": tsy_data[0],
                "Date": tsy_data.index.date[0]
            })

    return pd.DataFrame(result)


def get_swap_curve(end_dates):
    """Return the USD Swap Curve as of the given end_date"""
    if not isinstance(end_dates, list):
        end_dates = [end_dates]

    result = []

    for end_date in end_dates:
        start_date = end_date - BDay(5)

        for yr, series_id in USD_SWAP_RATES.items():
            swap_data = fred.get_series(
                series_id,
                observation_start=start_date,
                observation_end=end_date
            ).tail(1)
            result.append({
                "Label": f"{yr} Yr",
                "Year": yr,
                "Rate": swap_data[0],
                "Date": swap_data.index.date[0]
            })

    return pd.DataFrame(result)


def get_usd_swap_citation(year):

    date = datetime.date.today().strftime("%b %d, %Y")

    return "ICE Benchmark Administration Limited (IBA), ICE Swap Rates, 11:00 A.M. (London Time)," + \
           f"Based on U.S. Dollar, 10 Year Tenor [ICERATES1100USD{year}Y], retrieved from FRED," + \
           f"Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/ICERATES1100USD{year}Y," + date

