"""
defines high level html objects used throughout the app
"""

import dash_table
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime, date
from . import utils
import dataloader as dl
import pandas as pd

def get_datatable(id, df, params):
    """
    Returns an HTML DataTable container for a Dash app
    """
    dt = dash_table.DataTable(
        id=id,
        columns=[
            {"name": i, "id": i, "deletable": False} for i in df.columns
        ],
        data=df.to_dict("rows"),
        filtering=params['filtering'],
        sorting=params['sorting'],
        sorting_type=params['sorting_type']
    )

    return dt


def get_graph(id, figure=None):
    """
    Returns a plotly line graph as an HTML object
    """

    if figure is None:
        graph = dcc.Graph(id=id)
    else:
        graph = dcc.Graph(
            id=id,
            figure=figure
        )

    return graph


def get_symbol_selector(id, df, default_value='AAPL'):
    """
    Returns an HTML widger for selecting a ticker
    """

    data = df[["Symbol", "Security Name"]]

    # data.loc[:, "name"] = data["symbol"].map(str) + " - " + data["name"]

    data = data.rename(columns={"Security Name": "label", "Symbol": "value"}).to_dict("records")

    dropdown = dcc.Dropdown(
        id=id,
        options=data, 
        multi=False,
        value=default_value
    )

    return dropdown


def get_date_selector(id, min_date=None, max_date=None, value=None):
    """
    Returns an HTML date selector widget
    """

    if value is None:
        value = datetime.today().date()
    else:
        if not isinstance(value, date):
            raise ValueError("Argument passed to 'value' is of type '{}', not 'date'".format(type(value)))

    selector = dcc.DatePickerSingle(
        id=id,
        date=value,
        max_date_allowed=max_date,
        min_date_allowed=min_date
    )

    return selector


def get_interval_selector(id, default_value='5m'):
    """
    Returns an HTML interval selector
    :param id: HTML Object ID
    :param default_value: Initial Value
    :return: HTML Selector Widget
    """

    data = utils.dict_to_selector_data(dl.equities.interval_mapping)

    selector = dcc.Dropdown(
        id=id,
        options=data,
        multi=False,
        value=default_value
    )

    return selector


def get_period_selector(id, default_value='ytd'):
    """
    Returns an HTML period selector
    :param id: HTML Object ID
    :param default_value: Initial Value
    :return: HTML Selector Widget
    """

    data = utils.dict_to_selector_data(dl.equities.period_mapping)

    selector = dcc.Dropdown(
        id=id,
        options=data,
        multi=False,
        value=default_value
    )

    return selector
