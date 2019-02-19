import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dataloader as dl
import pandas as pd
import app_obj
from iexfinance.utils.exceptions import IEXSymbolError

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

crypto_names = dl.markets.crypto.get_symbols()
aapl_intraday = dl.markets.stocks.get_intraday(ticker="AAPL", start=datetime(2019, 1, 28))
symbols = dl.markets.reference.get_symbols()

params = {
    "filtering": True,
    "sorting": True,
    "sorting_type" : "multi"
}


def serve_layout():
    layout = html.Div(style=tile_style, children=[
        # Header
        app_obj.panel.header(),

        # Body
        app_obj.panel.crypto_table(),

        app_obj.panel.intraday_plot(),

        app_obj.panel.historical_plot()
    ])

    return layout


app.layout = serve_layout


@app.callback(
    Output('graph-intraday', 'figure'),
    [
        Input('dropdown-intraday-symbol', 'value'),
        Input('dateselector-intraday', 'date')
    ]
)
def update_intraday_graph(dropdown_intraday_symbol, dateselector_intraday):
    """
    Updates the intraday plot
    """

    ticker = dropdown_intraday_symbol
    start = datetime.strptime(dateselector_intraday.split(" ")[0], '%Y-%m-%d')

    df = dl.markets.stocks.get_intraday(ticker=ticker, start=start)

    return app_obj.figures.build_ohlcv(df, title='{} - Intraday OHLCV ({})'.format(ticker, start.date()))


@app.callback(
    Output('graph-historical', 'figure'),
    [
        Input('dropdown-historical-symbol', 'value'),
        Input('dateselector-historical-start', 'date'),
        Input('dateselector-historical-end', 'date')
    ]
)
def update_historical_graph(dropdown_historical_symbol, dateselector_start, dateselector_end):
    """
    Updates the historical plot
    """

    ticker = dropdown_historical_symbol
    start = datetime.strptime(dateselector_start.split(" ")[0], '%Y-%m-%d')
    end = datetime.strptime(dateselector_end.split(" ")[0], '%Y-%m-%d')

    try:
        df = dl.markets.stocks.get_historical(tickers=ticker, start=start, end=end)
    except IEXSymbolError as err:
        # TODO - Display error stating no data available
        print("No data available for '{}'".format(ticker))
        return "No Data"

    return app_obj.figures.build_ohlcv(df, title='{} - Historical OHLCV ({start} to {end})'.format(
        ticker,
        start=start.date(),
        end=end.date()
    ))


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)