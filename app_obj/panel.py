"""
Defines the main component panels of the app
"""

import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dataloader as dl
import pandas as pd
import app_obj
import app_obj.cfg as cfg


def panel_template(title="Template Panel", input_row=dbc.Row(), output_row=dbc.Row()):
    """
    A template for designing panels
    :param title: String. Title of the panel
    :param input_row: dbc.Row object
    :param output_row: dbc.Row object
    :return: dbc.Col object
    """

    obj = dbc.Col([
        # Title
        dbc.Row(html.H2(title)),

        html.Hr(),

        # Inputs
        input_row,

        # Output
        output_row,

        html.Hr(),
    ])

    return obj


def header():
    """
    The app's HTML header
    :return: html Div object
    """

    obj = dbc.Jumbotron([
        html.H1("Financial Markets Monitor")
    ])

    return obj


def live_tickers():
    """
    An HTML Div containing a table of live ticker values
    :return:
    """

    pass


def intraday_plot():
    """
    An HTML Div containing an interactive plot of intraday OHLCV data
    :return: html Div object
    """

    title = "Intraday OHLCV"

    input_row = dbc.Row([
        dbc.Col([
            app_obj.html.get_symbol_selector("dropdown-intraday-symbol", df=dl.reference.get_symbols())
        ], width=8),

        dbc.Col([
            app_obj.html.get_interval_selector("dropdown-intraday-interval", default_value="5m")
        ], width=4),

        dbc.Col([
            app_obj.html.get_date_selector(
                "dateselector-intraday",
                min_date=cfg.min_intraday_date,
                max_date=cfg.today
            )
        ], width=12)
    ])

    output_row = dbc.Row([
        app_obj.html.get_graph("graph-intraday")
    ])

    obj = panel_template(title, input_row, output_row)

    return obj


def historical_plot():
    """
    An HTML Div containing an interactive plot of daily OHLCV data
    :return: html Div object
    """

    title = "Historical OHLCV"

    input_row = dbc.Row([
        dbc.Col([
            app_obj.html.get_symbol_selector("dropdown-historical-symbol", df=dl.reference.get_symbols())
        ], width=8),

        dbc.Col([
            app_obj.html.get_interval_selector("dropdown-historical-interval", default_value="1d")
        ], width=4),

        dbc.Col([
            app_obj.html.get_date_selector("dateselector-historical-start",
                                           max_date=cfg.today,
                                           value=cfg.one_year_ago
                                           )
        ], width=6),

        dbc.Col([
            app_obj.html.get_date_selector("dateselector-historical-end",
                                           max_date=cfg.today,
                                           value=cfg.today
                                           )
        ], width=6)
    ])

    output_row = dbc.Row([
        app_obj.html.get_graph("graph-historical")
    ])

    obj = panel_template(title, input_row, output_row)

    return obj


def news_feed():
    """
    An HTML Div containing a tabbed RSS feed indexed by source
    :return: html Div object
    """

    output_row = dbc.Row([
        dcc.Tabs(id="news-feed-tab-selector", value=list(dl.news.rss_feeds.keys())[0],
                 children=[dcc.Tab(label=source_key, value=source_key) for source_key in dl.news.rss_feeds.keys()]
                 ),
        html.Div(id='news-feed-tab', children=[
            dbc.Row(children=[
                html.Div(id='news-feed-content')
            ]),
            dbc.Row(children=[
                dbc.Col(
                    dbc.Button("< Previous", id="news-button-back", outline=True, color="primary",
                               className="mr-1", block=True, n_clicks_timestamp=0),
                    width=6
                ),
                dbc.Col(
                    dbc.Button("Next >", id="news-button-next", outline=True, color="primary",
                               className="mr-1", block=True, n_clicks_timestamp=0),
                    width=6
                )
            ])
        ])
    ])

    obj = panel_template("News Feed", output_row=output_row)

    return obj
