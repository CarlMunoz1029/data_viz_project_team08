
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


import pandas as pd


    
    
"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import json
import preprocess
import bubble

app = dash.Dash(__name__)
app.title = 'TP4 | INF8808'

with open('/Users/antoineduplantie-grenier/Documents/École/Été2023/INF8808E/TP4/code-4/src/assets/data/countriesData.json') as data_file:
    data = json.load(data_file)

df_2000 = pd.json_normalize(data, '2000')
df_2015 = pd.json_normalize(data, '2015')

df_2000 = preprocess.round_decimals(df_2000)
df_2015 = preprocess.round_decimals(df_2015)

gdp_range = preprocess.get_range('GDP', df_2000, df_2015)
co2_range = preprocess.get_range('CO2', df_2000, df_2015)

df = preprocess.combine_dfs(df_2000, df_2015)
df = preprocess.sort_dy_by_yr_continent(df)

fig = bubble.get_plot(df, gdp_range, co2_range)
fig = bubble.update_animation_hover_template(fig)
fig = bubble.update_animation_menu(fig)
fig = bubble.update_axes_labels(fig)
fig = bubble.update_template(fig)
fig = bubble.update_legend(fig)

fig.update_layout(height=600, width=1000)
fig.update_layout(dragmode=False)

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
app.title = "project session INF8808"

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("AlayaCare", className="display-4"),
        html.Hr(),
        html.P(
            "Types of views", className="lead"
        ),
        dbc.Nav(
            [
        
                dbc.NavLink("Overview", href="/page-1", active="exact"),
                dbc.NavLink("Patient view", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/page-2":
        return  html.Div(
    [
        dbc.Row(dbc.Col(html.Div(dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            ))), 
        width="auto")),

        dbc.Row(
            dbc.Col(html.Div(        
            dbc.Row(dbc.Col(html.Div(dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            ))), 
        width="auto"))))
        ),

        
    ]
)
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8889)

