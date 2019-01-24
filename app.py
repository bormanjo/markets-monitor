import datetime

import dash
import dash_html_components as html

app = dash.Dash(__name__)

def serve_layout():
    return html.H1('The time is: ' + str(datetime.datetime.now()))

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)