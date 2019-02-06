import dash
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime, timedelta
import dash_core_components as dcc
import dash_html_components as html
import dataloader as dl
import pandas as pd
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

today = datetime.today()
three_months_ago = today - timedelta(days = 30 * 3)
five_years_ago = today - timedelta(days = 360 * 5)

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
        html.H1(
            "Financial Markets Monitor",
            style={'textAlign': 'center', 'color': colors['text']}
        ),

        # Body
        html.Div(style=tile_style, children=[
            html.H2(
                "Active Cryptocurrencies",
                style={'textAlign': 'center', 'color': colors['sub-text']}
            ),
            app_obj.html.get_DataTable("datatable-interative", crypto_names, params),
        ], className="five columns"),
                
        

        # Intraday Panel
        html.Div(style=tile_style, children=[
            html.H2(
                "Intraday OHLCVs",
                style={'textAlign': 'center', 'color': colors['sub-text']}
            ),
            # Inputs
            html.Div([
                html.Div([
                    app_obj.html.get_symbol_selector("dropdown-intraday-symbol", df=symbols)
                ], className="six columns", style=input_style), 
                
                html.Div([
                    app_obj.html.get_date_selector("dateselector-intraday", min_date=three_months_ago)
                ], className="six columns", style=input_style)

            ], className="row", style=input_container_style),
            
            # Output
            html.Div([
                app_obj.html.get_graph("graph-intraday")
            ])
        ], className="six columns",)

        
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
    start = datetime.strptime(dateselector_intraday, '%Y-%m-%d')

    print(start)

    df = dl.markets.stocks.get_intraday(ticker=ticker, start=start)

    return app_obj.figures.build_ohlcv(df, title='{} - Intraday OHLCV ({})'.format(ticker, start.date()))


app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)