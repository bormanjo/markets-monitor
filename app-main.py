"""
Defines the high level app outline, structure and callback interaction
"""

import dash
from dash.dependencies import Input, Output, State
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dataloader as dl
import pandas as pd
from pandas.tseries.offsets import BDay
import app_obj
from flask import Flask
import os

try:
    _DEV_ENVIRONMENT = False

    # The following are setup instructions for a Production Environment
    server = Flask(__name__)
    server.secret_key = os.environ.get('secret_key', 'secret')  # App will not find this if running local development

    app = dash.Dash(name= __name__, server=server, external_stylesheets=[dbc.themes.LUX])  # Cosmo, Journal, Litera, Lumen
    app.config.supress_callback_exceptions = True
except AttributeError as e:
    # Setup instruction for Development Environment
    _DEV_ENVIRONMENT = True

    app = dash.Dash(name=__name__, external_stylesheets=[dbc.themes.LUX])

# GLOBALS
active_rss_tab = ""
active_rss_page = 0


params = {
    "filtering": True,
    "sorting": True,
    "sorting_type": "multi"
}


def serve_layout():
    # noinspection PyPackageRequirements
    layout = dbc.Container([
        # Header
        app_obj.panel.header(),

        # Body
        dbc.Row([
            # Left Column
            dbc.Col([
                app_obj.panel.equity_component(),
                app_obj.panel.macro_component()
            ], width=8),

            # Right Column
            dbc.Col([
                app_obj.panel.news_component()
            ], width=4),

            dbc.Col([
            # F
            ], width=12)

        ]),
    ])

    return layout


# Pass layout to app object for display
app.layout = serve_layout


# Callbacks ------------------------------------------------------------------------------------------------------------


@app.callback(
    Output('graph-intraday', 'figure'),
    [
        Input('dropdown-intraday-symbol', 'value'),
        Input('dateselector-intraday', 'date'),
        Input('dropdown-intraday-interval', 'value')
    ]
)
def update_intraday_graph(dropdown_intraday_symbol, dateselector_intraday, dropdown_intraday_interval):
    """
    Updates the intraday plot
    """

    # Variables to update
    ticker = dropdown_intraday_symbol
    interval = dropdown_intraday_interval
    start = app_obj.utils.parse_date(dateselector_intraday)

    end = start + BDay(1)

    df = dl.equities.get_historical(tickers=ticker, start_date=start, end_date=end, interval=interval)

    return app_obj.figures.build_ohlcv(df, title=f'{ticker} - Intraday OHLCV ({start.date()})')


@app.callback(
    Output('graph-historical', 'figure'),
    [
        Input('dropdown-historical-symbol', 'value'),
        Input('dateselector-historical-start', 'date'),
        Input('dateselector-historical-end', 'date'),
        Input('dropdown-historical-interval', 'value')
    ]
)
def update_historical_graph(dropdown_historical_symbol, dateselector_historical_start, dateselector_historical_end,
                            dropdown_historical_interval):
    """
    Updates the historical plot
    """

    # Variables to update
    ticker = dropdown_historical_symbol
    start = app_obj.utils.parse_date(dateselector_historical_start).date()
    end = app_obj.utils.parse_date(dateselector_historical_end).date()
    interval = dropdown_historical_interval

    df = dl.equities.get_historical(tickers=ticker, start_date=start, end_date=end, interval=interval)

    return app_obj.figures.build_ohlcv(df, title=f'{ticker} - Historical OHLCV ({start} to {end})')


@app.callback(
    Output('dropdown-treasury-date', 'options'),
    [
        Input('button-treasury-add-date', 'n_clicks')
    ],
    [
        State('dateselector-treasury-curve', 'date'),
        State('dropdown-treasury-date', 'options')
    ]
)
def update_treasury_date_dropdown(add_button, date, existing_dates):
    """
    Updates the date dropdown selector for the US Treasury Curve plot
    """
    date = app_obj.utils.parse_date(date).date()

    existing_dates_lst = [str(d["value"]) for d in existing_dates]

    if str(date) not in existing_dates_lst:
        existing_dates.append({'label': date, 'value': date})

    return existing_dates


@app.callback(
    Output('dropdown-swap-date', 'options'),
    [
        Input('button-swap-add-date', 'n_clicks')
    ],
    [
        State('dateselector-swap-curve', 'date'),
        State('dropdown-swap-date', 'options')
    ]
)
def update_swap_date_dropdown(add_button, date, existing_dates):
    """
    Updates the date dropdown selector for the US Treasury Curve plot
    """
    date = app_obj.utils.parse_date(date).date()

    existing_dates_lst = [str(d["value"]) for d in existing_dates]

    if str(date) not in existing_dates_lst:
        existing_dates.append({'label': date, 'value': date})

    return existing_dates


@app.callback(
    Output('graph-treasury-curve', 'figure'),
    [
        Input('dropdown-treasury-date', 'value')
    ]
)
def update_treasury_curve_graph(dates):
    """
    Updates the US Treasury Yield Curve plot
    """

    if not isinstance(dates, list):
        dates = [dates]

    # Variables to update
    dates = list(map(app_obj.utils.parse_date, dates))
    df = dl.macro.get_treasury_curve(dates)

    if len(dates) > 1:
        title = "US Treasury Yield Curve"
    elif len(dates) == 1:
        title = f"US Treasury Yield Curve (as of {dates[0].date()})"
    else:
        title = ""

    return app_obj.figures.build_yield_curve(df, title)


@app.callback(
    Output('graph-swap-curve', 'figure'),
    [
        Input('dropdown-swap-date', 'value')
    ]
)
def update_swap_curve_graph(dates):
    """
    Updates the US Treasury Yield Curve plot
    """

    if not isinstance(dates, list):
        dates = [dates]

    # Variables to update
    dates = list(map(app_obj.utils.parse_date, dates))
    df = dl.macro.get_swap_curve(dates)

    if len(dates) > 1:
        title = "USD Swap Curve"
    elif len(dates) == 1:
        title = f"USD Swap Curve (as of {dates[0].date()})"
    else:
        title = ""

    return app_obj.figures.build_yield_curve(df, title)


@app.callback(
    Output("usd-swap-citations", "is_open"),
    [Input("usd-swap-citations-button", "n_clicks")],
    [State("usd-swap-citations", "is_open")],
)
def toggle_usd_swap_citations(n, is_open):
    if n:
        return not is_open
    return is_open



@app.callback(
    Output('news-feed-content', 'children'),
    [
        Input('news-feed-tab-selector', 'value'),
        Input('news-button-back', 'n_clicks_timestamp'),
        Input('news-button-next', 'n_clicks_timestamp')
    ]
)
def update_news_feed_content(news_feed_tab_selector, news_button_back, news_button_next):
    """Updates the news feed"""

    global active_rss_tab       # Refers to the current RSS tab
    global active_rss_page      # Refers to the current page w/in the tab

    # When tabs change, change the active tab and reset page count
    change_tab = active_rss_tab != news_feed_tab_selector

    if change_tab:
        active_rss_tab = news_feed_tab_selector
        active_rss_page = 0

    # Get the RSS feed from the data
    feed_entries = dl.news.get_rss_feed(news_feed_tab_selector)
    max_page = len(range(0, len(feed_entries), 5))

    # If 'back' was pressed last and page is greater than 0 -> decrement page
    if int(news_button_back) > int(news_button_next) and active_rss_page > 0 and not change_tab:
        active_rss_page -= 1
    # If 'next' was pressed and page is less than max -> increment page
    elif int(news_button_next) > int(news_button_back) and active_rss_page < max_page and not change_tab:
        active_rss_page += 1

    # Map each entry in the feed into a news card
    content = list(map(app_obj.html.get_news_card, feed_entries[active_rss_page:(active_rss_page+5)]))

    # Add the row
    content += [dbc.Row(children=[
        dbc.Col(
            html.H5(f"{active_rss_page + 1}/{max_page + 1}", style={"text-align": "center", 'padding': 5}),
            width=12)
    ])]

    return html.Div(children=content)


# Main -----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__" and _DEV_ENVIRONMENT:
    app.run_server(debug=True, host='0.0.0.0', port=8050)
