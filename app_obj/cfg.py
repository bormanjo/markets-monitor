from datetime import datetime, timedelta

today = datetime.today()
three_months_ago = today - timedelta(days=30 * 3)
five_years_ago = today - timedelta(days=252 * 5)


user_tickers = []


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
