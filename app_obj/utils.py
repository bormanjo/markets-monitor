import datetime
import pandas as pd


def parse_date(dateselector):
    """
    Parses input from a date selector into a datetime object
    :param dateselector: An HTMl dateselector object
    :return: datetime object
    """
    return datetime.datetime.strptime(dateselector.split(" ")[0], '%Y-%m-%d')


def dict_to_selector_data(d):
    """
    Converts a dict into a list of dicts for dropdown selector data
    :param d:
    :return:
    """
    data = {
        "label": list(d.keys()),
        "value": list(d.values())
    }

    return pd.DataFrame(data).to_dict("records")
