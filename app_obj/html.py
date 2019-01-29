import dash_table
import dash_core_components as dcc
import dash_html_components as html


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


def get_graph(id, figure):
    """
    Returns a plotly line graph as an HTML object
    """

    graph = dcc.Graph(
        id=id,
        figure=figure
    )

    return graph