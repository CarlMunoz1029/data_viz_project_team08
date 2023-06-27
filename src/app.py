
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Antoine Duplantie
    Course: INF8808
    Python Version: 3.9.6

    This file is the entry point for our dash app.
'''


import dash
from dash import html
from dash import dcc
from dash import ctx
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from preprocess import preprocess_general_timeline
from general_timeline import get_general_timeline
from adls_graph import get_patient_graph


import pandas as pd

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, ctx, ALL

import json
import preprocess

from pandas.io.json import json_normalize

font ="Times New Roman"


## this part is for the general timeline
df_tl = pd.read_csv('assets/timeline_dataset.csv', index_col=0)
df_tl = preprocess_general_timeline(df_tl)
fig_timeline = get_general_timeline(df_tl)

recent_events = preprocess.get_recent_events(df_tl)
curr=recent_events
app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
server = app.server
app.title = "project session INF8808"

# notesfeed fd
df = pd.read_csv('assets/notes.csv')
df = df.sort_values(by='DAY', ascending=False)

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
NOTEFEED_STYLE ={
  "width": "300px",
  'padding': '10px',
}

PATIENT_LIST_STYLE={
    'width': '10vw',
    'height': "2.5vw",
    "marginTop": 2.5,
    "fontSize": 13,
    "font-weight": 'bold',
    "textAlign": "center"}


PATIENT_LIST_STYLE_FIRST={
    'width': '10vw',
    'height': "2.5vw",
    "marginTop": 40,
    "fontSize": 13,
    "font-weight": 'bold',
    "textAlign": "center"
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

notesFeed = html.Div(
    children=[
        html.H1("Patient Notes Feed"),
        html.Div(
            children=[
                html.H3("Patient Filter"),
                dcc.Dropdown(
                    id='patient-dropdown',
                    options=[{'label': str(pid), 'value': pid} for pid in df['PATIENT_ID'].unique()],
                    placeholder='Select a patient',
                    style=NOTEFEED_STYLE
                ),
            ],
            style={'margin': '10px'}
        ),
        html.Div(id='note-feed')
    ]
)


patient_names = list(df_tl['PATIENT_ID'].unique())

list_patients = html.Div(
    [
        dbc.ListGroup(dbc.Stack(
            [
                dbc.ListGroupItem(patient_names[-1], href="/page-3", action=True, style=PATIENT_LIST_STYLE_FIRST, className="border "),
                dbc.ListGroupItem(patient_names[-2], href="/page-4", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-3], href="/page-5", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-4], href="/page-6", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-5], href="/page-7", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-6], href="/page-8", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-7], href="/page-9", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-8], href="/page-10", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-9], href="/page-11", action=True, style=PATIENT_LIST_STYLE, className="border "),
                dbc.ListGroupItem(patient_names[-10], href="/page-12", action=True, style =PATIENT_LIST_STYLE, className="border ")
            ], gap=2)
        )
    ]
)


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):

    
    filter_button = html.Div(
[
        dbc.Button(
        "Filter incidents",
        id="popover-target",
        className="me-1",
    ),
    dbc.Popover(
        dbc.PopoverBody([
    dbc.Label("Choose a bunch"),
    dbc.Checklist(
        options=[
            {"label": "Pain", "value": 1},
            {"label": "Falls", "value": 2},
            {"label": "Hospitalizations", "value": 3,},
        ],
        value=[1,2,3],
        id="checklist-input",
    ),
    dbc.Button(
        "confirm",
        id="popover-confirm",
        n_clicks=0,
        className="me-3",
    )
]),
        target="popover-target",
        trigger="click",
    ),
]
)

#55vw
    
    theme = html.Div(children=[dbc.Row([dbc.Col([html.Span("All incidents"), html.Br(),html.Br(),html.Span("Past 24h")]),
                                        dbc.Col(filter_button)]), html.Br(),
    html.Div(id='card_main', children=[dbc.Card([dbc.CardBody([html.H5(recent_events["INCIDENT"][i].title(), className="card-title"),html.Span("Patient : "+recent_events["PATIENT_ID"][i]), html.Br(),
                html.Span(recent_events["DAY"][i].strftime('%Y-%m-%d') +" ; "+ recent_events["INCIDENT_TIME"][i].strftime('%H:%M'))])], 
                                style={"maxHeight": "115px","background-color":recent_events["COLOR"][i], 'color':'white'}) for i in recent_events.index],
        style={"maxHeight": "1015px", "overflow-y":"scroll","background-color": "#f8f9fa",'height' : '60vh','border': '1px solid black'})])        
    layout = dbc.Row([dbc.Col(list_patients, align="top"), dbc.Col(html.Div(dcc.Graph(className='graph', figure=fig_timeline, config=dict(
        scrollZoom=False,
        showTips=False,
        showAxisDragHandles=False,
        doubleClick=False,
        displayModeBar=False
        ), style={'height': '75vh',
                  'width':'50vw'}))), 
            dbc.Col(html.Div(
                className='feed-div2',
                style={
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'display': 'inline-block',
                    'width': '16vw'},
                children=[
                    html.Div(id='feed2', style={
                        #'visibility': 'hidden',
                        'border': '1px solid black',
                        'padding': '10px',
                        'min-width' : '16vw',
                        'min-height' : '75vh'},
                            children=[
                                html.Div(id='marker-title2', style={
                                    'fontSize': '18px'}),
                                html.Div(id='mode2', style={
                                    'fontSize': '18px'}),
                                html.Div(id='theme2', children=[theme], style={
                                    'fontSize': '14px'})])]))], className="g-0")

    if pathname == "/page-1":

        return layout
        #return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return notesFeed
    

    elif pathname in ["/page-3","/page-4","/page-5","/page-6","/page-7","/page-8","/page-9","/page-10","/page-11","/page-12"]:

        selected_patient = patient_names[-(int(pathname[-1])-2)]
        filtered_df = df[df['PATIENT_ID'] == selected_patient]

        note_items = []
        for _, row in filtered_df.iterrows():
            note_date = row['DAY']
            note_type = row['NOTE_TYPE']
            note_content = row['NOTE']
            
            note_item = html.Div(
                children=[
                    html.Div(
                        html.P(f"Type: {note_type}")
                    ),
                    html.Div(children =[
                    html.P(f"Note: {note_content}"),
                    html.H6(f"Date:Sent on the {note_date}")])
                    
                ],
                style={'border': '1px solid black', 'padding': '10px',"margin-top":'40px', 'margin-bottom': '10px','overflow-y':'auto' }
            )
            note_items.append(note_item)

        return html.Div([notesFeed, html.Div(dcc.Graph(className='graph', figure=get_patient_graph(selected_patient))),html.Div(
                note_items, style={
                'height':'400px',
            'overflow-y':'scroll',
            #'position':'absolute',
            #'right':'2px',
            'top-padding':'10px',
            'left-margin':'10px',
            'border': '2px solid black'
            })])
    

    # If the user tries to reach a different page, return a 404 message
    return layout

    #     html.Div(
    #     [
    #         html.H1("404: Not found", className="text-danger"),
    #         html.Hr(),
    #         html.P(f"The pathname {pathname} was not recognised..."),
    #     ],
    #     className="p-3 bg-light rounded-3",
    # )



convert={0: None, 1:"PAIN",2:"FALL",3:"HOSPITALIZATION"}



@app.callback(
    dash.dependencies.Output('note-feed', 'children'),
     dash.dependencies.Input('patient-dropdown', 'value')
)
def display_note_feed(selected_patient):
    if not selected_patient:
        return html.Div()

    filtered_df = df[df['PATIENT_ID'] == selected_patient]

    if filtered_df.empty:
        return html.Div()

    note_items = []
    for _, row in filtered_df.iterrows():
        note_date = row['DAY']
        note_type = row['NOTE_TYPE']
        note_content = row['NOTE']
        
        note_item = html.Div(
            children=[
                html.Div(
                      html.P(f"Type: {note_type}")
                ),
                html.Div(children =[
                html.P(f"Note: {note_content}"),
                html.H6(f"Date:Sent on the {note_date}")])
                
            ],
            style={'border': '1px solid black', 'padding': '10px',"margin-top":'40px', 'margin-bottom': '10px','overflow-y':'auto' }
        )
        note_items.append(note_item)

    return html.Div([html.Div(dcc.Graph(className='graph', figure=get_patient_graph(selected_patient))),html.Div(
            note_items, style={
            'height':'400px',
        'overflow-y':'scroll',
        #'position':'absolute',
        #'right':'2px',
        'top-padding':'10px',
        'left-margin':'10px',
        'border': '2px solid black'
        })])

@app.callback(
    Output('popover-confirm', 'n_clicks'),
    Output('card_main', 'children'),
    
    Input('checklist-input', 'value'),
    Input('popover-confirm', 'n_clicks'),
   
    )
def on_click_confirm(value, n_clicks):
    print(ctx.triggered_id)
    if ctx.triggered_id=='popover-confirm' and ctx.triggered_id!="checklist-input":
        present = [convert[i] for i in value]
        curr = recent_events.loc[recent_events["INCIDENT"].isin(present),:]
        
    return 0, [dbc.Card([dbc.CardBody([html.H5(recent_events["INCIDENT"][i].title(), className="card-title"),html.Span("Patient : "+recent_events["PATIENT_ID"][i]), html.Br(),
                    html.Span(recent_events["DAY"][i].strftime('%Y-%m-%d') +" ; "+ recent_events["INCIDENT_TIME"][i].strftime('%H:%M'))])], 
                                    style={"maxHeight": "115px","background-color":recent_events["COLOR"][i], 'color':'white'}) for i in curr.index]
