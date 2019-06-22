"""
Defines the high level app outline, structure and callback interaction
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
from pandas.tseries.offsets import BDay
import app_obj

# Define the app object
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Testing data
aapl_intraday = dl.equities.get_historical(tickers="AAPL", period="1wk", interval="1h")
aapl_eod = dl.equities.get_historical(tickers="AAPL", period="ytd", interval="1h")
symbols = dl.reference.get_symbols()

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
                app_obj.panel.intraday_plot(),
                app_obj.panel.historical_plot()
            ], width=8),

            # Right Column
            dbc.Col([
                app_obj.panel.news_feed()
            ], width=4)
        ])
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
    end = app_obj.utils.parse_date(dateselector_intraday)

    start = end - BDay(1)

    df = dl.equities.get_historical(tickers=ticker, start_date=start, end_date=end, interval=interval)

    return app_obj.figures.build_ohlcv(df, title=f'{ticker} - Intraday OHLCV ({end.date()})')


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


@app.callback(Output('news-feed-tab', 'children'),
              [Input('news-feed-tab-selector', 'value')])
def update_news_feed_content(news_feed_tab_selector):
    """Updates the news feed"""
    markdown_str = dl.news.get_rss_feed(news_feed_tab_selector, top_n=5)

    return dcc.Markdown(markdown_str)


# Main -----------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
