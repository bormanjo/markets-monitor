import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dataloader as dl
import pandas as pd
from pandas.tseries.offsets import BDay
import app_obj
import app_obj.cfg as cfg


def sub_panel_template(title="Template Panel", input_row=dbc.Row(), output_row=dbc.Row(), **kwargs):
    """
    A template for designing sub panels
    :param title: String. Title of the panel
    :param input_row: dbc.Row object
    :param output_row: dbc.Row object
    :return: dbc.Col object
    """

    obj = dbc.Col([
        # Title
        dbc.Row(html.H3(title)),

        html.Hr(),

        # Inputs
        input_row,

        # Output
        output_row,

        html.Hr(),
    ], **kwargs)

    return obj


def live_tickers():
    """
    An HTML Div containing a table of live ticker values
    :return:
    """

    pass


def intraday_plot():
    """
    An sub panel containing an interactive plot of intraday OHLCV data
    :return: a sub panel
    """

    title = ""  # "Intraday OHLCV"

    input_row = dbc.Row([
        dbc.Col([
            app_obj.html.get_symbol_selector("dropdown-intraday-symbol", df=dl.reference.get_symbols())
        ], width=8),

        dbc.Col([
            app_obj.html.get_interval_selector("dropdown-intraday-interval", default_value="5m")
        ], width=4),

        dbc.Col([
            dbc.Row([
                dbc.Col(html.H5("Date:", style={'textAlign': 'center'}), width=2, align="center"),
                dbc.Col(app_obj.html.get_date_selector(
                        "dateselector-intraday",
                        min_date=cfg.min_intraday_date,
                        max_date=cfg.today),
                    width=3)
            ])
        ], width=12, style={'padding': 10})
    ])

    output_row = dbc.Row([
        app_obj.html.get_graph("graph-intraday")
    ])

    obj = sub_panel_template(title, input_row, output_row)

    return obj


def historical_plot():
    """
    A sub panel containing an interactive plot of daily OHLCV data
    :return: html object
    """

    title = ""  # "Historical OHLCV"

    input_row = dbc.Row([

        dbc.Col([
            app_obj.html.get_symbol_selector("dropdown-historical-symbol", df=dl.reference.get_symbols())
        ], width=8),

        dbc.Col([
            app_obj.html.get_interval_selector("dropdown-historical-interval", default_value="1d")
        ], width=4),

        dbc.Col([
            dbc.Row([
                dbc.Col(html.H5("Start Date:", style={'textAlign': 'center'}), width=3, align="center"),
                dbc.Col(app_obj.html.get_date_selector("dateselector-historical-start",
                                                       max_date=cfg.today,
                                                       value=cfg.one_year_ago
                                                       ),
                        width=3),
                dbc.Col(html.H5("End Date:", style={'textAlign': 'center'}), width=3, align="center"),
                dbc.Col(app_obj.html.get_date_selector("dateselector-historical-end",
                                                       max_date=cfg.today,
                                                       value=cfg.today
                                                       ),
                        width=3)
            ], align="center")
        ], width=12, style={'padding': 10})

    ], align="center")

    output_row = dbc.Row([
        app_obj.html.get_graph("graph-historical")
    ])

    obj = sub_panel_template(title, input_row, output_row)

    return obj


def treasury_curve():
    """
    An HTML Div containing an interactive US Treasury Curve plot
    :return: HTML Div object
    """

    title = ""  # "US Treasury Curve"

    input_row = dbc.Row([
        dbc.Col([
            app_obj.html.get_date_selector("dateselector-treasury-curve",
                                           max_date=cfg.today - BDay(2),
                                           value=cfg.today - BDay(2))
        ], width=dict(size=2)),
        dbc.Col([
            dbc.Button("Add Date", id="button-treasury-add-date", outline=True, className="mr-1", block=True)
        ], width=dict(size=3, offset=1)),
        dbc.Col([
            dcc.Dropdown(
                id="dropdown-treasury-date",
                options=[
                    {'label': cfg.today - BDay(2), 'value': cfg.today - BDay(2)}
                ],
                multi=True,
                value=cfg.today
            )
        ], width=dict(size=6))
    ], align="center")

    output_row = dbc.Row([
        app_obj.html.get_graph("graph-treasury-curve")
    ])

    obj = sub_panel_template(title, input_row, output_row, width=12)

    return obj
