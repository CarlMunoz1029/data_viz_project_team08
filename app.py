
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

from preprocess import preprocess_general_timeline
from general_timeline import get_general_timeline



import pandas as pd


    
    

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import json
import preprocess
import bubble

from pandas.io.json import json_normalize

font ="Times New Roman"


##this part is for the general timeline
df_tl = pd.read_csv('assets/timeline_dataset.csv', index_col=0)
df_tl = preprocess_general_timeline(df_tl)
fig_timeline = get_general_timeline(df_tl)

recent_events = preprocess.get_recent_events(df_tl)

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
    if pathname == "/page-1":
        filter_button = html.Div(
    [
         dbc.Button(
            "popover-target",
            id="popover-target",
            className="me-1",
        ),
        dbc.Popover(
            dbc.PopoverBody([
        dbc.Label("Choose a bunch"),
        dbc.Checklist(
            options=[
                {"label": "Option 1", "value": 1},
                {"label": "Option 2", "value": 2},
                {"label": "Option 3n", "value": 3,},
            ],
            value=[1,2,3],
            id="checklist-input",
        ),
        dbc.Button(
            "confirm",
            id="popover-confirm",
            className="me-3",
        )
    ]),
            target="popover-target",
            trigger="click",
        ),
    ]
)
        theme = html.Div(children=[dbc.Row([dbc.Col([html.Span("All incidents"), html.Br(),html.Br(),html.Span("Past 24h")]),
                                            dbc.Col(filter_button)]), html.Br(),
        html.Div(children=[dbc.Card([dbc.CardBody([html.H5("Card title", className="card-title"),html.Span("Patient : "+recent_events["PATIENT_ID"][i]), html.Br(),
                    html.Span(recent_events["DAY"][i].strftime('%Y-%m-%d') +" ; "+ recent_events["INCIDENT_TIME"][i].strftime('%H:%M'))])], 
                                    style={"maxHeight": "115px","background-color":recent_events["COLOR"][i], 'color':'white'}) for i in recent_events.index],
            style={"maxHeight": "1015px", "overflow-y":"scroll","background-color": "#f8f9fa",'height' : '60vh','border': '1px solid black'})])        
        layout = dbc.Row([dbc.Col(html.Div(dcc.Graph(className='graph', figure=fig_timeline, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            ), style={'width': '55vw', 'height':'75vh'}))),
                dbc.Col(html.Div(
                    className='feed-div2',
                    style={
                        'justifyContent': 'center',
                        'alignItems': 'center',
                        'display': 'inline-block'},
                    children=[
                        html.Div(id='feed2', style={
                            #'visibility': 'hidden',
                            'border': '1px solid black',
                            'padding': '10px',
                            'min-width' : '15vw',
                            'min-height' : '75vh'},
                                children=[
                                    html.Div(id='marker-title2', style={
                                        'fontSize': '24px'}),
                                    html.Div(id='mode2', style={
                                        'fontSize': '16px'}),
                                    html.Div(id='theme2', children=[theme], style={
                                        'fontSize': '16px'})])]))])


        return layout
        #return html.P("This is the content of page 1. Yay!")
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




