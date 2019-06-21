import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dataloader as dl
import pandas as pd
from pandas.tseries.offsets import BDay
import app_obj


app = dash.Dash(__name__)

# Defaults/Parameters

empty_ohlcv = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

colors = {
    'background': 'rgb(255, 255, 255)',
    'tile-background': 'rgb(214, 214, 214, 0.5)',
    'text': 'rgb(5, 42, 188)',
    'sub-text': 'rgb(0, 0, 0)',
    'plot-background': 'rgb(185, 204, 232, 0.6)'
}

tile_style = {
    'backgroundColor': colors['tile-background'],
    'border': '2px solid black',
    'borderRadius': '5px'
}

input_container_style = {
    'textAlign': 'center'
}

input_style = {
    'display': 'inline-block',
    'width': '50%',
    'margin': 'auto'
}

aapl_intraday = dl.equities.get_historical(tickers="AAPL", period="1wk", interval="1h")
aapl_eod = dl.equities.get_historical(tickers="AAPL", period="ytd", interval="1h")
symbols = dl.reference.get_symbols()

params = {
    "filtering": True,
    "sorting": True,
    "sorting_type": "multi"
}


def serve_layout():
    layout = html.Div(style=tile_style, children=[
        # Header
        app_obj.panel.header(),

        # Body
        app_obj.panel.intraday_plot(),

        app_obj.panel.historical_plot()
    ])

    return layout


app.layout = serve_layout


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


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)
