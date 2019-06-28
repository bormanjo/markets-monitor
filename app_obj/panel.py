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
from . import subpanel


def panel_template(title="Template Panel", output_row=dbc.Row(), **kwargs):
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

        # Output
        output_row,

        html.Hr(),
    ], **kwargs)

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


def news_component():
    """
    An HTML Div containing a tabbed RSS feed indexed by source
    :return: html Div object
    """

    output_row = dbc.Row([
        dcc.Tabs(id="news-feed-tab-selector", value=list(dl.news.rss_feeds.keys())[0],
                 children=[dcc.Tab(label=source_key, value=source_key) for source_key in dl.news.rss_feeds.keys()]
                 ),
        dbc.Col(id='news-feed-tab', children=[
            dbc.Row(children=[
                html.Div(id='news-feed-content', style={'padding': 2})
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


def equity_component():
    """
    The main equity panel
    :return:
    """

    title = "Equity Markets"

    output_row = dbc.Row(
        dbc.Tabs(id="equity-tab-selector", active_tab="intraday", children=[
            dbc.Tab(label="Intraday", tab_id="intraday", children=[
                subpanel.intraday_plot()
            ]),
            dbc.Tab(label="Historical", tab_id="historical", children=[
                subpanel.historical_plot()
            ])
        ])
    )

    obj = panel_template(title, output_row)

    return obj


def macro_component():
    """
    The main macro panel
    :return:
    """

    title = "Macro Data"

    output_row = dbc.Row(
        dbc.Tabs(id="macro-tab-selector", active_tab="ust-curve", children=[
            dbc.Tab(label="US Treasury Curve", tab_id="ust-curve", children=[
                subpanel.treasury_curve()
            ]),
            dbc.Tab(label="Coming Soon...", tab_id="coming-soon", disabled=True)
        ])
    )

    obj = panel_template(title, output_row)

    return obj
