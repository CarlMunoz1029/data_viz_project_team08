'''
    This file contains the functions to call when
    a click is detected on the map, depending on the context
'''
import dash_html_components as html


def no_clicks(style):
    '''
        Deals with the case where the map was not clicked

        Args:
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle no clicks on the mapp
    mode = None
    theme = None
    title = None
    style['visibility'] = 'hidden'
    
    return title, mode, theme, style


def map_base_clicked(title, mode, theme, style):
    '''
        Deals with the case where the map base is
        clicked (but not a marker)

        Args:
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    if title is not None:
        title = None
    
    if mode is not None:
            mode = None
            
    if theme is not None:
        theme = None

    if style is not None:
        style['visibility'] = 'hidden'

    return title, mode, theme, style


def map_marker_clicked(figure, curve, point, title, mode, theme, style): # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long
    '''
        Deals with the case where a marker is clicked

        Args:
            figure: The current figure
            curve: The index of the curve containing the clicked marker
            point: The index of the clicked marker
            title: The current display title
            mode: The current display title
            theme: The current display theme
            style: The current display style for the panel
        Returns:
            title: The updated display title
            mode: The updated display title
            theme: The updated display theme
            style: The updated display style for the panel
    '''
    # TODO : Handle clicks on the markers

    info = figure.get('data')[curve].get('customdata')[point]
    
    title_color = figure.get('data')[curve].get('marker').get('color')
    title = html.Div(id='marker-title', 
                     style={'color': title_color}, 
                     children=[html.Span(info[0])])
    
    mode = info[2]

    ## TODO: expand details on click.
    
    lis = info[1].split("\n")
    theme =  html.Div(children=[html.Div(
        id="b1", children=[
                html.Span("Thématique :"), 
                html.Ul(id="mylist", 
                children=[html.Li(i) for i in lis])], 
            style={"border":"1px solid green","maxHeight": "115px", "background-color":"coral"}),
                      html.Div(
        id="b2", children=[
                html.Span("Thématique :"), 
                html.Ul(id="mylist", 
                children=[html.Li(i) for i in lis])], 
            style={"border":"1px solid green", "maxHeight": "115px","background-color":"darkseagreen"})],
        style={"maxHeight": "415px", "overflow-y":"scroll"})
    
    # style is a dictionnary...
    style['visibility'] = 'visible'

    return title, mode, theme, style