"""
Defines common Plotly figures used throughout the app
"""

import plotly.graph_objs as go


def build_ohlcv(df, title='Intraday OHLCV Plot'):
    """
    Builds an OHLCV candlestick plot and returns a Plotly figure
    """

    cols = ["Open", "High", "Low", "Close", "Volume"]

    if not [col in df.columns for col in cols]:
        raise ValueError("'df' does not contain all required OHLCV columns: {}".format(cols))

    # Build the OHLC candlestick trace
    trace1 = go.Ohlc(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="OHLC"
    )

    # Build the Volume barchart
    trace2 = go.Bar(
        x=df.index,
        y=df["Volume"],
        yaxis='y2',         # Plot on a separate axis
        name="Volume",
        opacity=0.6,        # Slightly opaque
        marker=dict(
            color='rgb(66, 134, 244)'   # Blue color
        )
    )

    # Define the layout
    layout = go.Layout(
        showlegend=False,
        title=title,
        yaxis=dict(
            title='OHLC',
            side="left"
        ),
        yaxis2=dict(
            title='Volume',
            side="right",     
            overlaying="y"  # Volume plot overlays the candlestick
        )
    )

    # Aggregate the traces and build the figure
    data = [trace1, trace2]
    fig = go.Figure(data=data, layout=layout)

    # Return the plotly figure
    return fig