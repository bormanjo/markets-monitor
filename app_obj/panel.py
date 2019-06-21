import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dataloader as dl
import pandas as pd
import app_obj
import app_obj.cfg as cfg


def header():
    """
    The app's HTML header
    :return: html DiH! object
    """

    obj = html.H1(
        "Financial Markets Monitor",
        style={'textAlign': 'center', 'color': cfg.colors['text']}
    )

    return obj


def live_tickers():
    """
    An HTML Div containing a table of live ticker values
    :return:
    """


def intraday_plot():
    """
    An HTML Div containing an interactive plot of intraday OHLCV data
    :return: html Div object
    """

    obj = html.Div(style=cfg.tile_style, children=[
        # Title
        html.H2(
            "Intraday OHLCVs",
            style={'textAlign': 'center', 'color': app_obj.cfg.colors['sub-text']}
        ),
        # Inputs
        html.Div([
            html.Div([
                app_obj.html.get_interval_selector("dropdown-intraday-interval", default_value="5m")
            ], className="three columns", style=cfg.input_style),

            html.Div([
                app_obj.html.get_symbol_selector("dropdown-intraday-symbol",
                                                 df=dl.reference.get_symbols()
                                                 )
            ], className="three columns", style=cfg.input_style),

            html.Div([
                app_obj.html.get_date_selector("dateselector-intraday",
                                               min_date=cfg.min_intraday_date,
                                               max_date=cfg.today
                                               )
            ], className="three columns", style=cfg.input_style)
        ], className="row", style=cfg.input_container_style),

        # Output
        html.Div([
            app_obj.html.get_graph("graph-intraday")
        ])
    ], className="six columns")

    return obj


def historical_plot():
    """
    An HTML Div containing an interactive plot of daily OHLCV data
    :return: html Div object
    """

    obj = html.Div(style=cfg.tile_style, children=[
        # Title
        html.H2(
            "Historical OHLCV",
            style={'textAlign': 'center', 'color': app_obj.cfg.colors['sub-text']}
        ),

        # Inputs
        html.Div([
            html.Div([
                app_obj.html.get_interval_selector("dropdown-historical-interval", default_value="1d")
            ], className="three columns", style=cfg.input_style),

            html.Div([
                app_obj.html.get_symbol_selector("dropdown-historical-symbol",
                                                 df=dl.reference.get_symbols()
                                                 )
            ], className="twelve columns", style=cfg.input_style),

            html.Div([
                app_obj.html.get_date_selector("dateselector-historical-start",
                                               # min_date=cfg.five_years_ago,
                                               max_date=cfg.today,
                                               value=cfg.one_year_ago
                                               )
            ], className="six columns", style=cfg.input_style),

            html.Div([
                app_obj.html.get_date_selector("dateselector-historical-end",
                                               # min_date=cfg.five_years_ago,
                                               max_date=cfg.today,
                                               value=cfg.today
                                               )
            ], className="six columns", style=cfg.input_style)

        ], className="row", style=cfg.input_container_style),

        # Output
        html.Div([
            app_obj.html.get_graph("graph-historical")
        ])
    ], className="six columns")

    return obj
