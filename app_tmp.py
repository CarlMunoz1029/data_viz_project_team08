
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file is the entry point for our dash app.
'''


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

import pandas as pd


app = dash.Dash(__name__)
app.title = 'TP2 | INF8808'

"""
def prep_data():
    '''
        Imports the .csv file and does some preprocessing.

        Returns:
            A pandas dataframe containing the preprocessed data.
    '''
    dataframe = pd.read_csv('./assets/data/romeo_and_juliet.csv')

    proc_data = preprocess.summarize_lines(dataframe)
    proc_data = preprocess.replace_others(proc_data)
    proc_data = preprocess.clean_names(proc_data)

    return proc_data
"""


def init_app_layout(figure):
    '''
        Generates the HTML layout representing the app.

        Args:
            figure: The figure to display.
        Returns:
            The HTML structure of the app's web page.
    '''
    
    theme = html.Div(children=[
    html.Div(html.Button("Filter (does nothing atm)"), style={'padding':'50px'}),
    html.Div(children=[
        html.Div(
         children=[
                html.Span("Thématique :"), 
                html.Span("testing1")], 
            style={"border":"1px solid green","maxHeight": "115px", "background-color":"coral"}),
        html.Div(
         children=[
                html.Span("Thématique :"), html.Br(),
                html.Span("testing2")],  
            style={"border":"1px solid green", "maxHeight": "115px","background-color":"darkseagreen"})],
        style={"maxHeight": "1015px", "overflow-y":"scroll"})])
    
    layout = html.Div(
        className='row',
        children=[
            html.Div(
                className='view-div',
                style={
                    'justifyContent': 'center',
                    'alignItems': 'center',
                    'text-align':'center',
                    'display': 'inline-block',
                    'min-width' : '40vw',
                    'padding':'10vh'},
                children=[
                    html.Span("Insert figure here")]),
            html.Div(
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
                                    'fontSize': '16px'})])])])
    #return html.Div(className='content', children=[
    #    html.Header(children=[
    #        html.H1('Who\'s Speaking?'),
    #        html.H2('An analysis of Shakespeare\'s Romeo and Juliet')
    #    ])
    #])

    return layout

@app.callback(
    [Output('line-chart', 'figure'), Output('mode', 'children')],
    [Input('radio-items', 'value')],
    [State('line-chart', 'figure')]
)

def radio_updated(mode, figure):
    '''
        Updates the application after the radio input is modified.

        Args:
            mode: The mode selected in the radio input.
            figure: The figure as it is currently displayed
        Returns:
            new_fig: The figure to display after the change of radio input
            mode: The new mode
    '''
    # Update the figure's data and y axis, as well as the informational
    # text indicating the mode (Rose)
    #new_fig = bar_chart.draw(figure, data, mode)
    #new_mode = mode
    #return new_fig, new_mode


#data = prep_data()

#create_template()

#fig = bar_chart.init_figure()
fig=None

app.layout = init_app_layout(fig)