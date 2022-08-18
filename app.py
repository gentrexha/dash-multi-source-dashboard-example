from src.dune import return_dataframe
from src.ga_api import run_request

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Output, Input
from dash_bootstrap_templates import load_figure_template
import pandas as pd
import plotly.express as px

# Data loading
dune_df = return_dataframe()
ga_df = run_request()
df = pd.merge(dune_df, ga_df, left_on="block_time", right_on="date", how="left")

# Theme
load_figure_template("SANDSTONE")

# App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

# Layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Multi Source Dashboard Example", id="title_h1"),
                        html.Hr(),
                    ]
                ),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(
                            options=[
                                {"label": "Month", "value": "M"},
                                {"label": "Week", "value": "W"},
                                {"label": "Day", "value": "D"},
                            ],
                            value="D",
                            id="aggregate_by_dropdown",
                        )
                    ],
                    md=2,
                ),
            ],
            style={"margin-bottom": "25px"},
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(dcc.Loading(dcc.Graph(id="active_users_graph"))), md=6
                ),
                dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id="trades_graph"))), md=6),
            ],
            style={"margin-bottom": "25px"},
        ),
        dbc.Row(
            [dbc.Col(dbc.Card(dcc.Loading(dcc.Graph(id="conversion_graph")))),],
            style={"margin-bottom": "25px"},
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("active_users_graph", "figure"), Input("aggregate_by_dropdown", "value"),
)
def make_active_users_graph(aggregate_by_dropdown_value):
    dff = (
        df.groupby(pd.Grouper(freq=aggregate_by_dropdown_value, key="block_time"))
        .sum()
        .reset_index()
    )
    fig = px.bar(
        dff,
        x="block_time",
        y="activeUsers",
        title="Daily CoWSwap.exchange visitors (GA)",
        labels={"block_time": "Date", "activeUsers": "Visitors (#)",},
    )
    return fig


@app.callback(
    Output("trades_graph", "figure"), Input("aggregate_by_dropdown", "value"),
)
def make_trades_graph(aggregate_by_dropdown_value):
    dff = (
        df.groupby(pd.Grouper(freq=aggregate_by_dropdown_value, key="block_time"))
        .sum()
        .reset_index()
    )
    fig = px.bar(
        dff,
        x="block_time",
        y="count",
        title="Daily trades (Dune)",
        labels={"block_time": "Date", "count": "Trades (#)",},
    )
    return fig


@app.callback(
    Output("conversion_graph", "figure"), Input("aggregate_by_dropdown", "value"),
)
def make_conversion_graph(aggregate_by_dropdown_value):
    dff = (
        df.groupby(pd.Grouper(freq=aggregate_by_dropdown_value, key="block_time"))
        .sum()
        .reset_index()
    )
    dff["conversion"] = dff["count"] / dff["activeUsers"]
    fig = px.bar(
        dff,
        x="block_time",
        y="conversion",
        title="Daily conversion rate (GA+Dune)",
        labels={"block_time": "Date", "conversion": "Conversion (%)",},
    )
    fig.update_layout(yaxis_range=[0, 1])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
