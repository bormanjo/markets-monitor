import dash_table
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime


def get_DataTable(id, df, params):
    """
    Returns an HTML DataTable container for a Dash app
    """
    dt = dash_table.DataTable(
        id=id,
        columns=[
            {"name": i, "id": i, "deletable": False} for i in df.columns
        ],
        data=df.to_dict("rows"),
        filtering=params['filtering'],
        sorting=params['sorting'],
        sorting_type=params['sorting_type']
    )

    return dt

def get_graph(id, figure=None):
    """
    Returns a plotly line graph as an HTML object
    """

    if figure is None:
        graph = dcc.Graph(id=id)
    else:
        graph = dcc.Graph(
            id=id,
            figure=figure
        )

    return graph

def get_symbol_selector(id, df):
    """
    Returns an HTML widger for selecting a ticker
    """

    data = df[["name", "symbol"]]

    data.loc[:, "name"] = data["symbol"].map(str) + " - " + data["name"]

    data = data.rename(columns={"name":"label", "symbol":"value"}).to_dict("records")

    dropdown = dcc.Dropdown(
        id=id,
        options=data, 
        multi=False
    )

    return dropdown

def get_date_selector(id, min_date=None, max_date=None):
    """
    Returns an HTML date selector widget
    """

    selector = dcc.DatePickerSingle(
        id=id,
        date=datetime.today(),
        max_date_allowed=max_date,
        min_date_allowed=min_date
    )

    return selector