import dash
from dash.dependencies import Input, Output
import dash_table
import datetime
import dash_core_components as dcc
import dash_html_components as html
import dataloader as dl
import pandas as pd
import app_obj

app = dash.Dash(__name__)

crypto_names = dl.markets.crypto.get_symbols()
aapl_intraday = dl.markets.stocks.get_intraday(ticker="AAPL", start=datetime.datetime(2019, 1, 28))

params = {
    "filtering": True,
    "sorting": True,
    "sorting_type" : "multi"
}

# build graph
intraday_fig = app_obj.figures.build_ohlcv(aapl_intraday)


def serve_layout():
    layout = html.Div([
        # Header
        html.H1(
            'The time is: ' + str(datetime.datetime.now())
        ),

        # Body
        app_obj.html.get_DataTable("datatable-crypto", crypto_names, params),

        app_obj.html.get_graph("graph-intraday", figure=intraday_fig)
        
    ])

    return layout

app.layout = serve_layout


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)